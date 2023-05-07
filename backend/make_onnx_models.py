#!/usr/bin/env python

from sys import argv
from glob import glob
import warnings

import torch
from segment_anything import sam_model_registry
from segment_anything.utils.onnx import SamOnnxModel

from onnxruntime.quantization import QuantType
from onnxruntime.quantization.quantize import quantize_dynamic


def to_onnx(model_type: str, checkpoint: str):
    """Converts a .pth checkpoint in a directory into 2 ONNX files: normal and quantized"""

    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    onnx_model = SamOnnxModel(sam, return_single_mask=True)

    dynamic_axes = {
        "point_coords": {1: "num_points"},
        "point_labels": {1: "num_points"},
    }

    embed_dim = sam.prompt_encoder.embed_dim
    embed_size = sam.prompt_encoder.image_embedding_size
    mask_input_size = [4 * x for x in embed_size]
    dummy_inputs = {
        "image_embeddings": torch.randn(1, embed_dim, *embed_size, dtype=torch.float),
        "point_coords": torch.randint(low=0, high=1024, size=(1, 5, 2), dtype=torch.float),
        "point_labels": torch.randint(low=0, high=4, size=(1, 5), dtype=torch.float),
        "mask_input": torch.randn(1, 1, *mask_input_size, dtype=torch.float),
        "has_mask_input": torch.tensor([1], dtype=torch.float),
        "orig_im_size": torch.tensor([1500, 2250], dtype=torch.float),
    }
    output_names = ["masks", "iou_predictions", "low_res_masks"]

    onnx_model_path = f"models/{model_type}/sam_onnx_example.onnx"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        with open(onnx_model_path, "wb") as f:
            torch.onnx.export(
                onnx_model,
                tuple(dummy_inputs.values()),
                f,
                export_params=True,
                verbose=False,
                opset_version=17,
                do_constant_folding=True,
                input_names=list(dummy_inputs.keys()),
                output_names=output_names,
                dynamic_axes=dynamic_axes,
            )

    onnx_model_quantized_path = f"models/{model_type}/sam_onnx_quantized_example.onnx"
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
        warnings.filterwarnings("ignore", category=UserWarning)
        quantize_dynamic(
            model_input=onnx_model_path,
            model_output=onnx_model_quantized_path,
            optimize_model=True,
            per_channel=False,
            reduce_range=False,
            weight_type=QuantType.QUInt8,
        )


if __name__ == '__main__':
    assert len(argv) == 2, f"Usage: {argv[0]} model_type"
    model_type = argv[1]
    checkpoints = sorted(glob(f"models/{model_type}/*.pth"))
    assert checkpoints, f"Need at least one .pth checkpoint in models/{model_type}"
    checkpoint = checkpoints[0]
    to_onnx(model_type=model_type, checkpoint=checkpoint)

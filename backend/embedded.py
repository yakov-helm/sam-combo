import torch
import numpy as np
import cv2
import matplotlib.pyplot as plt

import argparse
import onnxruntime

from onnxruntime.quantization import QuantType
from onnxruntime.quantization.quantize import quantize_dynamic

from segment_anything import sam_model_registry, SamPredictor
from segment_anything.utils.onnx import SamOnnxModel

def make_embedding(encode, root:str, checkpoint:str, model_type:str):
    encode = np.fromstring(encode, dtype = np.uint8)
    image = cv2.imdecode(encode, cv2.IMREAD_UNCHANGED)
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    sam.to(device='cuda')
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    np.save(root, image_embedding)


def make_new_embedding(filename: str, checkpoint="models/sam_vit_b_01ec64.pth", model_type="vit_b") -> dict:
    """
    Outputs image.jpg.npy for an image called image.jpg.
    Returs a dictionary: {'npy': 'image.jpg.npy'}
    """
    print("FILENAME", filename)
    image = cv2.imread(filename)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    sam.to(device='cuda')
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    result = f"{filename}.npy"
    np.save(result, image_embedding)
    return {'npy': result}

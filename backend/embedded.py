import numpy as np
import cv2
from glob import glob
import logging

from segment_anything import sam_model_registry, SamPredictor

def make_embedding(model_type: str, img_path: str, npy_path: str) -> dict:
    """
    Outputs image.jpg.vit_h.npy for an image called image.jpg.
    Returs a dictionary: {'npy': 'image.jpg.vit_h.npy'}
    """
    logging.info(f"INPUT FILE: {img_path}")
    checkpoints = sorted(glob(f"models/{model_type}/*.pth"))
    assert checkpoints, f"models/{model_type} is missing a checkpoint"
    checkpoint = checkpoints[0]

    print("GOT CHECKPOINT", checkpoint)

    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    sam = sam_model_registry[model_type](checkpoint=checkpoint)
    sam.to(device='cuda')
    
    predictor = SamPredictor(sam)
    predictor.set_image(image)
    image_embedding = predictor.get_image_embedding().cpu().numpy()
    
    np.save(npy_path, image_embedding)
    return {'npy': npy_path}

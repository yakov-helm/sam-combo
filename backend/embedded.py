import numpy as np
import cv2
from glob import glob
import logging
from sys import argv, exit
from os.path import isfile

from segment_anything import sam_model_registry, SamPredictor

def make_embedding(model_type: str, img_path: str, npy_path: str, use_cached=True) -> dict:
    """
    Outputs image.jpg.vit_h.npy for an image called image.jpg.
    Returs a dictionary: {'npy': 'image.jpg.vit_h.npy'}
    """
    if isfile(npy_path) and use_cached:
        print("RE-USING EXISTING EMBEDDING IN", npy_path)
        return {"npy": npy_path}
    
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
    
    print(f"PRODUCED EMBEDDING IN {npy_path}")
    np.save(npy_path, image_embedding)
    return {'npy': npy_path}


if __name__ == '__main__':
    # apply make_embedding to the combo
    if len(argv) < 4:
        print(f"Usage: {argv[0]} model_type image_path npy_path")
        exit(0)

    model_type = argv[1]
    image_path = argv[2]
    npy_path = argv[3]

    make_embedding(model_type, image_path, npy_path)

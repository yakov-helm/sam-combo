from fastapi import FastAPI, Request, Response
import uvicorn
from starlette.middleware.cors import CORSMiddleware

import os
from PIL import Image

from embedded import make_embedding

app = FastAPI()


GALLERY = "assets/gallery"

def get_images(dir_name: str, n=0):
    """Return the list of images in the directory; returns a max of n if n > 0."""
    fnames = [fname for fname in os.listdir(dir_name) if fname.endswith('.jpg') or fname.endswith('.png')]
    fnames = [f"{dir_name}/{fname}" for fname in fnames]
    return fnames


@app.get("/ai/list-dirs")
async def list_dirs(request: Request):
    """List directories and the number of images."""
    body = await request.body()
    fnames = [f"{GALLERY}/{fname}" for fname in os.listdir(GALLERY)]
    dir_names = [fname for fname in fnames if os.path.isdir(fname)]
    out = [{'name': dir_name.split('/')[-1], 'count': len(get_images(dir_name))} for dir_name in dir_names]
    result = {"dirs": out}
    return result


@app.get("/ai/list/{dir_name}")
async def list_images(request: Request, dir_name: str) -> dict:
    """List images in the directory"""
    body = await request.body()
    fnames = get_images(f"{GALLERY}/{dir_name}")
    out = []
    for fname in sorted(fnames):
        im = Image.open(fname)
        w, h = im.size
        out.append({'src': fname, 'width': w, 'height': h})
    result = {"images": out}
    return result


@app.post("/ai/embedded/{model_type}/{dir_name}/{file_name}")
async def embedded(request: Request, model_type: str, dir_name: str, file_name: str):
    body = await request.body()
    img_path = f"{GALLERY}/{dir_name}/{file_name}"
    npy_path = f"{img_path}.{model_type}.npy"
    print("COMPUTING THE EMBEDDING FOR", img_path)
    result = make_embedding(model_type, img_path, npy_path)
    return result


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host="localhost",
        port=8000,
        reload=True,
    )

from fastapi import FastAPI, Request, Response
import uvicorn
from starlette.middleware.cors import CORSMiddleware

import os
import functools
from PIL import Image

from embedded import make_embedding

app = FastAPI()

PREFIX = "assets/gallery"
GALLERY = f"{os.path.abspath(os.path.join(os.getcwd(), os.pardir))}/frontend/public/{PREFIX}"


@app.get("/ai/list")
async def list_files(request: Request):
    body = await request.body()
    fnames = [fname for fname in os.listdir(GALLERY) if fname.endswith('.jpg') or fname.endswith('.png')]
    out = []
    for fname in sorted(fnames):
        im = Image.open(f"{GALLERY}/{fname}")
        w, h = im.size
        out.append({'src': f"/{PREFIX}/{fname}", 'width': w, 'height': h})
    return {"files": out}


@functools.lru_cache()
@app.post("/ai/embedded/{file_name}")
async def embedded(request: Request, file_name: str):
    print("COMPUTING THE EMBEDDING")
    body = await request.body()
    root = f"{GALLERY}/{file_name}.npy"
    if not os.path.isfile(root):
        checkpoint = "sam_vit_b.pth"
        model_type = "vit_b"
        print('PRODUCED EMBEDDING IN', root)
        make_embedding(body, root, checkpoint, model_type)
    return {"npy": f"{file_name}.npy"}


@app.post("/ai/embedded/all/{file_name}")
async def embedded(request: Request, file_name:str):
    return Response(status_code=200)


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

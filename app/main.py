from contextlib import asynccontextmanager
import os

import fasttext
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .health import LIDHealthResponse, health_endpoint
from .lid import LIDResponse, lid_endpoint
from . import shared


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(shared.MODEL_PATH.parent, exist_ok=True)
    if not shared.MODEL_PATH.exists():
        raise RuntimeError(
            f"Missing FastText model file: {shared.MODEL_PATH}. "
            "Place lid.176.bin in the resources directory."
        )
    with shared.model_lock:
        shared.model = fasttext.load_model(str(shared.MODEL_PATH))
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health", response_model=LIDHealthResponse)
def health() -> LIDHealthResponse:
    return health_endpoint()


@app.get("/lid", response_model=LIDResponse)
def detect(text: str) -> LIDResponse:
    return lid_endpoint(text=text, k=5)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=8004, reload=True)

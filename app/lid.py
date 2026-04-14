from typing import List
import time

from fastapi import HTTPException
from pydantic import BaseModel

from . import shared


class LIDCandidate(BaseModel):
    lang: str
    score: float

class LIDRequest(BaseModel):
    text: str
    k: int = 1

class LIDResponse(BaseModel):
    candidates: List[LIDCandidate]
    runtime_ms: float


def lid_endpoint(request: LIDRequest) -> LIDResponse:
    tic = time.perf_counter()
    with shared.model_lock:
        loaded_model = shared.model

    if loaded_model is None:
        raise HTTPException(status_code=503, detail="Model not loaded.")

    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Parameter 'text' must be non-empty.")

    # Use pybind directly to avoid fasttext wrapper/NumPy 2 copy=False incompatibility.
    raw = loaded_model.f.predict(request.text, int(request.k), 0.0, "strict")
    candidates = [
        LIDCandidate(lang=label.replace("__label__", ""), score=float(prob))
        for prob, label in raw
    ]
    runtime_ms = time.perf_counter() - tic
    return LIDResponse(candidates=candidates, runtime_ms=runtime_ms * 1000)

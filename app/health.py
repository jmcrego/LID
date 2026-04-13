from pydantic import BaseModel

from . import shared


class LIDHealthResponse(BaseModel):
    status: str
    model_loaded: bool
    model_path: str
    runtime_ms: float


def health_endpoint() -> LIDHealthResponse:
    import time
    tic = time.perf_counter()
    with shared.model_lock:
        loaded = shared.model is not None
    runtime_ms = time.perf_counter() - tic
    return LIDHealthResponse(
        status="ok",
        model_loaded=loaded,
        model_path=str(shared.MODEL_PATH),
        runtime_ms=runtime_ms * 1000,
    )

"""KohliIQ ML inference service (Phase 1 foundation).

Owns ONLY model loading + inference + model metadata (Phase 9).
Never touches MySQL; never duplicates Spring Boot business logic.
"""
from fastapi import FastAPI

app = FastAPI(title="KohliIQ Inference")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "kohliiq-inference"}

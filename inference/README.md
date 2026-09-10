# KohliIQ Inference (FastAPI)

Pure ML inference service. Called only by Spring Boot:
`React → Spring Boot → FastAPI → model → FastAPI → Spring Boot → React`.

- Run (Phase 9+): `uvicorn app.main:app --port 8000` (from `inference/`).
- No MySQL access. Prediction endpoints arrive in Phase 9.

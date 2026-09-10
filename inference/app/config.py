"""Inference-service settings (env-driven, no secrets in code)."""
import os

MODEL_PATH = os.getenv("MODEL_PATH", "../ml/artifacts/expected_runs.json")
PORT = int(os.getenv("PORT", "8000"))

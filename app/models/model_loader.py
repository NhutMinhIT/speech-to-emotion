import os
import joblib
from typing import Dict, Any

_MODEL_BUNDLE: Dict[str, Any] | None = None


def _candidate_model_dirs() -> list[str]:
    """
    Ưu tiên: ./app/models (đúng với repo của bạn)
    Fallback: ./models (nếu sau này bạn di chuyển)
    """
    here = os.path.abspath(os.path.dirname(__file__))
    repo_root = os.path.abspath(os.path.join(here, "..", ".."))
    return [
        os.path.join(repo_root, "app", "models"),
        os.path.join(repo_root, "models"),
    ]


def get_model_bundle() -> dict:
    global _MODEL_BUNDLE
    if _MODEL_BUNDLE is None:
        last_err = None
        for mdir in _candidate_model_dirs():
            try:
                model = joblib.load(os.path.join(mdir, "rf_emotion_model_v2.pkl"))
                scaler = joblib.load(os.path.join(mdir, "scaler_v2.pkl"))
                encoder = joblib.load(os.path.join(mdir, "encoder_v2.pkl"))
                _MODEL_BUNDLE = {"model": model, "scaler": scaler, "encoder": encoder}
                break
            except Exception as e:
                last_err = e
                continue
        if _MODEL_BUNDLE is None:
            raise RuntimeError(f"Cannot load model artifacts. Last error: {last_err}")
    return _MODEL_BUNDLE

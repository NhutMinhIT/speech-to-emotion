from fastapi import HTTPException
from ..services.audio_service import load_audio_to_wav
from ..services.feature_service import extract_features_scaled
from ..models.model_loader import get_model_bundle
from ..enum.Emotion import Emotion


def predict_emotion(file_bytes: bytes, filename: str | None = None):
    # 1) bytes -> (y, sr)
    try:
        y, sr = load_audio_to_wav(file_bytes, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid audio: {e}")

    # 2) features -> scaled
    X = extract_features_scaled(y, sr)
    if X is None:
        raise HTTPException(status_code=422, detail="Feature extraction failed")

    # 3) predict -> decode label
    bundle = get_model_bundle()
    model = bundle["model"]
    encoder = bundle["encoder"]

    pred_enc = model.predict(X)[0]
    label = encoder.inverse_transform([pred_enc])[0]
    label_str = str(label).replace("np.str_('", "").replace("')", "")
    try:
        display_label = Emotion[label_str].value
    except KeyError:
        display_label = label_str

    return {"label": display_label, "sample_rate": sr}

import numpy as np
import librosa
from ..utils.dsp import butter_bandpass_filter
from ..models.model_loader import get_model_bundle


def extract_features(y: np.ndarray, sr: int = 22050) -> np.ndarray | None:
    try:
        y_f = butter_bandpass_filter(y, fs=sr)
        mfccs = np.mean(librosa.feature.mfcc(y=y_f, sr=sr, n_mfcc=20).T, axis=0)
        rms = np.mean(librosa.feature.rms(y=y_f).T, axis=0)
        zcr = np.mean(librosa.feature.zero_crossing_rate(y=y_f).T, axis=0)
        feats = np.hstack((mfccs, rms, zcr))
        return feats
    except Exception as e:
        print("Feature extraction error:", e)
        return None


def extract_features_scaled(y: np.ndarray, sr: int = 22050) -> np.ndarray | None:
    feats = extract_features(y, sr)
    if feats is None:
        return None
    X = feats.reshape(1, -1)
    scaler = get_model_bundle()["scaler"]
    Xs = scaler.transform(X)
    return Xs

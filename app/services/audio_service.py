import io
import librosa
from pydub import AudioSegment  # cần ffmpeg nếu input là mp3/ogg/webm
import soundfile as sf  # giữ để librosa không cảnh báo backend
from typing import Tuple

TARGET_SR = 22050


def _bytes_to_wav_bytes(src_bytes: bytes, filename: str | None = None) -> bytes:
    name = (filename or "").lower()
    if name.endswith(".wav"):
        return src_bytes

    # chuyển mọi định dạng phổ biến -> WAV
    audio = AudioSegment.from_file(io.BytesIO(src_bytes))
    out_buffer = io.BytesIO()
    audio.export(out_buffer, format="wav")
    return out_buffer.getvalue()


def load_audio_to_wav(
    file_bytes: bytes, filename: str | None = None
) -> Tuple[list, int]:
    wav_bytes = _bytes_to_wav_bytes(file_bytes, filename)
    # librosa load từ buffer; resample và mono hoá
    y, sr = librosa.load(io.BytesIO(wav_bytes), sr=TARGET_SR, mono=True)
    return y, sr

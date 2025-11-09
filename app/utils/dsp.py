from scipy.signal import butter, lfilter


def butter_bandpass_filter(data, lowcut=100.0, highcut=8000.0, fs=22050, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    y_filtered = lfilter(b, a, data)
    return y_filtered

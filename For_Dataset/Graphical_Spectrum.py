import librosa
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. Load Audio
# ==============================
audio_path = "data/noakhali.wav"
y, sr = librosa.load(audio_path, sr=16000)

# ==============================
# 2. FFT (Frequency Spectrum)
# ==============================
fft = np.fft.fft(y)
magnitude = np.abs(fft)

freqs = np.fft.fftfreq(len(magnitude), 1 / sr)

# ==============================
# 3. Keep only positive frequencies
# ==============================
half = len(freqs) // 2

# ==============================
# 4. Plot
# ==============================
plt.figure(figsize=(10, 4))
plt.plot(freqs[:half], magnitude[:half])
plt.title("Frequency Spectrum")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.tight_layout()
plt.show()

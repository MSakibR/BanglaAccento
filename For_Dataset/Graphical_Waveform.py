import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# ==============================
# 1. Load Audio
# ==============================
audio_path = "data/chittagong.wav"
y, sr = librosa.load(audio_path, sr=16000)

# ==============================
# 2. Time axis (IMPORTANT for proper plot)
# ==============================
time = np.linspace(0, len(y) / sr, num=len(y))

# ==============================
# 3. Plot Waveform
# ==============================
plt.figure(figsize=(10, 4))
plt.plot(time, y)
plt.title("Waveform")
plt.xlabel("Time (seconds)")
plt.ylabel("Amplitude")
plt.tight_layout()
plt.show()

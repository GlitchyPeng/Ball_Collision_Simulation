import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pywt

# Load audio file
filename = ''
y, sr = librosa.load(filename)

# Wavelet Transform
wavelet = 'db4'  # Choose a suitable wavelet
coeffs = pywt.wavedec(y, wavelet)

# Noise Reduction (Thresholding)
threshold = 0.1  # Adjust threshold based on noise level
coeffs[1:] = [pywt.threshold(i, value=threshold, mode='soft') for i in coeffs[1:]]

# Inverse Wavelet Transform
y_denoised = pywt.waverec(coeffs, wavelet)

# Ensure that y_denoised is the same length as y
if len(y_denoised) > len(y):
    y_denoised = y_denoised[:len(y)]
else:
    y_denoised = np.pad(y_denoised, (0, len(y) - len(y_denoised)), mode='constant')

# Compute FFTs
y_fft = np.fft.fft(y)
y_denoised_fft = np.fft.fft(y_denoised)

# Calculate frequencies
freqs = np.fft.fftfreq(len(y), 1/sr)

# Plot FFTs
plt.figure(figsize=(14, 5))
plt.plot(freqs, np.abs(y_fft), label='Original')
plt.plot(freqs, np.abs(y_denoised_fft), label='Denoised')
plt.title('FFT Comparison')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.show()

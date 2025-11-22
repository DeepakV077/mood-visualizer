try:
    import sys
    import time
except ImportError as e:
    raise ImportError("Python standard modules are required") from e

try:
    from eeg_simulator import EEGSimulator
    from visualizer import Visualizer
except ImportError as e:
    raise ImportError("Make sure all project files are present and numpy/scipy/pygame are installed") from e

import numpy as np


class LocalSmoother:
    def __init__(self, alpha=0.35):
        self.alpha = alpha
        self.ema = None

    def update(self, vec):
        vec = np.asarray(vec)
        if self.ema is None:
            self.ema = vec
        else:
            self.ema = self.alpha * vec + (1.0 - self.alpha) * self.ema
        return self.ema


def compute_relative_bands_local(sig, fs):
    sig = np.asarray(sig)
    if sig.size == 0:
        return np.array([0.0, 0.0, 0.0])
    n = sig.size
    freqs = np.fft.rfftfreq(n, 1.0/fs)
    ps = np.abs(np.fft.rfft(sig))**2
    def band_energy(fmin, fmax):
        idx = (freqs >= fmin) & (freqs <= fmax)
        return float(ps[idx].sum())
    a = band_energy(8, 12)
    b = band_energy(13, 30)
    g = band_energy(30, 45)
    total = a + b + g + 1e-12
    return np.array([a/total, b/total, g/total])


def classify_mood_local(rel_bands, alpha_thresh=1.2, beta_thresh=1.2):
    a, b, g = rel_bands
    if a > b * alpha_thresh and a > g * 1.1:
        return "CALM"
    if b > a * beta_thresh or (b + 0.8 * g) > a * 1.25:
        return "FOCUS"
    if g > 0.5:
        return "STRESS"
    return "UNKNOWN"

FS = 128  # Hz
WINDOW_SIZE = 128

def main():
    # create simulator with sampling rate
    eeg = EEGSimulator(FS)
    smoother = LocalSmoother()
    vis = Visualizer()

    try:
        while True:
            # simulate EEG signal (get_samples takes duration in seconds)
            sig = eeg.get_samples(duration_sec=(WINDOW_SIZE / FS))
            rel_bands = compute_relative_bands_local(sig, FS)
            smoothed = smoother.update(rel_bands)
            mood = classify_mood_local(smoothed)
            vis.update(mood, smoothed, (WINDOW_SIZE / FS))
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        vis.close()

if __name__ == "__main__":
    main()

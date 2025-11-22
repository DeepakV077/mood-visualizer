"""
eeg_simulator.py
Simple, realistic-ish single-channel EEG simulator.

Provides:
 - EEGSimulator.get_samples(duration_sec=1.0) -> numpy array (n_samples,)
 - EEGSimulator.trigger_blink() to inject a transient blink-like artifact
"""
try:
    import numpy as np
except ImportError as e:
    raise ImportError("numpy is required for eeg_simulator.py. Install it with 'pip install numpy' or 'pip install -r requirements.txt'") from e

class EEGSimulator:
    def __init__(self, fs: int = 250, seed: int = None):
        self.fs = fs
        self.dt = 1.0 / fs
        self.t = 0.0
        self.rng = np.random.default_rng(seed)
        self._blink_pending = False

    def get_samples(self, duration_sec: float = 1.0):
        """
        Return a 1-D numpy array of simulated EEG samples for the given duration.
        """
        n = int(self.fs * duration_sec)
        t = np.linspace(self.t, self.t + duration_sec, n, endpoint=False)
        # rhythmic components: alpha (8-12 Hz), beta (13-30 Hz), gamma (~35-45 Hz)
        alpha = 0.8 * np.sin(2 * np.pi * 10.0 * t + self.rng.random() * 2*np.pi)
        beta  = 0.5 * np.sin(2 * np.pi * 20.0 * t + self.rng.random() * 2*np.pi)
        gamma = 0.25 * np.sin(2 * np.pi * 40.0 * t + self.rng.random() * 2*np.pi)
        # slow wandering baseline and noise
        baseline = 0.15 * np.sin(2 * np.pi * 0.2 * t + self.rng.random() * 2*np.pi)
        noise = 0.35 * self.rng.normal(scale=1.0, size=n)

        sig = alpha + beta + gamma + baseline + noise

        # optionally inject a blink-like transient
        if self._blink_pending:
            burst = self._make_blink(n)
            sig += burst
            self._blink_pending = False

        self.t += duration_sec
        return sig

    def trigger_blink(self):
        """Mark that next call to get_samples will include a blink artifact."""
        self._blink_pending = True

    def _make_blink(self, n):
        # transient Gaussian-shaped large amplitude (very short)
        center = int(0.2 * n)
        sigma = max(1, int(0.02 * n))
        x = np.arange(n)
        burst = 25.0 * np.exp(-0.5 * ((x - center) / sigma) ** 2)
        # channel-specific random sign
        sign = 1 if self.rng.random() > 0.5 else -1
        return sign * burst

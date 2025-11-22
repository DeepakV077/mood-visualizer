# Mood Visualizer

A tiny demo that simulates single-channel EEG, extracts simple band features (alpha/beta/gamma), classifies the user's "mood" (CALM / FOCUS / STRESS), and renders a live visual using Pygame. The project is intentionally small and educational — useful for prototyping biofeedback visuals or learning DSP basics.

This README contains everything you need to run, develop, and contribute.

## Quick overview

- `app.py` — application entrypoint. Ties together the simulator, feature extraction/smoothing, classification, and the visualizer.
- `eeg_simulator.py` — single-channel EEG signal simulator (alpha/beta/gamma components + noise + blink artifact trigger).
- `signal_processor.py` — bandpower (Welch) helper, EMA smoother, and a rule-based mood classifier.
- `visualizer.py` — Pygame visualizer. If Pygame is unavailable, a console fallback is provided so the app remains runnable.
- `requirements.txt` — Python dependencies (numpy, scipy, pygame).

## Prerequisites

- Python 3.8 - 3.12 is recommended for best compatibility with Pygame wheels. Newer Python versions may not have prebuilt pygame wheels yet.
- Git (optional for cloning/contributing)

If you plan to run development in VS Code, select the interpreter that contains the project dependencies so Pylance resolves imports.

## Install (recommended)

Open PowerShell in the project root (`d:\intentPredict\mood-visualizer`) and run:

```powershell
# create & activate a venv (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install requirements into the active venv
pip install -r requirements.txt
```

Notes:
- On some Windows setups with very new Python versions, `pygame` wheels may be missing. If `pip install pygame` fails, try using a slightly older Python (3.11 or 3.10) or consult the pygame downloads page.

## Run the app

With the venv activated (see above), run:

```powershell
python app.py
```

Controls (when the Pygame UI is available):
- SPACE : inject a simulated blink artifact (useful for testing)
- ESC or close window : quit

If Pygame is not available the project will run with a console visualizer and you will still get feature/classification prints.

## Troubleshooting

- Pylance / "Import X could not be resolved":
	- This is a static analysis warning from VS Code. Make sure the selected Python interpreter (bottom-right in VS Code) points to the environment where you installed dependencies (for example, `d:\intentPredict\.venv\Scripts\python.exe`).
	- You can also use the provided `.vscode/settings.json` which recommends the workspace venv.

- `ModuleNotFoundError: No module named 'numpy'` (or scipy/pygame):
	- Activate your venv and run `pip install -r requirements.txt` (see Install section). Use `python -m pip install` if you have multiple Python installs:

```powershell
# explicit target interpreter
D:\intentPredict\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

- Pygame install fails on Windows with your Python version:
	- Try installation with a supported Python version (3.10/3.11). Alternatively, run with the console fallback (no pygame required).

## Development notes

- The project includes import guards and a console fallback so `app.py` remains runnable even if Pygame or other optional modules are not present.
- The `signal_processor.py` uses `scipy.signal.welch` for bandpower. If you prefer a simpler/portable fallback, `app.py` contains a tiny FFT-based estimator used when `signal_processor` import is not available.

### Project structure

```
mood-visualizer/
	├─ app.py                 # entrypoint
	├─ eeg_simulator.py       # synthetic EEG generator
	├─ signal_processor.py    # bandpower, smoothing, classifier
	├─ visualizer.py          # pygame visual + console fallback
	├─ requirements.txt       # numpy, scipy, pygame
	└─ assets/
			└─ colors.json        # optional color mapping
```

## Tests / Smoke checks

You can perform a quick smoke run (no UI) by running a short Python snippet that imports the modules and calls a few update cycles. The code in `app.py` already contains a lightweight learning-friendly pipeline.

## Contributing

Contributions and feedback are welcome. If you want to help the project or improve the Pygame visuals, please:

1. Fork the repo and create a feature branch
2. Run tests / smoke checks locally
3. Open a pull request with a short description and screenshots (if relevant)

If your contribution is Pygame-related, consider reading the Pygame contribution guidelines: https://www.pygame.org/contribute.html

## License

This project is provided under the MIT license. Use freely, and please attribute if you publish derived work.

---

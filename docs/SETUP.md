# Preliminary setup

## Prerequisites

- A computer or Raspberry Pi running a desktop environment capable of displaying Tkinter windows.
- Python 3 and a camera OpenCV can open using device index `0` (camera compatibility has not been tested here).
- System Tkinter support (`python3-tk` on Raspberry Pi OS / Debian-based Linux).
- OpenCV, NumPy, Pillow, and Matplotlib Python packages.

## Debian/Raspberry Pi OS example

```bash
sudo apt update
sudo apt install python3 python3-venv python3-tk
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python code.py
```

These are general environment setup commands, **not a verified Raspberry Pi test**. Installing OpenCV may require an OS-specific package or a compatible Python build depending on the Raspberry Pi model, operating system, and Python version.

## What will and will not work as provided

The supplied script can be parsed as Python source but has **not been run here with a Raspberry Pi camera and desktop**. In its current form, photo capture and analysis will likely fail because the capture output filename differs from the file later opened for analysis. There are also nonportable absolute paths, a legacy Pillow resizing constant, and no handling for failed camera reads. Consult [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Pending prerequisites for YOLO inference

No complete executable YOLO script, weights, configuration, or label list was provided. This repository therefore does not yet have verified YOLO inference instructions or a model-installation procedure. Do not assume a particular YOLO version or weights filename without checking the original source.

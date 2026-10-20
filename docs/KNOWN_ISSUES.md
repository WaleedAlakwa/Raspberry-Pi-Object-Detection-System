# Known issues and verification status

The `code.py` file is copied from the user's upload **without modification**. The following issues were found through static inspection; runtime behavior was not tested.

| Issue | Source evidence | Practical impact |
| --- | --- | --- |
| Inconsistent image filenames | `photo_captured()` writes `opencv{n}.png` but opens `\home\pi\waleedalakwa\screenshot{n}.png` | The newly saved photo is not the file being displayed. The backslash path is also incorrect for Raspberry Pi OS. |
| Different analysis input path | `cracks_detection()` reads `/home/pi/waleedalakwa/screenshot{n}.png` | Analysis may fail because capture did not write that path. |
| Removed Pillow constant | Uses `Image.ANTIALIAS` | Current Pillow versions no longer provide it; use `Image.Resampling.LANCZOS` in a maintained version. |
| Unhandled camera failure | Uses `self.cap.read()[1]` without checking success | A missing/disconnected camera may result in an exception. |
| Analysis before photo | `self.i - 1` can equal `-1` | No valid image is available if analysis is clicked before capture. |
| Hard-coded desktop layout | Fixed 1500×750 window and placements | May not fit a small Raspberry Pi screen. |
| Camera resource cleanup | No explicit `self.cap.release()` on close | The camera may remain allocated until the process ends. |
| Detector source missing | YOLO appears in screenshots only | YOLO detection cannot be reproduced from the submitted script. |

## Suggested maintenance work (not silently applied)

1. Save and load captures through one shared `pathlib.Path` location, such as `outputs/`.
2. Check the result of every `VideoCapture.read()` call.
3. Use a supported Pillow resizing API (`Image.Resampling.LANCZOS`).
4. Handle the GUI close event and release the camera.
5. Avoid fixed pixels where possible; resize preview images to available panel dimensions.
6. Add the original YOLO detection script and licensed model files before documenting end-to-end detection.
7. Validate Raspberry Pi OS version, OpenCV camera backend, and interpreter/package versions.

Please review and test fixes on your actual hardware before marking the project fully reproducible.

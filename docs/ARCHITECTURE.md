# Architecture and processing notes

## Available source: `code.py`

The single complete uploaded script defines a `MainWindow` class and starts the GUI at module import time via `object = MainWindow()`.

### User interface

The script creates a fixed-size `1500 × 750` Tkinter window titled `Waleed Al-Akwa` and lays out three areas:

1. **Video capturing:** Displays frames from `cv2.VideoCapture(0)` on a Tkinter Canvas.
2. **Photo capturing:** Attempts to save a frame and display it in a separate panel.
3. **Photo analyzing:** Calls a function named `cracks_detection`, which applies classical filtering, edge processing, and ORB features to a saved frame.

### Data flow

```text
cv2.VideoCapture(0)
      ├── update_image() → BGR-to-RGB → PIL → ImageTk → canvas (100 ms update)
      └── photo_captured() → PNG frame
                                  ↓
                           cracks_detection()
                           ├── grayscale
                           ├── 3 × 3 mean blur
                           ├── logarithmic intensity transform
                           ├── bilateral filter (5, 75, 75)
                           ├── Canny (100, 200)
                           ├── morphology close (5 × 5 kernel)
                           └── ORB keypoints (nfeatures=1500)
```

The current file paths connecting the capture and processing stages do not agree, so this workflow describes intent, not confirmed execution.

## Detection demonstrated in screenshots, not in source

A separate screenshot of `yolo_object_detection.py` visibly uses `cv2.dnn.blobFromImage`, `net.forward`, bounding-box coordinate extraction, `cv2.dnn.NMSBoxes` (confidence threshold `0.5`, NMS threshold `0.4`), and rectangle/text overlays. **Those partial code lines are not sufficient to reproduce the YOLO pipeline**, and they are not implemented in `code.py`.

The screenshot of `test.py` shows a Tkinter GUI with video, photo, and detected-object controls, including `self.object_detection`. Its full function definitions and dependencies were not supplied. The blue-background demonstration screenshot may show this separate GUI version. The relationship among the scripts remains to be confirmed.

## Future integration checklist

- Add all original `.py` scripts, keeping their actual filenames or documenting renames.
- Determine which script is the main entry point.
- Define reproducible model and label-file acquisition.
- Use configurable paths (relative to the project root) instead of machine-specific absolute paths.
- Run and document a smoke test on the target Raspberry Pi model and camera.

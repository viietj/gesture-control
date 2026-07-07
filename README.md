# Hand Gesture Control

## Overview

Hand Gesture Control is a real-time computer vision application that enables users to control a computer using hand gestures captured by a webcam. The system is developed in Python using OpenCV, MediaPipe Hands, and PyAutoGUI. It recognizes predefined hand gestures and maps them to different computer actions.

## Features

- Real-time hand gesture recognition
- Mouse cursor movement
- Left-click operation
- Screenshot capture
- Page scrolling
- System volume control
- Media playback (Play/Pause)
- Next track control
- Open Apple Music from a predefined gesture

## Technologies

- Python
- OpenCV
- MediaPipe Hands
- PyAutoGUI

## Requirements

- Python 3.10 or later
- Webcam
  
## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python gesture_control.py
```

Make sure your webcam is connected before starting the program.

## Gesture Recognition

The application recognizes eight predefined hand gestures. To improve stability, a frame-based confirmation algorithm is applied before executing any action. This approach reduces false detections caused by temporary hand movements or recognition noise.

## Future Improvements

- Support for custom gestures
- Multi-hand recognition
- Adjustable gesture sensitivity
- Cross-platform optimization
- Graphical settings interface

## Author

Phan Viet Anh

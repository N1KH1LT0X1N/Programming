# Viral Meme Face Filter

Real-time face detection with AI-powered meme overlay. Detect your face and automatically overlay viral meme expressions!

## Features

- 🎥 Real-time webcam feed
- 😂 Multiple meme face filters
- 🎯 Fast face detection using Haar Cascades
- 🖼️ Smooth meme overlay on detected faces
- ⌨️ Easy keyboard controls

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

### Keyboard Controls

- `1-5`: Switch between different meme filters
- `s`: Save screenshot
- `q` or `ESC`: Quit

## Project Structure

```
.
├── src/
│   ├── main.py           # Main application
│   ├── face_detector.py  # Face detection logic
│   └── meme_overlay.py   # Meme overlay functionality
├── memes/                # Meme image assets
├── README.md
└── requirements.txt
```

## How It Works

1. Captures video from your webcam
2. Detects faces using OpenCV's Haar Cascade classifier
3. Overlays meme images on detected faces in real-time
4. Displays the modified feed

## Requirements

- Python 3.8+
- Webcam
- Windows/Mac/Linux


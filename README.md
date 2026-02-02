# PDF Image Extractor and Viewer

A Python utility that extracts images from PDF files and provides an interactive PyQt5-based GUI for viewing them.

## Features

- Extract all images from PDF files automatically
- Navigate through images using mouse scroll or keyboard arrows
- Buffered mode for reusing previously extracted images
- Zero-padded image naming for proper sorting

## Requirements

- Python 3.7+
- pypdf
- PyQt5
- tqdm

## Installation

```bash
pip install pypdf PyQt5 tqdm
```

## Usage

### Extract and view images from a PDF:
```bash
python imgs.py path/to/your/file.pdf
```

### Use pre-extracted images (buffered mode):
```bash
python imgs.py path/to/your/file.pdf -b
```

## Navigation

- **Mouse Wheel**: Scroll up/down to move between images
- **Arrow Keys**: Use Up/Down/Left/Right to navigate

## How It Works

1. Extracts images from each PDF page into an `images/` folder
2. Saves images as `image_XXXXXX.png` with zero-padded numbering
3. Launches an interactive viewer displaying images one at a time
4. Window title shows current image number (e.g., "Fig. 1")

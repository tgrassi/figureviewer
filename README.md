# FigureViewer

Tired of jumping around on a paper when authors cite figures two millions pages away?
Here is a Python utility that extracts images from PDF files and provides an interactive PyQt5-based GUI for viewing them.

## Features

- Extract all images from PDF files automatically
- Navigate through images using mouse scroll or keyboard arrows

## Requirements

- Python 3.7+
- pypdf
- PyQt5
- tqdm

## Installation and usage

```bash
git clone git@github.com:tgrassi/figureviewer.git
pip install pypdf PyQt5 tqdm
python imgs.py path/to/your/file.pdf
```
Use mouse wheel to scroll or keyboard arrows.

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

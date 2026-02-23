# FigureViewer

:weary: Tired of jumping around on a paper when authors cite a figure two million pages away?          
:blush: Here is a Python utility that **extracts images** from PDF files and provides an **interactive PyQt5-based GUI** for viewing them.       

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
python viwer.py path/to/your/file.pdf
```
Use mouse wheel to scroll or keyboard arrows.

## Keys
- **Mouse Wheel**: Scroll up/down to move between images
- **Arrow Keys**: Use Up/Down/Left/Right to navigate
- **PageUp/PageDown**: Navigate images
- **Space**: Next image
- **R**: Refresh the current image
- **T/A**: Toggle always-on-top mode
- **X**: hide/show window content
- **Home**: Go to the first image
- **End**: Go to the last image
- **Esc/Q**: Quit the application
- **H**: Show help dialog

## Use pre-extracted images (buffered mode):
```bash
python viewer.py path/to/your/file.pdf -b
```

## Use mapping between image file and figure number:
Since not all the extracted files are relevant, or there are multiple images per figure, you can map the image file to the figure number.    
For example, if Figure 1 corresponds to the second file (so you skip the first file), and Figure 3 is formed by three image files, you can create a file `maps.txt`
```
-1, 1, 2, 3, 3, 3, 4, 5, 6, 7
```
and run
```bash
python viewer.py path/to/your/file.pdf path/to/maps.txt
```


## How It Works

1. Extracts images from each PDF page into an `images/` folder
2. Saves images as `image_XXXXXX.png` with zero-padded numbering
3. Launches an interactive viewer displaying images one at a time
4. Window title shows current image number (e.g., "Fig. 1")

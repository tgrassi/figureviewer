"""PDF Image Extractor and Viewer.

This module extracts images from a PDF file and provides a PyQt5-based GUI
to view and navigate through the extracted images using mouse scroll or keyboard.
"""

from pypdf import PdfReader
from tqdm import tqdm
import os
from glob import glob
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys


# ============================================================================
# Command-line argument parsing
# ============================================================================
# Check if PDF file path is provided as first argument
if len(sys.argv) > 1:
    pdf_path = sys.argv[1]
else:
    print(f"Error: missing PDF file\nUsage: python {sys.argv[0]} <path-to-pdf-file>")
    sys.exit(1)

# Validate that the PDF file exists
if not os.path.exists(pdf_path):
    print(f"Error: PDF file '{pdf_path}' does not exist")
    sys.exit(1)

# ============================================================================
# Configuration and initialization
# ============================================================================
# Check for buffered mode flag (-b): if set, use pre-extracted images
if "-b" in sys.argv:
    use_buffered = True
    print("Using buffered images from 'images' folder")
else:
    use_buffered = False

# Load the PDF file
reader = PdfReader(pdf_path)

# ============================================================================
# Image extraction from PDF
# ============================================================================
# Extract and save images from PDF pages if not using buffered images
if not use_buffered:
    # Create images folder if it does not exist
    if not os.path.exists("images"):
        os.mkdir("images")

    # Clear existing images from folder
    for g in glob("images/*.png"):
        os.remove(g)

    # Extract images from each page in the PDF
    icount = 0
    for page in tqdm(reader.pages):
        # Extract all image objects from the current page
        for i, image_file_object in enumerate(page.images):
            # Save image with zero-padded counter in filename
            filename = f"images/image_{icount:06d}.png"
            image_file_object.image.save(filename)

            icount += 1

# ============================================================================
# PyQt5 Image Viewer
# ============================================================================
# Define the main window class for image viewing
class ImageViewer(QMainWindow):
    """PyQt5 window for viewing extracted PDF images.

    Provides navigation through images using mouse wheel scrolling or keyboard
    arrow keys (Up/Down/Left/Right).

    Attributes:
        image_files (list): Sorted list of image file paths.
        current_index (int): Index of the currently displayed image.
        label (QLabel): Label widget that displays the image.
    """

    def __init__(self, image_folder):
        """Initialize the image viewer with images from the specified folder.

        Args:
            image_folder (str): Path to folder containing PNG images.
        """
        super().__init__()
        self.setWindowTitle("PDF Image Viewer")
        self.image_files = sorted(glob(os.path.join(image_folder, "*.png")))
        self.current_index = 0

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.label)
        self.setCentralWidget(self.scroll)

        self.scroll.setWidgetResizable(True)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.alwaysOnTop = False

        self.update_image()

    def update_image(self):
        """Update the displayed image and window title based on current index."""

        if self.image_files:
            pixmap = QPixmap(self.image_files[self.current_index])
            self.label.setPixmap(pixmap.scaled(self.scroll.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            # change window title to current image file name
            self.setWindowTitle(f"PDF Image Viewer - Fig.{self.current_index + 1} / {len(self.image_files)}")

    def wheelEvent(self, event):
        """Handle mouse wheel events to navigate through images.

        Scroll up moves to previous image, scroll down moves to next image.

        Args:
            event (QWheelEvent): The wheel event object.
        """
        if event.angleDelta().y() > 0:
            self.current_index = (self.current_index - 1) % len(self.image_files)
        else:
            self.current_index = (self.current_index + 1) % len(self.image_files)
        self.update_image()

    def keyPressEvent(self, event):
        """Handle keyboard events to navigate through images.

        Right/Down arrow keys move to next image.
        Left/Up arrow keys move to previous image.

        Args:
            event (QKeyEvent): The key press event object.
        """
        if event.key() in (Qt.Key_Right, Qt.Key_Down, Qt.Key_Space, Qt.Key_PageDown):
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.update_image()
        elif event.key() in (Qt.Key_Left, Qt.Key_Up, Qt.Key_PageUp):
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.update_image()
        elif event.key() == Qt.Key_R:
            self.update_image()
        elif event.key() in (Qt.Key_T, Qt.Key_A):
            self.alwaysOnTop = not self.alwaysOnTop
            self.setWindowFlag(Qt.WindowStaysOnTopHint, self.alwaysOnTop)
            self.show()
        elif event.key() == Qt.Key_Home:
            self.current_index = 0
            self.update_image()
        elif event.key() == Qt.Key_End:
            self.current_index = len(self.image_files) - 1
            self.update_image()
        elif event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
        elif event.key() == Qt.Key_H:
            # open help dialog
            help_text = (
                "PDF Image Viewer Help:\n\n"
                "- Mouse wheel: navigate through images.\n"
                "- Left/Up arrow keys: previous image.\n"
                "- Right/Down arrow keys: next image.\n"
                "- Space/PageUp/PageDown: navigate images.\n"
                "- R: refresh the current image.\n"
                "- T/A: toggle always-on-top mode.\n"
                "- Home: go to the first image.\n"
                "- End: go to the last image.\n"
                "- Esc/Q: quit the viewer.\n"
                "- H: show this help dialog."
            )
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Help", help_text)

    def resizeEvent(self, event):
        """Handle window resize events to adjust image scaling.

        Args:
            event (QResizeEvent): The resize event object.
        """
        self.update_image()


# ============================================================================
# Main application execution
# ============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer("images")
    viewer.show()
    sys.exit(app.exec_())
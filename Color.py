from enum import Enum

def rgb(r, g, b):
    """Convert 0–255 ke 0–1 float untuk OpenGL."""
    return r / 255.0, g / 255.0, b / 255.0

class Color(Enum):
    RED     = rgb(255, 0, 0)
    GREEN   = rgb(0, 255, 0)
    BLUE    = rgb(0, 0, 255)
    ORANGE  = rgb(255, 128, 0)
    WHITE   = rgb(255, 255, 255)
    BLACK   = rgb(0, 0, 0)
    MAROON  = rgb(85, 0, 0)

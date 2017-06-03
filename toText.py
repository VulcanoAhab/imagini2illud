import re
import tldextract

import pytesseract
from PIL import Image
from PIL import ImageFilter


## process image
def process_image(imagePath, resizeTimes):
    """
    """
    #open
    image=Image.open(imagePath).copy()
    #convert to gray
    image=image.convert("L")
    #resize
    newSize=[int(s*resizeTimes) for s in image.size]
    image=image.resize(newSize, Image.ANTIALIAS)
    image.filter(ImageFilter.SHARPEN)
    text=pytesseract.image_to_string(image)
    image.close()
    return text


def process_screenShot(imagePath, resizeTimes=2.5):
    """
    """
    return process_image(imagePath, resizeTimes)

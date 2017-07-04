import re
import tldextract

import cv2
import pytesseract
from PIL import Image



## process image
def process_image(imagePath, resizeTimes):
    """
    """
    #open
    image=cv2.imread(imagePath).copy()
    #convert to gray
    grayImage=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #resize
    size=grayImage.shape[:2]
    newSize=tuple([int(s*resizeTimes) for s in size[::-1]])
    toImage=cv2.resize(grayImage, newSize)
    #read
    toTextImage=Image.fromarray(toImage)
    text=pytesseract.image_to_string(toTextImage)
    return text


def process_screenShot(imagePath, resizeTimes=2.5):
    """
    """
    return process_image(imagePath, resizeTimes)

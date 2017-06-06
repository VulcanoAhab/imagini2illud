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
    #convert to gray -> binary
    image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #ret,image2 = cv2.threshold(image,127,255,cv2.THRESH_BINARY_INV)
    #resize
    height,width=image.shape[:2]
    newSize=(width*resizeTimes, height*resizeTimes)
    image2=cv2.resize(image, newSize, interpolation=cv2.INTER_LANCZOS4)
    #read
    toTextImage=Image.fromarray(image2)
    text=pytesseract.image_to_string(toTextImage)
    return text


def process_screenShot(imagePath, resizeTimes=4):
    """
    """
    return process_image(imagePath, resizeTimes)

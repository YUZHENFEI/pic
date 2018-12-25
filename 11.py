import cv2
import PIL
import numpy as np

camera = cv2.VideoCapture(0)
width  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = width,height
print(repr(size))
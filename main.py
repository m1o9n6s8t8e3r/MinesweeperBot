import numpy as np
from PIL import Image, ImageGrab

gameCoords = [0,0,10,10]

#while True:
screen = np.array(ImageGrab.grab(bbox = None))

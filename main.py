import numpy as np
from PIL import Image, ImageGrab
import cv2
import pyautogui

pyautogui.PAUSE = .005

width = 20
height = 20

blocksize = 36

cornerX = 375
cornerY = 116

whiteColor = 208
blackColor = 0

gameCoords = [cornerX, 
              cornerY,
              cornerX + blocksize * width, 
              cornerY + blocksize * height]


def tileToScreen(x, y):
    return (cornerX + 7 + blocksize * x,
            cornerY + 7 + blocksize * y)

def getScreenString():
    s = ""
    for row in range(height):
        for col in range(width):
            screenX, screenY = tileToScreen(row, col)
            color = grayscreen[screenX - cornerX][screenY - cornerY]
            if color == whiteColor:
                s += "C"
            elif color == blackColor:
                s += "B"
            else:
                s += "N"
            screenX, screenY = tileToScreen(col, row)
            pyautogui.moveTo(screenX, screenY)
        s += "\n"
    return s

def clickClear():
    for row in range(height):
        for col in range(width):
            screenX, screenY = tileToScreen(row, col)
            color = grayscreen[screenX - cornerX][screenY - cornerY]
            if color == whiteColor:
                mouseX, mouseY = tileToScreen(col, row) #wtf, but it works
                pyautogui.moveTo(mouseX, mouseY)
                pyautogui.click(button='left')
                pyautogui.click(button='right')

while True:
    screen = np.array(ImageGrab.grab(bbox = gameCoords))
    grayscreen = np.array(cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY))
    cv2.imshow("hey", grayscreen)
    cv2.waitKey(0)
    #print("Screen")
    #print(getScreenString())
    clickClear()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

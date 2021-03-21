import numpy as np
from PIL import Image, ImageGrab
import cv2
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

pyautogui.PAUSE = .05

width = 8
height = 9

blocksize = 36

cornerX = 375 + 1
cornerY = 116 + 1

whiteColor = 208
blackColor = 0
lineColor = 153
bombColor = 108

gameCoords = [cornerX, 
              cornerY,
              cornerX + blocksize * width, 
              cornerY + blocksize * height]

def tileToScreenv0(x, y):
    return (cornerX + 7 + blocksize * x,
            cornerY + 7 + blocksize * y)

"""
def getLines(w, h):
    line_cols = []
    line_rows = []
    for row in range(h):
        for col in range(w):
            color = grayscreen[row][col]
            if color == lineColor:
                if row not in line_cols:
                    line_cols.append(row)
                if col not in line_cols:
                    line_cols.append(col)
"""

def filterImageGrid(s):
    grid = np.fromiter((x for x in s if x == lineColor), dtype=s.dtype)

def getScreenString():
    s = ""
    for row in range(height):
        for col in range(width):
            screenX, screenY = tileToScreenv0(row, col)
            color = grayscreen[screenX - cornerX][screenY - cornerY]
            if color == whiteColor:
                s += "C"
            elif color == blackColor:
                s += "B"
            else:
                s += "N"
            screenX, screenY = tileToScreenv0(col, row)
            pyautogui.moveTo(screenX, screenY)
        s += "\n"
    return s

def clickClear():
    for row in range(height):
        for col in range(width):
            screenX, screenY = tileToScreenv0(row, col)
            color = grayscreen[screenX - cornerX][screenY - cornerY]
            if color == whiteColor:
                mouseX, mouseY = tileToScreenv0(col, row) #wtf, but it works
                pyautogui.moveTo(mouseX, mouseY)
                pyautogui.click(button='left')
                pyautogui.click(button='right')

def lineComp(x):
    if (x == 153):
        return 153
    else:
        return 0

lineCompV = np.vectorize(lineComp)

while True:
    screen = np.array(ImageGrab.grab(bbox = gameCoords))
    grayscreen = np.array(cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY))
    #print(grayscreen)
    grid = (grayscreen == lineColor).astype(np.uint8)
    vertical_lines = [0]
    for i in range(blocksize * width):
        if (grid[0][i] == 1):
            vertical_lines.append(i)
    horizontal_lines = [0]
    for j in range(blocksize * height):
        if (grid[j][0] == 1):
            horizontal_lines.append(j)
    print(vertical_lines)
    print(horizontal_lines)
    
    cv2.imshow("hey", grayscreen)
    cv2.waitKey(0)
    #Printing Gird
    #grid = (grid * 153)
    #print(grayscreen)
    #print(grid)
    #cv2.imshow("grid", grid)
    print(width, len(vertical_lines))
    print(height, len(horizontal_lines))
    cong = r'--oem 3 --psm 10 outputbase digits'
    s = ""
    for j in range(height):
        for i in range(width):
            screenX = vertical_lines[i] + 1
            screenY = horizontal_lines[j] + 1
            color = grayscreen[screenY][screenX]
            if color == whiteColor:
                #s += "C"
                digit_image = np.array(grayscreen[screenY:screenY+blocksize, screenX:screenX+blocksize])
                cv2.imshow("4row5col", digit_image)
                #data = pytesseract.image_to_data(digit_image, config=cong)
                badumtss = pytesseract.image_to_string(digit_image, config=cong)
                #print(data)
                try: 
                    digit = int(badumtss)
                    s += str(digit)
                except:
                    s += "C"

            elif color == blackColor:
                s += "B"
            else:
                s += "N"
        s += "\n"
    print(s)
    #print("Screen")
    #print(getScreenString())
    #clickClear()
    cv2.waitKey(0)
    cv2.destroyAllWindows()

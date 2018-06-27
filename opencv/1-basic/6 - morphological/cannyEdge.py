import cv2
import numpy as np
from matplotlib import pyplot as plt

def recalculateEdges(x):
    maxValue = cv2.getTrackbarPos('ValorMáximo','window')
    minValue = cv2.getTrackbarPos('ValorMínimo','window')
    edges = cv2.Canny(img,minValue,maxValue)
    print(minValue, maxValue)
    cv2.imshow('window',edges)
    pass


img = cv2.imread('familia.jpg',0)
cv2.namedWindow('window', cv2.WINDOW_NORMAL)
cv2.resizeWindow('window', 600, 600)
edges = cv2.Canny(img,100,200)


# create trackbars for color change
cv2.createTrackbar('ValorMáximo','window',200
,600,recalculateEdges)
cv2.createTrackbar('ValorMínimo','window',100,600,recalculateEdges)

cv2.imshow('window',edges)

while(1):
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

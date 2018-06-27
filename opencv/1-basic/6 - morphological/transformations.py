import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('whiteLine.jpg',0)


kernel = np.ones((5,5),np.uint8)

erosion = cv2.erode(img,kernel,iterations = 1)
dilation = cv2.dilate(img,kernel,iterations = 1)
gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)
tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)
blackhat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)

while(1):
    cv2.imshow('blackhat',blackhat)
    cv2.imshow('tophat',tophat)
    cv2.imshow('gradient',gradient)
    cv2.imshow('dilation',dilation)
    cv2.imshow('erosion',erosion)
    cv2.imshow('ORIGINAL',img)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

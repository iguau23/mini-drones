import numpy as np
import cv2
from matplotlib import pyplot as plt

im = cv2.imread('psy.jpg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
cv2.imwrite('thresh.jpg', thresh)

image, contours, hierarchy = cv2.findContours(thresh,
                                cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

image = cv2.drawContours(im, contours, -1, (0,255,0), 1)
cv2.imwrite('contours.jpg', image)
image = image[:,:,::-1]
plt.imshow(image)

cnt = contours[0]
M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print ("o centroide é: ", cx, cy)

area = cv2.contourArea(cnt)
print("a área é: ", area)

perimeter = cv2.arcLength(cnt,True)
print("o perímetro é: ", perimeter)

#contour approximation
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)
hull = cv2.convexHull(cnt)

k = cv2.isContourConvex(cnt)
print("a curva é convexa: ", k)

plt.show()

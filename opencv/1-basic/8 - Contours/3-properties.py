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
cnt = contours[0]


#Aspect ratio
x,y,w,h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h
print("ratio is: ", aspect_ratio)

#extent
area = cv2.contourArea(cnt)
x,y,w,h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area
print("extent is: ", extent)

#solidity
area = cv2.contourArea(cnt)
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area
print("solidity is: ", solidity)

#equivalent Diameter
area = cv2.contourArea(cnt)
equi_diameter = np.sqrt(4*area/np.pi)
print("equivalent Diameter is: ", equi_diameter)

#orientation
(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)
print("angle is: ", angle)

#mask and pixel points
mask = np.zeros(imgray.shape,np.uint8)
cv2.drawContours(mask,[cnt],0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))

#max value and min value
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray,mask = mask)
print("minimun value is: ", min_val, "in: ", min_loc)
print("maximum value is: ", max_val, "in: ", max_loc)

#mean color
mean_val = cv2.mean(im, mask=mask)
print("mean value is: ", mean_val)

#extreme points
leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
rightmost = tuple(cnt[cnt[:,:,0].argmax()][0])
topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
image = cv2.circle(image, leftmost, 3, (0,0,255), -1)
image = cv2.circle(image, rightmost, 3, (0,0,255), -1)
image = cv2.circle(image, topmost, 3, (0,0,255), -1)
image = cv2.circle(image, bottommost, 3, (0,0,255), -1)


cv2.imwrite('contours.jpg', image)
image = image[:,:,::-1]
plt.imshow(image)

plt.show()

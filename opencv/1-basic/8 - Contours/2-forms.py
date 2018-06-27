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

#bounding Rect
x,y,w,h = cv2.boundingRect(cnt)
image = cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)

#rotated rect
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(im,[box],0,(0,0,255),2)

#enclosing circle
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
image = cv2.circle(image,center,radius,(255,0,0),2)


#Ellipse
ellipse = cv2.fitEllipse(cnt)
im = cv2.ellipse(im,ellipse,(0,255,255),2)

#line
rows,cols = image.shape[:2]
[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
image = cv2.line(image,(cols-1,righty),(0,lefty),(0,255,0),2)



cv2.imwrite('contours.jpg', image)
image = image[:,:,::-1]
plt.imshow(image)

plt.show()

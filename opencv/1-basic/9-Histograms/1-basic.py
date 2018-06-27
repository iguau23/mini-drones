import cv2
import numpy as np, sys
from matplotlib import pyplot as plt

img = cv2.imread('yukari.jpg')
img = img[:,:,::-1]
color = ('r','g','b')
plt.subplot(2, 1, 1)
plt.imshow(img)

plt.subplot(2, 1, 2)
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])
plt.show()


cv2.waitKey(0)
cv2.destroyAllWindows()

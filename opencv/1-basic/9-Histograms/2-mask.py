import cv2
import numpy as np, sys
from matplotlib import pyplot as plt

img = cv2.imread('yukari.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)



# create a mask
mask = np.zeros(img_gray.shape[:2], np.uint8)
mask[1200:2300, 0:2000] = 255
masked_img = cv2.bitwise_and(img_gray,img_gray,mask = mask)

# Calculate histogram with mask and without mask
# Check third argument for mask
hist_full = cv2.calcHist([img_gray],[0],None,[256],[0,256])
hist_mask = cv2.calcHist([img_gray],[0],mask,[256],[0,256])

plt.subplot(221), plt.imshow(img_gray, 'gray')
plt.subplot(222), plt.imshow(mask,'gray')
plt.subplot(223), plt.imshow(masked_img, 'gray')
plt.subplot(224), plt.plot(hist_full), plt.plot(hist_mask)
plt.xlim([0,256])

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

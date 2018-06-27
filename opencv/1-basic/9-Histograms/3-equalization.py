import cv2
import numpy as np
from matplotlib import pyplot as plt
'''
img = cv2.imread('neblina.jpg', 0)

hist,bins = np.histogram(img.flatten(),256,[0,256])

cdf = hist.cumsum()
cdf_normalized = cdf * hist.max()/ cdf.max()

plt.plot(cdf_normalized, color = 'b')
plt.hist(img.flatten(),256,[0,256], color = 'r')
plt.xlim([0,256])
plt.legend(('cdf','histogram'), loc = 'upper left')
plt.show()



equ = cv2.equalizeHist(img)
res = np.hstack((img, equ))
plt.imshow(res, 'gray')
plt.show()
'''

#equalize color
img_color = cv2.imread('yukari.jpg')
img_yuv = cv2.cvtColor(img_color, cv2.COLOR_BGR2YUV)

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
#img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

plt.subplot(2,1,2)
hist = cv2.calcHist([img_yuv[:,:,0]],[0],None,[256],[0,256])
plt.plot(hist)
plt.xlim([0,256])

plt.subplot(2,1,1)
img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

img_color = img_color[:,:,::-1]
img_output = img_output[:,:,::-1]
res = np.hstack((img_color, img_output))
plt.imshow(res)
plt.show()

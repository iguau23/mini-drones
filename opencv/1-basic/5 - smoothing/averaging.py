import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('scopus.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


dst = cv2.blur(img, (10,10))

plt.subplot(121),plt.imshow(img),plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(dst),plt.title('blurred')
plt.xticks([]), plt.yticks([])
plt.show()

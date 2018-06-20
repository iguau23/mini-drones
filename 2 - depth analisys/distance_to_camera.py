# import the necessary packages
import numpy as np
import cv2
from matplotlib import pyplot as plt
from feature_matching_sift import find_marker

def distance_to_camera(knowWidth, focalLength, perWidth):
    distance = (knowWidth*focalLength)/perWidth
    return distance

KNOW_DISTANCE = 45
KNOWN_WIDTH = 21

knowImage = cv2.imread('data/45.jpg') # trainImage
dst, img2 = find_marker(knowImage)
plt.imshow(img2, 'gray'), plt.show()

#camera Calibration
perWidth = dst[3][0][0]-dst[0][0][0]
focalLength = (perWidth*KNOW_DISTANCE)/KNOWN_WIDTH

#compute distance
img = cv2.imread('data/70.jpg')
dst, img2 = find_marker(img)
perWidth = dst[3][0][0]-dst[0][0][0]
distance = distance_to_camera(KNOWN_WIDTH, focalLength,perWidth)

font = cv2.FONT_HERSHEY_SIMPLEX
print(distance)
text = ("%.2fcm" %distance)
cv2.putText(img2,text,(img2.shape[1] - 300, img2.shape[0] - 30),
font, 2,(255,255,255),2,cv2.LINE_AA)

plt.imshow(img2, 'gray'), plt.show()

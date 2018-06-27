import cv2
import numpy as np, sys

apple = cv2.imread('apple.jpg')
orange = cv2.imread('orange.jpg')

#generate guassian pyramid
gaussian = apple.copy()
gpA = [gaussian]
for i in range(6):
    gaussian = cv2.pyrDown(gaussian)
    gpA.append(gaussian)

gaussian = orange.copy()
gpB = [gaussian]
for i in range(6):
    gaussian = cv2.pyrDown(gaussian)
    gpB.append(gaussian)



lpA = [gpA[5]]
for i in range(5,0,-1):
    GE = cv2.pyrUp(gpA[i])
    cv2.imwrite('gpAi-1.jpg', gpA[i -1])
    cv2.imwrite('GE.jpg', GE)
    L = cv2.subtract(gpA[i-1], GE)
    lpA.append(L)



lpB = [gpB[5]]
for i in range(5,0,-1):
    GE = cv2.pyrUp(gpB[i])
    L = cv2.subtract(gpB[i-1],GE)
    lpB.append(L)



LS = []
for la, lb in zip(lpA, lpB):
    rows, cols, dpt = la.shape
    ls = np.hstack((la[:,0:cols/2], lb[:, cols/2:]))
    LS.append(ls)

for i in range(0,6):
    cv2.imwrite('LS-%d.jpg' %i, LS[i])

ls_ = LS[0]
for i in range(1,6):
    ls_ = cv2.pyrUp(ls_)
    cv2.imwrite('ls_%d.jpg' %i, ls_)
    ls_ = cv2.add(ls_, LS[i])


# image with direct connecting each half
real = np.hstack((apple[:,:cols/2],orange[:,cols/2:]))

cv2.imwrite('Pyramid_blending2.jpg',ls_)
cv2.imwrite('Direct_blending.jpg',real)

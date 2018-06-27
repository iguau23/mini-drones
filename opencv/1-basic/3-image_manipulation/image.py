import cv2
import numpy as np

familia = cv2.imread('familia.jpg')
familiaGray = cv2.cvtColor(familia, cv2.COLOR_BGR2GRAY)
rows,cols, ch = familia.shape

#Scaling
scaled = cv2.resize(familia,None,fx=2, fy=2, interpolation = cv2.INTER_LINEAR)

cv2.imwrite('scaled.jpg', scaled)


#TRanslation
M = np.float32([[1,0,500],[0,1,0]])
translated = cv2.warpAffine(familiaGray, M, (cols, rows))
cv2.imwrite('translated.jpg', translated)

#Rotation
M2 = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
rotated = cv2.warpAffine(familiaGray, M2, (cols, rows))
cv2.imwrite('rotated.jpg', rotated)

#Affine
pts1 = np.float32([[100,100],[400,100],[100,400]])
pts2 = np.float32([[20,200],[400,100],[200,500]])
M3 = cv2.getAffineTransform(pts1,pts2)
affined = cv2.warpAffine(familia,M3,(cols,rows))
cv2.imwrite('affinedTransformation.jpg', affined)

#Perspective
pts1 = np.float32([[56,65],[1500,52],[28,2000],[1500,2000]])
pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])
M4 = cv2.getPerspectiveTransform(pts1,pts2)
perspectived = cv2.warpPerspective(familia,M4,(300,300))
cv2.imwrite('perspectived.jpg', perspectived)

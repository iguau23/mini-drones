import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('psy.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255,0)
image, contours,hierarchy = cv2.findContours(thresh,2,1)
cnt = contours[0]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)


for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,5,[0,0,255],-1)




#Point polygon test
pontos = [(0,0), (50,50), (120,120), (200,200)]
for i in range(4):
    dist = cv2.pointPolygonTest(cnt, pontos[i], True)
    print("O ponto %d %d está a distancia: %d" %(pontos[i][0], pontos[i][1], dist))



img = img[:,:,::-1]
plt.imshow(img)

plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()

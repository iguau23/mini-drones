import numpy as np
import cv2
import glob

with np.load('camera_array.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

img = cv2.imread('data/40.jpg')
h,  w = img.shape[:2]
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

x, y, w, h = roi
#dst = dst[y:y+h, x:x+w]
cv2.imwrite('data/calibresult.jpg', dst)

import numpy as np
import cv2
from matplotlib import pyplot as plt


def calibrateImagem(img):
    '''
    Recebe a imagem, e calibra ele de acordo com os parametros
    presentes em camera_array.npz. retorna a Imagem cortada
    '''
    with np.load('camera_array.npz') as X:
        mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    h,  w = img.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    #plt.imshow(dst, 'gray'), plt.show()
    return dst

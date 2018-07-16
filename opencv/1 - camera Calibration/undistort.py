import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt

# You should replace these 3 lines with the output in calibration step


def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    with np.load('camera_array_fisheye.npz') as X:
            mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
    DIM=(640,480)
    K=mtx
    D=dist
    images = glob.glob('./data/foto??.jpg')
    for p in images:
        undistort(p)

import numpy as np
import cv2
from matplotlib import pyplot as plt
FLANN_INDEX_LSH = 6
MIN_MATCH_COUNT = 10


img1 = cv2.imread('box.png',0)          # queryImage
img2 = cv2.imread('box_in_scene.png',0) # trainImage

# # Initiate SIFT detector
# orb = cv2.ORB_create()
#
# # find the keypoints and descriptors with SIFT
# kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)

fast = cv2.FastFeatureDetector_create()
kp1 = fast.detect(img1,None)
#img1 = cv2.drawKeypoints(img1, kp1,None, color=(255,0,0))
brief = cv2.xfeatures2d.BriefDescriptorExtractor_create()
kp1,des1= brief.compute(img1,kp1)
kp2 = fast.detect(img2, None)
#img2 = cv2.drawKeypoints(img2, kp2,None, color=(255,0,0))
kp2, des2 = brief.compute(img2,kp2)
plt.imshow(img2, 'gray'),plt.show()

# FLANN parameters
FLANN_INDEX_KDTREE = 0
index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 12, # 12
                   key_size = 20,     # 20
                   multi_probe_level = 2) #2
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)


matches = flann.knnMatch(des1,des2,k=2)


# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.9*n.distance:
        good.append(m)

if len(matches)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print ("Not enough matches are found - %d / %d" %(len(matches),MIN_MATCH_COUNT))
    matchesMask = None

draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3, 'gray'),plt.show()

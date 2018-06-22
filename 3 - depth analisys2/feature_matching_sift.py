import numpy as np
import cv2
from matplotlib import pyplot as plt
FLANN_INDEX_LSH = 6
MIN_MATCH_COUNT = 5


'''
    Encontra o marcador definido no template, e devolve
    as coordenadas dos quatro pontos do marcador
    e a imagem com o marcador
    ->(dst, imagem)
'''
def find_marker(image, template):
    img1 = template         # queryImage
    img2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #trainIMage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    if(des1 is None or des2 is None):
        return None, image


    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    flann = cv2.FlannBasedMatcher(index_params,search_params)


    matches = flann.knnMatch(des1,des2,k=2)


    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
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

        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
        	           singlePointColor = None,
        	           matchesMask = matchesMask, # draw only inliers
        	           flags = 2)

        img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)


        #print(dst[0][0][0], dst[0][0][1])
        #print(dst[1][0][0], dst[1][0][1])
        #print(dst[2][0][0], dst[2][0][1])
        #print(dst[3][0][0], dst[3][0][1])
        #plt.imshow(img2, 'gray'),plt.show()
        return dst, img2

    else:
        print ("Not enough matches are found - %d / %d" %(len(matches),MIN_MATCH_COUNT))
        matchesMask = None
        return None, image



'''
img2 = cv2.imread('30.jpg') # trainImage
_, img2 = find_marker(img2)
plt.imshow(img2, 'gray'), plt.show()'''

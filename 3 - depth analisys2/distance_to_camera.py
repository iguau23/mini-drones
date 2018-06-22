# import the necessary packages
import numpy as np
import cv2
from matplotlib import pyplot as plt
from feature_matching_sift import find_marker
from undistort import calibrateImagem

class DistanceCalculator():
    def __init__(self):
        self.KNOW_DISTANCE = 30
        self.KNOWN_WIDTH = 21
        self.KNOW_Y = 0

        self.distance_x = 0
        self.distance_y = 0

        self.template = cv2.imread('data/board.jpg', 0)

        knowImage = cv2.imread('data/0-30.jpg') # trainImage
        knowImage = calibrateImagem(knowImage)
        dst, img2 = find_marker(knowImage, self.template)
        #plt.imshow(img2, 'gray'), plt.show()

        #camera Setting
        perWidth = dst[3][0][0]-dst[0][0][0]
        self.focalLength = (perWidth*self.KNOW_DISTANCE)/self.KNOWN_WIDTH
        self.center = (dst[3][0][0]+dst[0][0][0])/2

    def distance_to_camera(self,knowWidth, focalLength, perWidth):
        distance = (knowWidth*focalLength)/perWidth
        return distance

    def calculateDistance(self, img):
        img = calibrateImagem(img)

        #compute distance
        dst, img2 = find_marker(img, self.template)
        if(dst is not None):
            perWidth = dst[3][0][0]-dst[0][0][0]
            self.distance_x = self.distance_to_camera(self.KNOWN_WIDTH, self.focalLength,perWidth)

            resolucao = perWidth/self.KNOWN_WIDTH
            newCenter = (dst[3][0][0]+dst[0][0][0])/2
            self.distance_y = (newCenter-self.center)/resolucao

        return self.distance_x, self.distance_y


    def writeDistance(img, distance_x, distance_y):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = ("distancia = %.2fcm" %distance_x)
        text2 = ("y = %.2fcm" %distance_y)
        cv2.putText(img,text,(img.shape[1] - 200, img.shape[0] - 30),
                    font, 0.5,(0,0,0),2,cv2.LINE_AA)
        cv2.putText(img,text2,(img.shape[1] - 200, img.shape[0] - 15),
                    font, 0.5,(0,0,0),2,cv2.LINE_AA)


if __name__ == '__main__':
    calculator = DistanceCalculator()

    img = cv2.imread('data/30g-10-30.jpg')
    distance_x, distance_y = calculator.calculateDistance(img)
    DistanceCalculator.writeDistance(img, distance_x, distance_y)
    plt.imshow(img, 'gray'), plt.show()

import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
from distance_to_camera import DistanceCalculator


calculator = DistanceCalculator()
cap = cv2.VideoCapture('data/video.webm')

cont = 0
while(cap.isOpened()):
    ret, frame = cap.read()

    if(frame is None):
        break
        
    if(cont%50==0):
        distance_x, distance_y = calculator.calculateDistance(frame)

    DistanceCalculator.writeDistance(frame, distance_x, distance_y)
    cv2.imshow('frame',frame)

    cont += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

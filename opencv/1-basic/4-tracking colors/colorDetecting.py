import cv2
import numpy as np

redValue = 111
greenValue = 111
blueValue = 111




def pixelShow(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        blueValue = blue[x,y,0]
        greenValue = blue[x,y,1]
        redValue = blue[x,y,2]
        text = "RED: "+str(redValue)+" BLUE: "+str(blueValue)+ " GREEN: "+str(greenValue)
        cv2.putText(blue, text, (200,25), font, 0.5, (0,0,0), 1, cv2.LINE_AA )

blue = cv2.imread('rosto.jpg')
cv2.namedWindow('image')
cv2.setMouseCallback('image', pixelShow)



while(1):
    cv2.imshow('image',blue)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break


    font = cv2.FONT_HERSHEY_SIMPLEX



cv2.destroyAllWindows()

import numpy as np
import cv2
from matplotlib import pyplot as plt

selection = None
drag_start = None
show_backproj = False
track_window = None

def show_hist(hist):
    bin_count = hist.shape[0]
    bin_w = 24
    img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
    for i in range(bin_count):
        h = int(hist[i])
        cv2.rectangle(img, (i*bin_w +2, 255), ((i+1)*bin_w-2, 255-h),
        (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

def onMouse(event, x, y, flags, param):
    global selection
    global drag_start
    global show_backproj
    global track_window
    if event == cv2.EVENT_LBUTTONDOWN:
        drag_start = (x,y)
        track_window = None
    if drag_start != None:
        xmin = min(x, drag_start[0])
        ymin = min(y, drag_start[1])
        xmax = max(x, drag_start[0])
        ymax = max(y, drag_start[1])
        selection = (xmin, ymin, xmax, ymax)

    if event == cv2.EVENT_LBUTTONUP:
        drag_start = None
        track_window = (xmin, ymin, xmax-xmin, ymax-ymin)
        print(track_window)

cap = cv2.VideoCapture(0)

while(1):
    ret ,frame = cap.read()
    img2 = frame.copy()

    cv2.namedWindow('camshift')
    cv2.setMouseCallback('camshift', onMouse)


    if track_window and track_window[2] > 0 and track_window[3] >0:
        if selection:
            # set up the ROI for tracking
            roi = frame[track_window[1]:track_window[1]+track_window[3],
                        track_window[0]:track_window[0]+track_window[2]]
            cv2.imwrite('roi.jpg', roi)
            hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
            roi_hist = cv2.calcHist([hsv_roi],[0],mask,[16],[0,180])
            cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)
            show_hist(roi_hist)

            selection = None


        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )


        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

        # apply meanshift to get the new location
        ret, track_window = cv2.CamShift(dst, track_window, term_crit)

        # Draw it on image
        pts = cv2.boxPoints(ret)
        pts = np.int0(pts)
        img2 = cv2.polylines(frame, [pts], True, 255, 2)

    cv2.imshow('camshift',img2)
    k = cv2.waitKey(60) & 0xff
    if k == 27:
        break
    else:
        cv2.imwrite(chr(k)+".jpg",img2)

cv2.destroyAllWindows()
cap.release()

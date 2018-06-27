import  cv2
import numpy as np

familia = cv2.imread('familia.jpg')
scopusLogo = cv2.imread('scopus.jpeg')

rows, cols, channels = scopusLogo.shape
roi = familia[0:rows, 0:cols]

scopusLogoGray = cv2.cvtColor(scopusLogo, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(scopusLogoGray, 180, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

cv2.imwrite('0_scopusLogoGray.png', scopusLogoGray)
cv2.imwrite('1_scopusMask.png', mask)
cv2.imwrite('2_scopusMaskInv.png', mask_inv)

roiBlackedOut = cv2.bitwise_and(roi, roi, mask = mask)
scopusLogoPuro = cv2.bitwise_and(scopusLogo, scopusLogo, mask = mask_inv)

cv2.imwrite('3_roiBlackedOut.png', roiBlackedOut)
cv2.imwrite('4_scopusLogoPuro.png', scopusLogoPuro)

roiFinal = cv2.add(roiBlackedOut, scopusLogoPuro)
familia[0:rows, 0:cols] = roiFinal

cv2.imwrite('5_roi.png', roiFinal)
cv2.imwrite('6_familiaFInal.png', familia)

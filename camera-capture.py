import cv2

cam = cv2.VideoCapture(0)
s, im = cam.read() # captures image
cv2.imshow("Test Picture", im) # displays captured image
cv2.waitKey(0)
cv2.destroyAllWindows()

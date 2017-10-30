# Standard imports
import cv2
import numpy as np;
 
# Read image
cam = cv2.VideoCapture(0)
s, im = cam.read()
cv2.imwrite("blob.png",im)
im = cv2.imread("blob.png", cv2.IMREAD_GRAYSCALE)

params = cv2.SimpleBlobDetector_Params()

# Filter by color
params.filterByColor = True
params.blobColor = 0

### Change thresholds
##params.minThreshold = 10;
##params.maxThreshold = 200;
## 
### Filter by Area.
##params.filterByArea = True
##params.minArea = 1500
## 
### Filter by Circularity
##params.filterByCircularity = True
##params.minCircularity = 0.1
## 
### Filter by Convexity
##params.filterByConvexity = True
##params.minConvexity = 0.87
## 
### Filter by Inertia
##params.filterByInertia = True
##params.minInertiaRatio = 0.01
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)
 
# Detect blobs.
keypoints = detector.detect(im)

for kp in keypoints:
    print kp.pt

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
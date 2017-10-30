from recognition import corners
import cv2
from time import time

def getFrame(debug=False):
    cam = cv2.VideoCapture(0)
    s, im = cam.read() # captures image
    if debug:
        cv2.imshow("Test Picture", im) # displays captured image
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imwrite("test.png",im)
    corners('test.png', debug=debug)
    #corners('../test-images/messy-scene-color.png')

t0 = time()
getFrame()
t1 = time()
print 'function vers1 takes %f' %(t1-t0)
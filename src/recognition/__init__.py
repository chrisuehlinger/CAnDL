from corners import corners
import cv2

def getFrame(debug=False):
    cam = cv2.VideoCapture(0)
    s, im = cam.read() # captures image
    if debug:
        cv2.imshow("Test Picture", im) # displays captured image
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    cv2.imwrite("test.png",im)
    return corners('test.png', debug=debug)
    #corners('../test-images/messy-scene-color.png')

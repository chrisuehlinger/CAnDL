import cv2
from recognition import getFrame, getPrecapturedFrame
from twisted.internet import task
from twisted.internet import reactor
from server import serve

projector, capture = serve(reactor)

class Engine():
    def runEverySecond():
        print "a second has passed"
        frame = getFrame(debug=True)
        print frame
        projector.sendNewState(frame)

    def captureImage(self):
        print 'Capturing...'
        capture.captureImage()

    def receiveImage(self, image):
      cv2.imwrite("test.png",image)
      frame = getPrecapturedFrame(debug=True)
      print frame
      projector.sendNewState(frame)

      reactor.callLater(0.1, self.captureImage)

engine = Engine()
# l = task.LoopingCall(engine.runEverySecond)
# l.start(0.1) # call every second
# l.stop() will stop the looping calls

capture.registerReceiver(engine)
reactor.callLater(10.0, engine.captureImage)
reactor.run()

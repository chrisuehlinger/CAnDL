from recognition import getFrame
from twisted.internet import task
from twisted.internet import reactor
from server import serve

factory = serve(reactor)

def runEverySecond():
    print "a second has passed"
    frame = getFrame(debug=False)
    print frame
    factory.sendNewState(frame)

l = task.LoopingCall(runEverySecond)
l.start(0.1) # call every second

# l.stop() will stop the looping calls
reactor.run()

from recognition import getFrame
from twisted.internet import task
from twisted.internet import reactor

def runEverySecond():
    print "a second has passed"
    try:
        print getFrame(debug=False)
    except:
        e = sys.exc_info()[0]
        print "Error: " + e

l = task.LoopingCall(runEverySecond)
l.start(0.1) # call every second

# l.stop() will stop the looping calls
reactor.run()
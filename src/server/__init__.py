import sys
import random

from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site

from autobahn.twisted.resource import WebSocketResource

from projector import setup as projectorSetup
from capture import setup as captureSetup

def serve(reactor):
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File(".")

    # websockets resource on "/projector-socket" path
    projectorFactory = projectorSetup()
    projectorSocket = WebSocketResource(projectorFactory)
    root.putChild(u"projector-socket", projectorSocket)

    # websockets resource on "/capture-socket" path
    captureFactory = captureSetup()
    captureSocket = WebSocketResource(captureFactory)
    root.putChild(u"capture-socket", captureSocket)

    site = Site(root)
    reactor.listenTCP(8080, site)
    return (projectorFactory, captureFactory)

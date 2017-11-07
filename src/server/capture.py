from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
import cv2
import numpy as np

def data_uri_to_cv2_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img

class SomeServerProtocol(WebSocketServerProtocol):
    def onOpen(self):
        """
        Connection from client is opened. Fires after opening
        websockets handshake has been completed and we can send
        and receive messages.

        Register client in factory, so that it is able to track it.
        Try to find conversation partner for this client.
        """
        self.factory.register(self)

    def connectionLost(self, reason):
        """
        Client lost connection, either disconnected or some error.
        Remove client from list of tracked connections.
        """
        self.factory.unregister(self)

    def onMessage(self, payload, isBinary):
        """
        Message sent from client, communicate this message to its conversation partner,
        """
        self.factory.receiveImage(payload)



class CaptureFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(CaptureFactory, self).__init__(*args, **kwargs)
        self.clients = {}

    def registerReceiver(self, receiver):
        self.receiver = receiver

    def register(self, client):
        """
        Add client to list of managed connections.
        """
        self.clients[client.peer] = {"object": client, "partner": None}

    def unregister(self, client):
        """
        Remove client from list of managed connections.
        """
        self.clients.pop(client.peer)

    def receiveImage(self, payload):
        """
        Receive an image from a client
        """
        if self.receiver is not None:
            image = data_uri_to_cv2_img(payload)
            self.receiver.receiveImage(image)

    def captureImage(self):
      for peer, client in self.clients.iteritems():
        client["object"].sendMessage("capture")

def setup():
  factory = CaptureFactory(u"ws://127.0.0.1:8080")
  factory.protocol = SomeServerProtocol
  return factory

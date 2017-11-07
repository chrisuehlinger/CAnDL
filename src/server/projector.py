import json
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol

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
        self.factory.communicate(self, payload, isBinary)



class ProjectorFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(ProjectorFactory, self).__init__(*args, **kwargs)
        self.clients = {}

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

    def communicate(self, client, payload, isBinary):
        """
        Broker message from client to its partner.
        """
        c = self.clients[client.peer]
        if not c["partner"]:
            c["object"].sendMessage("Sorry you dont have partner yet, check back in a minute")
        else:
            c["partner"].sendMessage(payload)

    def sendNewState(self, payload):
      for peer, client in self.clients.iteritems():
        client["object"].sendMessage(json.dumps(payload))

def setup():
  factory = ProjectorFactory(u"ws://127.0.0.1:8080")
  factory.protocol = SomeServerProtocol
  return factory

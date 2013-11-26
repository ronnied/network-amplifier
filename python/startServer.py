from amplifier.controllerServer import ControllerServer
from twisted.internet import reactor
from twisted.web.server import Site

# Run the Network Amplifier Web Server and Controller
reactor.listenTCP(8241, Site(ControllerServer()))
reactor.run()

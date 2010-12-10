import socket
import threading
import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from Registry import Registry


class RegistryRPCServer(threading.Thread):
  """An RPC Server built to work closely with the Registry
     This server is meant to be inherited, as it has no actual functionality
     
     Derived classes should simply call __init__, and then register their functions
     To stop the server, self.die should be set to True

     The following members will automatically be set during __init__:
       self.server is the RPCServer member
       self.name is the name of the server, which may be different then the name passed in
       self.port is the port that the server is running on
       self.die is set to false
  """
  def __init__(self, name):
    try:
      # Connect to Registry
      registry = xmlrpclib.ServerProxy("http://localhost:%d" % Registry.SERVER_PORT)
      # Request a port
      for i in range(3):
        port = registry.request_port()
        if port == Registry.RET_NO_PORT:
          raise Exception("No available ports")
        # Start our server
        self.server = None
        try:
          self.server = SimpleXMLRPCServer(("localhost", port),
                                            requestHandler=SimpleXMLRPCRequestHandler)
          self.server.register_introspection_functions()
          break
        except socket.error, e:
          print "Couldn't start on port %d" % port
        
      if self.server is None:
        raise Exception("To many bad port retries")

      # Successfully started our server, register ourselves
      ret = None
      for i in range(3):
        ret = registry.register(name, port)
        if ret == Registry.RET_NAME_EXISTS:
          name = name + "*"
        elif ret == Registry.RET_PORT_EXISTS:
          raise Exception("Couldn't register port")
        elif ret == Registry.RET_OK:
          break
        else:
          raise Exception("Unexpected return code on register")

      if ret != Registry.RET_OK:
        raise Exception("Too many registry retries")


      # Successfully started and registered
      print "Started server %s on port %d" % (name, port)
      self.name = name
      self.port = port
      self.die = False
      threading.Thread.__init__(self)

    except socket.error, e:
      raise Exception("Could not connect to registry on start up")

  def run(self):
    while not self.die:
      self.server.handle_request()

    # Cleanup
    self.server.server_close()
    try:
      # Connect to Registry
      registry = xmlrpclib.ServerProxy("http://localhost:%d" % Registry.SERVER_PORT)
      ret = registry.unregister(self.name, self.port)
      if ret == Registry.RET_OK:
        print "Successfully unregistered"
      elif ret == Registry.RET_BAD:
        print "Could not unregister properly"
    except socket.error, e:
      raise Exception("Could not connect to registry on shut down")

import logging
import socket
import threading
import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from Registry import Registry, SilentRequestHandler


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
    if not hasattr(self, 'log'):
      self.log = logging.getlogger("RPC")

    try:
      # Connect to Registry
      registry = xmlrpclib.ServerProxy("http://localhost:%d" % Registry.SERVER_PORT)
      # Request a port
      for i in range(3):
        port = registry.request_port()
        if port == Registry.RET_NO_PORT:
          self.log.error("No available ports")
          raise Exception("No available ports")
        # Start our server
        self.server = None
        try:
          self.server = SimpleXMLRPCServer(("localhost", port),
                                            requestHandler=SilentRequestHandler)
          self.server.register_introspection_functions()
          break
        except socket.error, e:
          self.log.warning("Couldn't start on port %d" % port)
        
      if self.server is None:
        self.log.error("Too many bad port retries")
        raise Exception("Too many bad port retries")

      # Successfully started our server, register ourselves
      ret = None
      for i in range(3):
        ret = registry.register(name, port)
        if ret == Registry.RET_NAME_EXISTS:
          name = name + "*"
        elif ret == Registry.RET_PORT_EXISTS:
          self.log.error("Couldn't register port")
          raise Exception("Couldn't register port")
        elif ret == Registry.RET_OK:
          break
        else:
          self.log.error("Unexpected return code on register")
          raise Exception("Unexpected return code on register")

      if ret != Registry.RET_OK:
        self.log.error("Too many registry retries")
        raise Exception("Too many registry retries")


      # Successfully started and registered
      self.log.info("Started server %s on port %d" % (name, port))
      self.name = name
      self.port = port
      self.die = False
      threading.Thread.__init__(self)

    except socket.error, e:
      self.log.error("Could not connect to registry on start up")
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
        self.log.info("Successfully unregistered")
      elif ret == Registry.RET_BAD:
        self.log.warning("Could not unregister properly")
    except socket.error, e:
      self.log.error("Could not connect to registry on shut down")
      raise Exception("Could not connect to registry on shut down")

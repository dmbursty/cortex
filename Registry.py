import threading
import xmlrpclib

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

from common import synchronize

class Registry(threading.Thread):
  SERVER_PORT = 9047
  CLIENT_PORT_START = 9027
  CLIENT_PORT_END = 9030

  # Define return codes
  RET_OK, RET_BAD, RET_NO_PORT, RET_NAME_EXISTS, RET_PORT_EXISTS = range(5)

  def __init__(self):
    self.mutex = threading.Lock()
    self.die = False
    self.clients = {}

    self.ports = self.refreshPorts()

    self.server = SimpleXMLRPCServer(("localhost", Registry.SERVER_PORT),
                                     requestHandler=SimpleXMLRPCRequestHandler)
    self.server.register_introspection_functions()

    self.server.register_function(self.kill, "kill")
    self.server.register_function(self.ping, "ping")
    self.server.register_function(self.request_port, "request_port")
    self.server.register_function(self.register, "register")
    self.server.register_function(self.unregister, "unregister")
    self.server.register_function(self.get_clients, "get_clients")

    threading.Thread.__init__(self)

  def run(self):
    print "Cortex registry started"
    while not self.die:
      self.server.handle_request()
    self.server.server_close()

  def refreshPorts(self):
    ret = []
    for port in range(Registry.CLIENT_PORT_START, Registry.CLIENT_PORT_END):
      if port not in self.clients.values():
        ret.append(port)
    return ret


  @synchronize('mutex')
  def ping(self):
    return "pong!"

  @synchronize('mutex')
  def kill(self):
    self.die = True
    return Registry.RET_OK

  @synchronize('mutex')
  def request_port(self):
    try:
      return self.ports.pop()
    except IndexError:
      # Refresh port pool
      self.ports = self.refreshPorts()
      if len(self.ports) == 0:
        return Registry.RET_NO_PORT
      return self.ports.pop()

  @synchronize('mutex')
  def register(self, name, port):
    # Check for duplicate name
    if name in self.clients.keys():
      return Registry.RET_NAME_EXISTS
    # Check for duplicate port
    if port in self.clients.values():
      return Registry.RET_PORT_EXISTS
    # Success
    self.clients[name] = port
    return Registry.RET_OK

  @synchronize('mutex')
  def unregister(self, name, port):
    # Check name matches port
    if self.clients.has_key(name) and self.clients[name] == port:
      self.clients.pop(name)
      return Registry.RET_OK
    else:
      return Registry.RET_BAD

  @synchronize('mutex')
  def get_clients(self):
    return self.clients


if __name__ == "__main__":
  Registry().start()

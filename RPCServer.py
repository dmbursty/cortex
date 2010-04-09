import threading
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler

class RPCServer(threading.Thread):
  def __init__(self, controller):
    self.mutex = threading.Lock()
    self.controller = controller
    self.die = False
    self.server = SimpleXMLRPCServer(("localhost", 8000),
                                     requestHandler=SimpleXMLRPCRequestHandler)
    self.server.register_introspection_functions()

    self.server.register_function(self.kill, "kill")
    self.server.register_function(self.addManager, "addManager")

    threading.Thread.__init__(self)

  def run(self):
    print "RPC Server started"
    while not self.die:
      self.server.handle_request()
    self.server.server_close()

  def kill(self):
    self.mutex.acquire()
    self.controller.kill()
    self.die = True
    self.mutex.release()
    return 0

  def addManager(self, manager, args):
    """Start up a new manager with given args

    manager: String name of manager type
    args: Dict of manager arguments"""
    self.mutex.acquire()
    ret = self.controller.addManager(manager, args)
    self.mutex.release()
    return ret

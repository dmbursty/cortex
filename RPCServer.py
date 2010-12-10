import threading

from RegistryRPCServer import RegistryRPCServer

from common import synchronize

class RPCServer(RegistryRPCServer):
  def __init__(self, controller, name="cortex"):
    self.mutex = threading.Lock()
    self.controller = controller

    RegistryRPCServer.__init__(self, name)

    self.server.register_function(self.kill, "kill")
    self.server.register_function(self.ping, "ping")
    self.server.register_function(self.addManager, "addManager")

  @synchronize('mutex')
  def ping(self):
    return "pong!"

  @synchronize('mutex')
  def kill(self):
    self.controller.kill()
    self.die = True
    return 0

  @synchronize('mutex')
  def addManager(self, manager, args):
    """Start up a new manager with given args

    manager: String name of manager type
    args: Dict of manager arguments"""
    return self.controller.addManager(manager, args)

import logging
import threading

from registry.RegistryRPCServer import RegistryRPCServer

from common.threading import synchronize

class RPCServer(RegistryRPCServer):
  def __init__(self, controller, name="cortex"):
    self.log = logging.getLogger("Cortex.RPCServer")
    self.mutex = threading.Lock()
    self.controller = controller

    RegistryRPCServer.__init__(self, name)

    self.server.register_function(self.kill, "kill")
    self.server.register_function(self.ping, "ping")
    self.server.register_function(self.addManager, "addManager")
    self.server.register_function(self.addDepot, "addDepot")

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

  @synchronize('mutex')
  def addDepot(self, depot, name, args):
    """Start up a new depot with the given args

    depot: String name of the depot type
    name: String unique name for the depot used to identify it
    args: Dict of depot args"""
    return self.controller.addDepot(depot, name, args)

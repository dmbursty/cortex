import logging
import threading
import traceback

from Mixer import Mixer

import managers.ManagerFactory as ManagerFactory
import depots.DepotFactory as DepotFactory


class Controller:
  """Handles input from the RPC server"""

  def __init__(self):
    self.log = logging.getLogger("Cortex.Controller")
    self.managers = []
    self.mutex = threading.Lock()
    self.mixer = Mixer()
    self.nextID = 1

  def kill(self):
    """Shut down the entire system"""
    # Note we cannot kill the RPC Server from here
    self.mutex.acquire()
    for manager in self.managers:
      manager.kill()
    self.mutex.release()

  def addManager(self, manager, args):
    """Start up a new manager with given args

    manager: String name of manager type
    args: Dict of manager arguments"""
    manager_class = ManagerFactory.getManager(manager)
    if manager_class:
      try:
        self.nextID += 1
        if "depots" in args:
          self.mixer.addLinks(self.nextID, args['depots'])
        self.managers.append(manager_class(self.nextID, self.mixer, args))
        self.managers[-1].start()
      except KeyError, e:
        self.log.error("Manager %s init failed due to missing arg: %s" %
            (self.managers[-1], e))
        return 2
      except Exception, e:
        # Manager init failed due to other reason
        self.log.error("Manager %s init failed: %s\nStack Trace:\n%s" %
            (manager_class.__name__ + str(args), e, traceback.format_exc()))
        return 3
    else:
      # If We couldn't find the manager type
      return 1

    return 0

  def addDepot(self, depot, name, args):
    """Start up a new depot with the given args

    depot: String name of the depot type
    name: String unique name for the depot used to identify it
    args: Dict of depot args"""
    depot_class = DepotFactory.getDepot(depot)
    if depot_class:
      try:
        new_depot = depot_class(name, args)
        self.mixer.addDepot(new_depot)
      except KeyError, e:
        self.log.error("Depot init failed due to missing arg: %s" % e)
        return 2
      except Exception,e :
        self.log.error("Depot init failed: %s" % traceback.format_exc())
        return 3
    else:
      return 1

    return 0

import threading

from depots.RSSDepot import RSSDepot

import depots.DepotFactory as DepotFactory
import managers.ManagerFactory as ManagerFactory


class Controller:
  """Handles input from the RPC server"""

  def __init__(self):
    self.managers = []
    self.mutex = threading.Lock()
    self.depot = RSSDepot("/home/max/public_html/burstyn.ca/cortex.xml")
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
        self.managers.append(manager_class(self.nextID, self.depot, args))
        self.managers[-1].start()
      except KeyError, e:
        # Manager init failed due to missing arg
        print e
        return 2
      except Exception, e:
        # Manager init failed due to other reason
        print e
        return 3
    else:
      # If We couldn't find the manager type
      return 1

    return 0

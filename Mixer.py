import logging

from depots.RSSDepot import RSSDepot

class Mixer:
  """Mixer to handle interaction between Managers and Depots"""
  def __init__(self):
    self.log = logging.getLogger("Cortex.Mixer")
    # Keep a base depot for all items from all managers
    self.base_depot = RSSDepot("_base",
                               "/home/max/public_html/burstyn.ca/cortex.xml")
    self.depots = {}
    # Maps manager Id to list of depot names
    self.links = {}

    self.testingInit()

  def testingInit(self):
    depot = RSSDepot("alt", "/home/max/public_html/burstyn.ca/alt.xml")
    self.addDepot(depot)

  def addDepot(self, depot):
    if depot.name in self.depots:
      self.log.warning("A depot with name %s already exists" % depot.name)
      return
    self.depots[depot.name] = depot

  def addLinks(self, manager_id, depot_names):
    # Check all names are present
    if manager_id not in self.links:
      self.links[manager_id] = []

    for name in depot_names:
      if name not in self.depots:
        self.log.warning("Depot %s is not known" % name)
      else:
        self.links[manager_id].append(name)
        self.log.debug("Linked manager %d to depot %s" % (manager_id, name))

  def update(self, source, items):
    self.base_depot.update(items)
    if source.id not in self.links:
      return
    for name in self.links[source.id]:
      self.depots[name].update(items)

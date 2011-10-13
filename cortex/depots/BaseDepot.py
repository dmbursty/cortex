import logging

class BaseDepot:
  """Base class for depots"""
  def __init__(self, name):
    self.log = logging.getLogger("Cortex.Depots.%s" % self.__class__.__name__)
    self.name = name

  # Children must implement this method
  def update(self, items):
    """Manager source has new items for us"""
    raise NotImplemented("BaseDepot: You must implement update")

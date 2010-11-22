class BaseDepot:
  """Base class for depots"""
  def __init__(self):
    pass

  # Children must implement this method
  def update(self, source, items):
    """Manager source has new items for us"""
    raise NotImplemented("BaseDepot: You must implement update")

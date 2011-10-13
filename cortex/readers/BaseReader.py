import logging
import time

class BaseReader:
  def __init__(self):
    self.log = logging.getLogger("Cortex.Readers.%s" %
                                 self.__class__.__name__)
    self.items = []

  def getUpdate(self):
    """Check for updates, and retrieve them"""
    self.checkUpdate()
    # getItems will delete items as it returns them
    return self.getItems()

  def getItems(self):
    """Return all available items (deletes them locally)"""
    ret = self.items
    self.items = []
    return ret

  def peekItems(self):
    """Returns all available items, keeping them locally"""
    # Tuple prevents access to the local list, but does not stop
    # changing the items themselves
    return tuple(self.items)

  # NOT IMPLMENTED
  def checkUpdate(self):
    """This function must be overwritten and should check for an update
       and put the update items in self.items"""
    raise NotImplemented("BaseReader: You must implement checkUpdate")


class BaseItem:
  """Object for storing an item."""
  def __init__(self, data, metadata = {}):
    """data can be in any format, as accessors must be written,
       metadata should be a dict."""
    self.data = data
    self.metadata = metadata
    self.metadata['time'] = time.localtime()

  def getMetadata(self):
    return self.metadata

  # NOT IMPLMENTED
  def getDataString(self):
    """Get the complete item data as a string"""
    raise NotImplemented("BaseItem: You must implement getDataString")

  def getSummaryString(self):
    """Get a short summary of the item"""
    raise NotImplemented("BaseItem: You must implement getSummaryString")

  def title(self):
    """Get the title of the item"""
    # All items need a title
    raise NotImplemented("BaseItem: You must implement title")

  def link(self):
    """Get the link of the item"""
    # Default empty string
    return ""

  def content(self):
    """Get the content of the item"""
    # Default empty string
    return ""

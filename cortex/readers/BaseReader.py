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
  def __init__(self, metadata = {}):
    self.metadata = metadata
    self.metadata['time'] = time.localtime()

    self.title = ""
    self.link = ""

    # Don't default these fields, since they are manditory
    #self.content = ""
    #self.html = ""

  def set_all_content(self, content):
    """Helper to set all content fields to the same value, for simple readers"""
    self.title = content
    self.content = content
    self.html = content

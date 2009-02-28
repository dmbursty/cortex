# THIS FILE IS NOT TO BE USED
# It is a starting point for building a reader
#
# Copy this file and save as the new reader
# s/Base/Type/g to change BaseReader to TypeReader etc

raise NotImplemented("This file is for reference only. DO NOT USE")

class BaseReader:
  def __init__(self, args):
    self.source = args['source']
    self.data = None
    self.identifier = None

    print "Created Base Reader with source %s" % self.source
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing identifiers.
       This call will update self.data
    """
    self.retrieveData()
    # Functionality for identifiers goes here
    new_identifier = 0
    if new_identifier != self.identifier:
      self.identifier = new_identifier
      return True
    return False

  def retrieveData(self):
    """Retrieve data from the source"""
    if self.source is None:
      raise Exception("No source was given")
    # Get data from source
    self.data = "Base Data"

  def getUpdate(self):
    """Return the latest update to the source"""

  def getItems(self):
    """Return all items of the source"""
    # Turn raw data into items, and return
    items = []
    for word in self.data.split(" "):
      items.append(BaseItem(word))
    return items


class BaseItem:
  """Object for storing an item. Has output formatters"""
  def __init__(self, data, aux = None):
    # data is a mandatory field
    self.data = data
    # aux is a dictionary of optional fields
    self.aux = aux

  def toString(self):
    """Get the item as a complete string"""
    ret = self.data + "\n"
    return ret

  def toSummary(self):
    """Get a short summary of the item"""
    return str(len(self.data))

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    # Remember to escape when necessary
    return "<h1>" + self.data + "<\h1>"

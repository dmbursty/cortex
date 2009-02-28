import urllib2

class SimpleWebsiteReader:
  """Reader for very simple webpages.  Compares hashes of the page's source
     This will fail on sites with random content (including ads)
  """
  def __init__(self, args):
    self.source = args['source']
    self.data = None
    self.identifier = None

    print "Created Simple Website Reader with source %s" % self.source
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing identifiers.
       This call will update self.data
    """
    self.retrieveData()
    new_identifier = hash(self.data)
    if new_identifier != self.identifier:
      self.identifier = new_identifier
      return True
    return False

  def retrieveData(self):
    """Retrieve data from the source"""
    if self.source is None:
      raise Exception("No source was given")
    # Get data from source
    request   = urllib2.Request(self.source)
    opener    = urllib2.build_opener()
    self.data = opener.open(request).read()

  def getUpdate(self):
    """Return the latest update to the source"""

  def getItems(self):
    """Return all items of the source"""
    # Turn raw data into items, and return
    return [SimpleWebsiteItem(len(self.data))]


class SimpleWebsiteItem:
  """Object for storing an item. Has output formatters"""
  def __init__(self, data, aux = None):
    # data is a mandatory field
    self.data = data
    # aux is a dictionary of optional fields
    self.aux = aux

  def toString(self):
    """Get the item as a complete string"""
    return "The site was updated [%d bytes]" % self.data

  def toSummary(self):
    """Get a short summary of the item"""
    return "Updated"

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    # Remember to escape when necessary
    return self.toString()

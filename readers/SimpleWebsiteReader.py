import urllib2

from BaseReader import BaseReader, BaseItem


class SimpleWebsiteReader(BaseReader):
  """Reader for very simple webpages.  Compares hashes of the page's source
     This will fail on sites with random content (including ads)
  """
  def __init__(self, args):
    self.source = args['source']
    self.state = None

    print "Created Simple Website Reader with source %s" % self.source
    BaseReader.__init__(self)

  def checkUpdate(self):
    # Get data from source
    request = urllib2.Request(self.source)
    opener  = urllib2.build_opener()
    data    = opener.open(request).read()

    if self.state is None:
      self.state = data
    elif self.state != data:
      self.state = data
      self.items.append(SimpleWebsiteItem(self.source))


class SimpleWebsiteItem(BaseItem):
  def __init__(self, data):
    BaseItem.__init__(self, data)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "Update found in %s" % self.data

  def getSummaryString(self):
    """Get a short summary of the item"""
    return "Update found in %s" % self.data

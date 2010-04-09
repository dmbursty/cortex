import urllib2
from xml.dom import minidom

from BaseReader import BaseReader, BaseItem


class RSSReader(BaseReader):
  """Reader for RSS Feeds"""
  def __init__(self, args):
    # The address of the xml feed
    self.source = args['source']
    # To store the parsed xml data
    self.data = None
    # A value to compare with to check whether the feed has updated
    # Currently is hash of latest item title
    self.latest = None

    print "Created RSS Reader with source %s" % self.source
    BaseReader.__init__(self)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    # Pull feed data
    request = urllib2.Request(self.source)
    opener  = urllib2.build_opener()
    feed    = opener.open(request).read()
    data    = minidom.parseString(feed)

    # Check if there is a new item
    items = data.getElementsByTagName("item")
    latest_item = items[0]
    latest = latest_item.childNodes[1].firstChild.data
    if self.latest is None:
      self.latest = latest
    elif self.latest != latest:
      # Constuct RSS items
      for item in items:
        # Loop until we hit one we've already handled
        if item.childNodes[1].firstChild.data == self.latest:
          break
        self.items.append(RSSItem(item, {'source':self.source}))
      self.latest = latest


class RSSItem(BaseItem):
  def __init__(self, data, metadata):
    # data is the xml object containing the RSS data
    #   childNode[1]: title
    #   childNode[3]: link
    #   childNode[5]: text
    BaseItem.__init__(self, data, metadata)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "%s\n%s\nSource: %s" % (self.data.childNodes[1].firstChild.data,
                                   self.data.childNodes[5].firstChild.data,
                                   self.data.childNodes[3].firstChild.data)

  def getSummaryString(self):
    """Get a short summary of the self.data"""
    return "%s:\n    %s" % (self.data.childNodes[3].firstChild.data,
                            self.data.childNodes[1].firstChild.data)

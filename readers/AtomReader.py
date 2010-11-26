import urllib2
from xml.dom import minidom

from BaseReader import BaseReader, BaseItem


class AtomReader(BaseReader):
  """Reader for Atom Feeds"""
  def __init__(self, args):
    # The address of the xml feed
    self.source = args['source']
    # To store the parsed xml data
    self.data = None
    # A value to compare with to check whether the feed has updated
    # Currently is hash of latest item title
    self.latest = None

    print "Created Atom Reader with source %s" % self.source
    BaseReader.__init__(self)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    # Pull feed data
    request = urllib2.Request(self.source)
    opener  = urllib2.build_opener()
    feed    = opener.open(request).read()
    data    = minidom.parseString(feed)

    # Check if there is a new item
    items = data.getElementsByTagName("entry")
    latest = items[0].getElementsByTagName("title")[0].firstChild.data
    # Constuct RSS items
    for item in reversed(items):
      # Loop through ones we've already done
      if self.latest is not None and item.getElementsByTagName("title")[0].firstChild.data == self.latest:
        continue
      self.items.append(RSSItem(item, {'source':self.source}))
    self.latest = latest


class AtomItem(BaseItem):
  def __init__(self, data, metadata):
    # data is the xml object containing the RSS data
    BaseItem.__init__(self, data, metadata)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "%s\n%s\nSource: %s" % (self.title(), self.content(), self.link())

  def getSummaryString(self):
    """Get a short summary of the self.data"""
    return "%s:\n    %s" % (self.link(), self.title())

  def title(self):
    """Get the title of the item"""
    title = self.data.getElementsByTagName("title")[0].firstChild.data
    return title

  def link(self):
    """Get the link of the item"""
    link = self.data.getElementsByTagName("link")[0].getAttribute("href")
    return link

  def content(self):
    """Get the content of the item"""
    content = self.data.getElementsByTagName("content")[0].firstChild.data
    return content

import urllib2
from xml.dom import minidom

from BaseReader import BaseReader, BaseItem


"""Get an ID for the item to identify it uniquely"""
def getItemHash(item):
  #TODO: Make this more unique
  return item.getElementsByTagName("title")[0].firstChild.data

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

    BaseReader.__init__(self)
    self.log.info("Created RSS Reader with source %s" % self.source)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    # Pull feed data
    request = urllib2.Request(self.source)
    opener  = urllib2.build_opener()
    feed    = opener.open(request).read()
    data    = minidom.parseString(feed)

    # Check if there are new items.  NOTE: The feed has items from newer->older,
    # but we want the items to be older->newer so reverse iterate
    items = data.getElementsByTagName("item")
    # Start with the oldest item
    i = len(items) - 1
    while i >= 0 and self.latest is not None:
      # Loop through items older than the newest one we saw last time
      if (getItemHash(items[i]) == self.latest):
        i -= 1
        break
      i -= 1

    while i >= 0:
      # Remaining items are new, so add them oldest->newest
      self.items.append(RSSItem(items[i], {'source':self.source}))
      i -= 1

    self.latest = getItemHash(items[0])


class RSSItem(BaseItem):
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
    link = self.data.getElementsByTagName("link")[0].firstChild.data
    return link

  def content(self):
    """Get the content of the item"""
    content = self.data.getElementsByTagName("description")[0].firstChild.data
    return content

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
  def __init__(self, xml, metadata):
    BaseItem.__init__(self, metadata)
    self.title = xml.getElementsByTagName("title")[0].firstChild.data
    self.link = xml.getElementsByTagName("link")[0].firstChild.data
    self.html =  xml.getElementsByTagName("description")[0].firstChild.data
    self.content = self.html

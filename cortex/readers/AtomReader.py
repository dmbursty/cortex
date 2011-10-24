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

    BaseReader.__init__(self)
    self.log.info("Created Atom Reader with source %s" % self.source)

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
      self.items.append(AtomItem(item, {'source':self.source}))
    self.latest = latest


class AtomItem(BaseItem):
  def __init__(self, xml, metadata):
    BaseItem.__init__(self, metadata)
    self.title = xml.getElementsByTagName("title")[0].firstChild.data
    self.link = xml.getElementsByTagName("link")[0].getAttribute("href")
    self.html = xml.getElementsByTagName("content")[0].firstChild.data
    self.content = self.html

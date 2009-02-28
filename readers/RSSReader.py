import urllib2
from xml.dom import minidom

class RSSReader:
  """Reader for RSS Feeds"""
  def __init__(self, args):
    # The address of the xml feed
    self.source = args['source']
    # To store the parsed xml data
    self.data = None
    # A value to compare with to check whether the feed has updated
    # Currently is hash of latest item title
    self.identifier = None

    print "Created RSS Reader with source %s" % self.source
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing hashes of the latest item.
       This call will update self.data.
    """
    self.retrieveData()
    latest_item = self.data.getElementsByTagName("item")[0]
    new_identifier = hash(latest_item.childNodes[1].firstChild.data)
    if new_identifier == self.identifier:
      return False
    else:
      self.identifier = new_identifier
      return True

  def retrieveData(self):
    """Retrieve and parse the feed"""
    if self.source is None:
      raise Exception("No source was given")
    request   = urllib2.Request(self.source)
    opener    = urllib2.build_opener()
    feed      = opener.open(request).read()
    self.data = minidom.parseString(feed)

  def getItems(self):
    """From the saved data, return a list of items.
       Each item is a dictionary of the fields.
    """
    if self.data is None:
      raise Exception("Cannot get items - no data present")

    return_items = []
    items = self.data.getElementsByTagName("item")
    if items is []:
      raise Exception("Feed was empty")
    for item in items:
      return_items.append(RSSItem(self,
                                  item.childNodes[1].firstChild.data,
                                  item.childNodes[3].firstChild.data,
                                  item.childNodes[5].firstChild.data))

    return return_items


class RSSItem:
  """Object for storing an item. Has output formatters"""
  def __init__(self, reader, title, link, text, aux = None):
    self.reader = reader
    self.title = title
    self.link = link
    self.text = text
    self.aux = aux

  def toString(self):
    """Get the item as a complete string"""
    ret = self.title + "\n"
    ret += self.text + "\n"
    ret += "Source: " + self.link + "\n"
    ret += "Additional data:\n"
    for k, v in self.aux:
      ret += "%s: %s\n" % (str(k), str(v))
    return ret

  def toSummary(self):
    """Get a short summary of the item"""
    return "%s:\n%s" % (self.reader.source, self.title)

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    return "Not implemented yet - RSS.toHTML"

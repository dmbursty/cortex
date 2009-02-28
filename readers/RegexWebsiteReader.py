import re
import urllib2

class RegexWebsiteReader:
  """Reader for webpages.  Compares the text that matches the given regex.
     Since this only checks a specific regex, other updates to the site may
     not be caught, and if no match is found the reader dies (to avoid checking
     sites that may have a layout change).
  """
  def __init__(self, args):
    self.source = args['source']
    self.regex = re.compile(args['regex'])
    self.data = None
    self.identifier = None

    print "Created Regex Website Reader with source %s" % self.source
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing identifiers.
       This call will update self.data
    """
    self.retrieveData()
    match = self.regex.search(self.data)
    if match is None:
      raise Exception("%s didn't match regex" % self.source)
    new_identifier = hash(match.group(0))
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
    return [RegexWebsiteItem(len(self.data))]


class RegexWebsiteItem:
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

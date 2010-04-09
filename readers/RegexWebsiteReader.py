import re
import urllib2

from BaseReader import BaseReader, BaseItem


class RegexWebsiteReader(BaseReader):
  """Reader for webpages.  Compares the text that matches the given regex.
     Since this only checks a specific regex, other updates to the site may
     not be caught, and if no match is found the reader dies (to avoid checking
     sites that may have a layout change).
  """
  def __init__(self, args):
    self.source = args['source']
    self.regex = re.compile(args['regex'])
    self.lastmatch = None

    print "Created Regex Website Reader with source %s" % self.source
    self.checkUpdate()
    BaseReader.__init__(self)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    # Get website data
    request = urllib2.Request(self.source)
    opener  = urllib2.build_opener()
    data    = opener.open(request).read()
    
    # Check for an update
    match = self.regex.search(data)
    if match is None:
      raise Exception("No match for regex on %s" % self.source)
    elif self.lastmatch is None:
      self.lastmatch = match.group(0)
    elif self.lastmatch != match.group(0):
      self.lastmatch = match.group(0)
      self.items.append(RegexWebsiteItem(match, {'source':self.source}))
      print self.lastmatch


class RegexWebsiteItem(BaseItem):
  def __init__(self, data):
    BaseItem.__init__(self, data)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "Update found for %s" % self.metadata['source']

  def getSummaryString(self):
    """Get a short summary of the item"""
    return "Update found for %s" % self.metadata['source']
    

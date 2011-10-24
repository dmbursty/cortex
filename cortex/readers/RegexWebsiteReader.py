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

    BaseReader.__init__(self)
    self.log.info("Created Regex Website Reader with source %s" % self.source)
    self.checkUpdate()

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
      self.items.append(RegexWebsiteItem(self.source))


class RegexWebsiteItem(BaseItem):
  def __init__(self, source):
    BaseItem.__init__(self)
    self.set_all_content("Update found for %s" % source)
    self.link = source

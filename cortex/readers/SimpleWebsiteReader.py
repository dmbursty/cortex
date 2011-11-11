from common import urlfetch
from BaseReader import BaseReader, BaseItem


class SimpleWebsiteReader(BaseReader):
  """Reader for very simple webpages.  Compares hashes of the page's source
     This will fail on sites with random content (including ads)
  """
  def __init__(self, args):
    self.source = args['source']
    self.state = None

    BaseReader.__init__(self)
    self.log.info("Created Simple Website Reader with source %s" % self.source)

  def checkUpdate(self):
    # Get data from source
    data = urlfetch.fetch(self.source).read()

    if self.state is None:
      self.state = data
    elif self.state != data:
      self.state = data
      self.items.append(SimpleWebsiteItem(self.source))

  def __str__(self):
    return "%s(%s)" % (BaseReader.__str__(self), self.source)


class SimpleWebsiteItem(BaseItem):
  def __init__(self, source):
    BaseItem.__init__(self)
    self.set_all_content("Update found in %s" % source)
    self.link = source

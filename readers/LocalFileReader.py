from BaseReader import BaseReader, BaseItem


class LocalFileReader(BaseReader):
  """Reader for local files.
     Currently only text files should be used.
  """
  def __init__(self, args):
    self.source = args['source']
    # init data
    file = open(self.source, 'rb')
    self.data = file.read()
    file.close()

    print "Starting File Reader with source", self.source
    BaseReader.__init__(self)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    file = open(self.source, 'rb')
    data = file.read()
    file.close()

    if data != self.data:
      self.items.append(LocalFileItem(self.source))
      self.data = data
    

class LocalFileItem(BaseItem):
  def __init__(self, data):
    BaseItem.__init__(self, data)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "Update found in %s" % self.data

  def getSummaryString(self):
    """Get a short summary of the item"""
    return "Update found in %s" % self.data

  def title(self):
    """Get the title of the item"""
    return "Update found in %s" % self.data

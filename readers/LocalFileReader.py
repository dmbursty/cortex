class LocalFileReader:
  """Reader for local files.
     Currently only text files should be used.
  """
  def __init__(self, args):
    self.source = args['source']
    self.data = None
    self.identifier = None

    print "Created file reader with source %s" % self.source
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing hashes of the file.
       This call will update self.data.
    """
    self.retrieveData()
    new_identifier = hash(self.data)
    if new_identifier == self.identifier:
      return False
    else:
      self.identifier = new_identifier
      return True

  def retrieveData(self):
    """Retrieve and parse the feed"""
    if self.source is None:
      raise Exception("No source was given")
    file = open(self.source, 'rb')
    self.data = file.read()
    file.close()

  def getItems(self):
    """From the saved data, return a list of items.
       Returns only one item, that is the file.
    """
    if self.data is None:
      raise Exception("Cannot get items - no data present")
    return [LocalFileItem(self, self.data)]

class LocalFileItem:
  """Object for storing an item. Has output formatters"""
  def __init__(self, reader, data, aux = None):
    self.reader = reader
    self.data = data
    self.aux = aux

  def toString(self):
    """Get the item as a complete string"""
    return self.data

  def toSummary(self):
    """Get a short summary of the item"""
    return "Update found for %s" % self.reader.source

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    return self.toString()

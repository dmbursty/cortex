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

    BaseReader.__init__(self)
    self.log.info("Starting File Reader with source", self.source)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    file = open(self.source, 'rb')
    data = file.read()
    file.close()

    if data != self.data:
      self.items.append(LocalFileItem(self.source))
      self.data = data
    

class LocalFileItem(BaseItem):
  def __init__(self, filename):
    BaseItem.__init__(self)
    self.set_all_content("Update found in %s" % filename)
    # This will probably not work, but better than nothing
    self.link = "file://%s" % filename

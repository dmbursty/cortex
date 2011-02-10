from BaseDepot import BaseDepot

class CoutDepot (BaseDepot):
  def __init__(self):
    BaseDepot.__init__(self)
    self.sep = '-' * 80

  def update(self, source, items):
    for item in items:
      print item.title()
      print item.link()
      print item.content()
      print self.sep

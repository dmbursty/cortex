from BaseDepot import BaseDepot

class CoutDepot (BaseDepot):
  def __init__(self, name):
    BaseDepot.__init__(self, name)
    self.sep = '-' * 80

  def update(self, items):
    for item in items:
      print item.title()
      print item.link()
      print item.content()
      print self.sep

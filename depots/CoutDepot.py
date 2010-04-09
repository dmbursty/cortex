class CoutDepot:
  def __init__(self):
    pass

  def update(self, items):
    for item in items:
      print "Update:", item.getSummaryString()

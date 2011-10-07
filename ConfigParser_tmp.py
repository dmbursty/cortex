class ConfigParser:
  def __init__(self):
    pass

  def parseXML(filename):
    try:
      file = open(filename)
    except IOError, e:
      print "Couldn't open file %s" % filename
      return None

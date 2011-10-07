import xml.dom.minidom

class ConfigLoader:
  def __init__(self):
    pass

  @staticmethod
  def parseXML(filename):
    try:
      dom = xml.dom.minidom.parse(filename)
      file = open(filename)
    except IOError, e:
      print "Couldn't open file %s" % filename
      return None

    for server in dom.getElementsByTagName("server"):
      parseServer(server)


if __name__ == "__main__":
  ConfigLoader.parseXML("config.xml")

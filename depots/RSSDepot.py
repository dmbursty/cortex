from common import xml

from BaseDepot import BaseDepot

RSS_HEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rss version=\"2.0\"><channel><title>Cortex</title>\n"
RSS_ITEMBASE = "<item><title>%s</title><link>%s</link><description>%s</description></item>\n"
RSS_FOOTER = "</channel></rss>\n"


class RSSDepot (BaseDepot):
  def __init__(self, outfile):
    self.outfile = outfile
    self.items = []
    BaseDepot.__init__(self)

  def update(self, source, items):
    self.items.extend(items)

    # Build xml file
    out = RSS_HEADER

    for item in reversed(self.items[-30:]):
      out += self.itemToXML(item)

    out += RSS_FOOTER

    # Write xml file
    try:
      f = open(self.outfile, 'w')
      ff = out.decode("utf-8").encode("utf_8")
      f.write(ff)
    except IOError, e:
      print "IOError in RSSDepot: %s" % e
      raise
      

  def itemToXML(self, item):
    return RSS_ITEMBASE % (xml.escape(item.title()),
                           xml.escape(item.link()),
                           xml.escape(item.content()))

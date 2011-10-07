import time
import traceback

from common import xml

from BaseDepot import BaseDepot

RSS_HEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rss version=\"2.0\">\n<channel>\n<title>Cortex</title>"
RSS_ITEMBASE = """
<item>
  <title>%s</title>
  <link>%s</link>
  <description>%s</description>
  <pubDate>%s</pubDate>
  <guid>%s</guid>
</item>
"""
RSS_FOOTER = "</channel>\n</rss>\n"


class RSSDepot (BaseDepot):
  def __init__(self, name, outfile):
    BaseDepot.__init__(self, name)
    self.outfile = outfile
    self.items = []

  def update(self, items):
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
      self.log.error("IOError in RSSDepot: %s" % traceback.format_exc())
      raise
      
  def makeGUID(self, item):
    return "%s#%d" % (item.link(),
                      time.mktime(item.getMetadata()['time']))

  def itemToXML(self, item):
    return RSS_ITEMBASE % (xml.escape(item.title()),
                           xml.escape(item.link()),
                           xml.escape(item.content()),
                           time.strftime("%a, %d %b %Y %H:%M:%S %Z",
                           item.getMetadata()['time']),
                           self.makeGUID(item))

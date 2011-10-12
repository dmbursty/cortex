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

# All about unicode:
# encode: unicode string --> byte string
# decode: byte string --> unicode string
# For ascii byte strings == their unicode equivalent
#
# Ex: u'\u2022'.encode('utf8')       --> b'\xe2\x80\xa2'
#     b'\xe2\x80\xa2'.encode('utf8') --> u'\u2022'
#     b'\xe2\x80\xa2'.encode('utf8') --> UnicodeDecodeError char \xe2
#     u'\u2022'.decode('utf8')       --> UnicodeEncodeError char \u2022

class RSSDepot (BaseDepot):
  def __init__(self, name, args):
    BaseDepot.__init__(self, name)
    self.outfile = args['outfile']
    self.items = []

  def update(self, items):
    self.items.extend(items)

    # Build xml file
    out = RSS_HEADER

    for item in reversed(self.items[-30:]):
      item_out = self.itemToXML(item)
      # Ensure each item is a utf8 encoded string
      try:
        out += item_out.decode('utf8')
      except UnicodeEncodeError:
        out += item_out

    out += RSS_FOOTER

    # Write xml file
    try:
      f = open(self.outfile, 'w')
      f.write(out.encode("utf8"))
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

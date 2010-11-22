import re
import htmlentitydefs
from BaseDepot import BaseDepot

RSS_HEADER = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<rss version=\"2.0\"><channel><title>Cortex</title>\n"
RSS_ITEMBASE = "<item><title>%s</title><link>%s</link><description>%s</description></item>\n"
RSS_FOOTER = "</channel></rss>\n"

def unescape(text):
   """Removes HTML or XML character references 
      and entities from a text string.
   @param text The HTML (or XML) source text.
   @return The plain text, as a Unicode string, if necessary.
   from Fredrik Lundh
   2008-01-03: input only unicode characters string.
   http://effbot.org/zone/re-sub.htm#unescape-html
   """
   def fixup(m):
      text = m.group(0)
      if text[:2] == "&#":
         # character reference
         try:
            if text[:3] == "&#x":
               return unichr(int(text[3:-1], 16))
            else:
               return unichr(int(text[2:-1]))
         except ValueError:
            print "Value Error"
            pass
      else:
         # named entity
         # reescape the reserved characters.
         try:
            if text[1:-1] == "amp":
               text = "&amp;amp;"
            elif text[1:-1] == "gt":
               text = "&amp;gt;"
            elif text[1:-1] == "lt":
               text = "&amp;lt;"
            else:
               text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
         except KeyError:
            print "keyerror"
            pass
      return text # leave as is
   return re.sub("&#?\w+;", fixup, text)


class RSSDepot (BaseDepot):
  def __init__(self, outfile):
    self.outfile = outfile
    self.items = []
    BaseDepot.__init__(self)

  def update(self, source, items):
    self.items.extend(items)

    # Build xml file
    out = RSS_HEADER

    for item in self.items:
      out += self.itemToXML(item)

    out += RSS_FOOTER
    
    # Clean out the html &; codes
    out = unescape(out)

    # Write xml file
    f = open(self.outfile, 'w')
    f.write(out.encode("utf-8"))

  def itemToXML(self, item):
    return RSS_ITEMBASE % (item.title(), item.link(), item.content())

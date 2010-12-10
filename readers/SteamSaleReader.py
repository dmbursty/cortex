import re
import urllib2

from BaseReader import BaseReader, BaseItem

class SteamSaleReader(BaseReader):
  SPECIALS_URL = "http://store.steampowered.com/search/?specials=1"
  ITEM_PATTERN = "<a href=\"[\w\d:/.]+?\" class=\"search_result_row.*?</a>"
  DATA_PATTERN = """href=\"([\w\d:/.]+?)\"   .*?     # Link
                    <strike>&\#36;([\d.]+)</strike>  # Original price
                    </span><br>&\#36;([\d.]+)</div>  # Sale price
                    .*? <h4>(.+?)</h4>               # Title
                    """

  def __init__(self, args):
    self.regex = re.compile(self.ITEM_PATTERN, re.DOTALL)
    self.dataregex = re.compile(self.DATA_PATTERN, re.DOTALL | re.VERBOSE)
    self.prevsales = None
    print "Created Steam Sale Reader"
    BaseReader.__init__(self)

  def diffSales(self, sa, sb):
    if sa is None or sb is None:
      return True

    if len(sa) != len(sb):
      return True

    for ia, ib in zip(sa, sb):
      for ka, kb in zip(ia, ib):
        if ka != kb:
          return True

    return False

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    request = urllib2.Request(self.SPECIALS_URL)
    opener  = urllib2.build_opener()

    # Try up to 3 times
    numTries = 3
    for i in range(numTries):
      try:
        data = opener.open(request).read()
        break
      except IncompleRead, e:
        if i == numTries - 1:
          raise
        continue
      

    sales = []

    items = re.findall(self.regex, data)
    try:
      for item in items:
        match = self.dataregex.search(item)
        link, price, sale_price, title = match.groups()
        sales.append((title, price, sale_price, link))
    except AttributeError, e:
      print "Regex didn't match:"
      print item
      raise

    sales.sort()  # Sort by title

    if self.diffSales(sales, self.prevsales):
      self.items.append(SteamSaleItem(sales, {"link":self.SPECIALS_URL}))
      self.prevsales = sales

class SteamSaleItem(BaseItem):
  def __init__(self, data, metadata):
    # data: list of tuples of (Title, base price, sale price, link url)
    BaseItem.__init__(self, data, metadata)

  def getDataString(self):
    """Get the complete item data as a string"""
    return self.content()

  def getSummaryString(self):
    """Get a short summary of the item"""
    return self.title()

  def title(self):
    """Get the title of the item"""
    return "Steam sale update!"

  def link(self):
    """Get the link of the item"""
    return self.metadata["link"]

  def content(self):
    """Get the content of the item"""
    ret = ""
    for item in self.data:
      sale = int(((float(item[1]) - float(item[2])) / float(item[1])) * 100)
      ret += "<a href=\"%s\">%s on sale for %s (%d%% off)</a><br>\n" % (item[3],
                                                                        item[0],
                                                                        item[2],
                                                                        sale)
    return ret


if __name__ == "__main__":
  ssr = SteamSaleReader({})
  ssr.checkUpdate()
  ssr.checkUpdate()
  print ssr.items[0].title()
  print ssr.items[0].link()
  print ssr.items[0].content()

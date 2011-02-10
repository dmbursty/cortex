import re
import httplib
import urllib2

from BaseReader import BaseReader, BaseItem

class SteamSaleReader(BaseReader):
  SPECIALS_URL = "http://store.steampowered.com/search/?specials=1"
  ITEM_PATTERN = "<a href=\"[\w\d:/._?=]+?\" class=\"search_result_row.*?</a>"
  # Basic sale pattern
  DATA_PATTERN = """href=\"([\w\d:/._?=]+?)\"   .*?  # Link
                    <strike>&\#36;([\d.]+)</strike>  # Original price
                    </span><br>&\#36;([\d.]+)</div>  # Sale price
                    .*? <h4>(.+?)</h4>               # Title
                    """
  # Pattern for items that are free
  DATA_FREE_PATTERN = """href=\"([\w\d:/._?=]+?)\"   .*?  # Link
                         search_price">Free</div>         # Free
                         .*? <h4>(.+?)</h4>               # Title
                         """
  # Pattern for items under specials that aren't really on sale
  DATA_EMPTY_PATTERN = """href=\"([\w\d:/._?=]+?)\"   .*?    # Link
                          search_price">&\#36;([\d.]+)</div> # Base Price
                          .*? <h4>(.+?)</h4>                 # Title
                          """

  def __init__(self, args):
    self.regex = re.compile(self.ITEM_PATTERN, re.DOTALL)
    self.dataregex = re.compile(self.DATA_PATTERN, re.DOTALL | re.VERBOSE)
    self.datafreeregex = re.compile(self.DATA_FREE_PATTERN,
                                    re.DOTALL | re.VERBOSE)
    self.dataemptyregex = re.compile(self.DATA_EMPTY_PATTERN,
                                     re.DOTALL | re.VERBOSE)
    self.prevsales = None

    BaseReader.__init__(self)
    self.log.info("Created Steam Sale Reader")

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
      except httplib.IncompleteRead, e:
        if i == numTries - 1:
          raise
        continue
      

    sales = []

    items = re.findall(self.regex, data)
    for item in items:
      try:
        match = self.dataregex.search(item)
        link, price, sale_price, title = match.groups()
        sales.append((title, price, sale_price, link))
      except AttributeError, e:
        try:
          match = self.datafreeregex.search(item)
          link, title = match.groups()
          sales.append((title, 0, 0, link))
        except AttributeError, e:
          match = self.dataemptyregex.search(item)
          if match is None:
            self.log.warning("Regex didn't match item: %s" % item)

    sales.sort()  # Sort by title

    if self.diffSales(sales, self.prevsales):
      self.items.append(SteamSaleItem(sales, self.prevsales, {"link":self.SPECIALS_URL}))
      self.prevsales = sales

class SteamSaleItem(BaseItem):
  def __init__(self, data, prevdata, metadata):
    # data: list of tuples of (Title, base price, sale price, link url)
    self.prevdata = prevdata
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

  def formatItem(self, item, color=None):
      if color is None:
        style = ""
      else:
        style = "style=\"color: %s;\"" % color
      if item[1] == 0 and item[2] == 0:
        return "<a %s href=\"%s\">%s is Free!</a><br>\n" % (style, item[3], item[0])
      else:
        sale = int(((float(item[1]) - float(item[2])) / float(item[1])) * 100)
        return ("<a %s href=\"%s\">%s on sale for %s (%d%% off)</a><br>\n" %
                   (style, item[3], item[0], item[2], sale))

  def getDiffSales(self, sa, sb):
    ret = []
    ia = 0
    ib = 0
    while ia < len(sa) and ib < len(sb):
      if sa[ia][0] < sb[ib][0]:
        ret.append(sa[ia])
        ia += 1
        continue
      elif sa[ia][0] == sb[ib][0]:
        ia += 1
        ib += 1
      else:
        ib += 1

    return ret

  def content(self):
    """Get the content of the item"""
    ret = ""

    # Generate diff information
    if self.prevdata is not None:
      diffsales = self.getDiffSales(self.data, self.prevdata)
      if diffsales:
        ret += "Update<br/>\n"
        for item in diffsales:
          ret += self.formatItem(item, "#00CC00")
        ret += "</span><br/>\n"
      else:
        diffsales = self.getDiffSales(self.prevdata, self.data)
        for item in diffsales:
          ret += self.formatItem(item, "#CC0000")
        ret += "</span><br/>\n"
        

    # Full summary
    ret += "Full Summary<br/>\n"
    for item in self.data:
      ret += self.formatItem(item)

    return ret

if __name__ == "__main__":
  r = SteamSaleReader({})
  for item in r.getUpdate():
    print item.content()

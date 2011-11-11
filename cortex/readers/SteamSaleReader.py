import re
import traceback

from common import urlfetch
from BaseReader import BaseReader, BaseItem

class SteamSaleReader(BaseReader):
  SPECIALS_URL = "http://store.steampowered.com/search/?specials=1"
  SPECIALS_PAGE_URL = "http://store.steampowered.com/search/?specials=1&page=%d"
  ITEM_PATTERN = "<a href=\"[\w\d:/._?=]+?\" class=\"search_result_row.*?</a>"
  # Basic sale pattern
  DATA_PATTERN = """href=\"([\w\d:/._]+)\?.*?\"   .*?  # Link
                    <strike>&\#36;([\d.]+)</strike>    # Original price
                    </span><br>&\#36;([\d.]+)</div>    # Sale price
                    .*? <h4>(.+?)</h4>                 # Title
                    """
  # Pattern for items that are free
  DATA_FREE_PATTERN = """href=\"([\w\d:/._]+)\?.*?\"   .*?  # Link
                         search_price">Free</div>           # Free
                         .*? <h4>(.+?)</h4>                 # Title
                         """
  # Pattern for items under specials that aren't really on sale
  DATA_EMPTY_PATTERN = """href=\"([\w\d:/._]+)\?.*?\"   .*?   # Link
                          search_price">&\#36;([\d.]+)</div>  # Base Price
                          .*? <h4>(.+?)</h4>                  # Title
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
      self.log.info("Diff sales due to None")
      return True

    if len(sa) != len(sb):
      self.log.info("Diff sales due to # of sales")
      return True

    for ia, ib in zip(sa, sb):
      for ka, kb in zip(ia, ib):
        if ka != kb:
          self.log.info("Diff sales due to %s != %s" % (ka, kb))
          return True

    return False

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    items = []
    maxPages = 7

    # Check for multiple pages of sales
    for page in range(1, maxPages):
      data = urlfetch.fetch(self.SPECIALS_PAGE_URL % page).read()
      new_items = re.findall(self.regex, data)
      self.log.debug("Found %d sales for page %d" % (len(new_items), page))
      items.extend(new_items)

      # Stop checking pages after an empty one
      if len(new_items) == 0:
        break
        

    sales = []

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
      self.items.append(SteamSaleItem(sales, self.prevsales))
      self.prevsales = sales

class SteamSaleItem(BaseItem):
  def __init__(self, sales, prevsales):
    # sales: list of tuples of (Title, base price, sale price, link url)
    BaseItem.__init__(self)
    self.title = "Steam sale update!"
    self.link = SteamSaleReader.SPECIALS_URL
    self.html = ""

    # Generate diff information
    if prevsales is not None:
      newsales = self.getDiffSales(sales, prevsales)
      endsales = self.getDiffSales(prevsales, sales)
      if newsales or endsales:
        self.html += "Update<br/>\n"
        for item in newsales:
          self.html += self.formatItem(item, "#00CC00")
        self.html += "</span><br/>\n"
        for item in endsales:
          self.html += self.formatItem(item, "#CC0000")
        self.html += "</span><br/>\n"

    # Full summary
    self.html += "Full Summary<br/>\n"
    for item in sales:
      self.html += self.formatItem(item)

    self.content = self.html

  def formatItem(self, item, color=None):
      if color is None:
        style = ""
      else:
        style = "style=\"color: %s;\"" % color
      if item[1] == 0 and item[2] == 0:
        return "<a %s href=\"%s\">%s is Free!</a><br>\n" % (style,
                                                            item[3],
                                                            item[0])
      else:
        pricedrop = float(item[1]) - float(item[2])
        sale = int((pricedrop / float(item[1])) * 100)
        return ("<a %s href=\"%s\">%s for $%s (%d%% / $%.2f off)</a><br>\n" %
                   (style, item[3], item[0], item[2], sale, pricedrop))

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

    while ia < len(sa):
      ret.append(sa[ia])
      ia += 1

    return ret

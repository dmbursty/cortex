class Histogram:
  def __init__(self, name="Histogram", buckets=None):
    # If buckets is None, then do the bucketing dynamically
    self.name = name
    self.buckets = {}
    self.dynamic = (buckets is None)
    self.bucket_keys = buckets

    if buckets:
      for b in buckets:
        self.buckets[b] = 0

  def add(self, k):
    if k in self.buckets:
      self.buckets[k] += 1
    elif self.dynamic:
      self.buckets[k] = 1
    else:
      # Bucket does not exist
      pass

  def reset(self, buckets=None):
    self.__init__(buckets)

  def getStr(self, char='*', length=10, linebreak="\n"):
    if self.dynamic:
      keys = self.buckets.keys()
      keys.sort()
    else:
      keys = self.bucket_keys

    try:
      increments = float(length) / max(self.buckets.values())
    except (ZeroDivisionError, ValueError):
      return "Empty histogram"

    lines = []
    padding = 0
    for k in keys:
      lines.append(("%s(%d)" % (k, self.buckets[k]),
                    char * int(increments * self.buckets[k])))
      padding = max(padding, len(lines[-1][0]))

    ret = self.name + linebreak
    for l, r in lines:
      ret += l.ljust(padding) + " : " + r + linebreak
    return ret

  def getHTML(self, char='*', length=10):
    if self.dynamic:
      keys = self.buckets.keys()
      keys.sort()
    else:
      keys = self.bucket_keys

    try:
      increments = float(length) / max(self.buckets.values())
    except (ZeroDivisionError, ValueError):
      return "Empty histogram<br/>\n"

    lines = []

    for k in keys:
      lines.append(("%s(%d)" % (k, self.buckets[k]),
                    char * int(increments * self.buckets[k])))

    ret = self.name + "<br/><table border=0>\n"
    for l, r in lines:
      ret += "<tr><td>%s</td><td>: %s</td></tr>\n" % (l, r)

    return ret + "</table>"

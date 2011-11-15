import logging
import urllib2
import traceback

# Singleton opener
opener = urllib2.build_opener()
opener.addheaders = [("User-agent", "CortexBot/0.1")]

__log = logging.getLogger("Cortex.urlfetcher")

class DummyResponse:
  def read(self):
    return ""

  def readline(self):
    return ""

  def readlines(self):
    return []

  def __iter__(self):
    if False:
      yield

def fetch(url, raise_on_failure=True):
  """Fetch a url from the web"""
  try:
    __log.debug("Requesting: %s" % url)
    request = urllib2.Request(url)
    return __open(request)
  except Exception, e:
    if raise_on_failure:
      raise
    else:
      __log.info("Request for %s failed" % url)
      return DummyResponse()

def __open(request):
  """Attempt to retrieve the url"""
  numTries = 3
  for i in range(numTries):
    try:
      return opener.open(request)
    except Exception, e:
      __log.warning("Request for %s failed:\n%s" % (request.full_url,
                                                    traceback.format_exc()))
      continue
  raise

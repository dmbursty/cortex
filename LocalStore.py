import threading

class LocalStore:
  """Stores update data.
     Contains a list of per-source lists"""
  def __init__(self):
    self.latestId = 0
    self.sourceStores = []
    self.mutex = threading.Lock()

  def getNewSourceID(self):
    self.mutex.acquire()
    self.latestId += 1
    self.sourceStores.append([])
    self.mutex.release()
    return self.latestId

  def storeUpdate(self, sourceId, items):
    self.mutex.acquire()
    try:
      self.sourceStores[sourceId].extend(items)
    except Exception e:
      print "Couldn't store update: %s" % str(e)
    self.mutex.release()

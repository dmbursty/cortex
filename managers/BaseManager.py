import threading

import readers.ReaderFactory as ReaderFactory

class BaseManager (threading.Thread):
  """Base class for managers"""
  def __init__(self, id, depot):
    self.id = id
    self.mutex = threading.Lock()
    self.event = threading.Event()
    self.die = False
    self.depot = depot
    threading.Thread.__init__(self)

  def run(self):
    """Main running loop"""
    self.mutex.acquire()
    while not self.die:
      try:
        self.doWork()
      except Exception, e:
        print "Manager died unexpectedly:", e
        self.die = True
        self.event.set()
      self.mutex.release()
      # Wait for a significant event
      self.event.wait()
      self.event.clear()
      # Wait for mutex before continuing
      self.mutex.acquire()
    self.mutex.release()

  def makeReader(self, reader, args):
    """Helper method for making readers"""
    reader_class = ReaderFactory.getReader(reader)
    if (reader_class):
      return reader_class(args)
    else:
      raise Exception("Reader type not found")

  def kill(self):
    self.mutex.acquire()
    self.cleanup()
    self.die = True
    self.event.set()
    self.mutex.release()

  # Method for children to do cleanup
  def cleanup(self):
    pass

  # Children must implement this method
  def doWork(self):
    raise NotImplemented("BaseManager: You must implement doWork")


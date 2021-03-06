import logging
import threading

import readers.ReaderFactory as ReaderFactory

class BaseManager (threading.Thread):
  """Base class for managers"""
  def __init__(self, id, mixer):
    self.log = logging.getLogger("Cortex.Managers.%s" %
                                 self.__class__.__name__)
    self.id = id
    self.mutex = threading.Lock()
    self.event = threading.Event()
    self.die = False
    self.mixer = mixer
    threading.Thread.__init__(self)

  def run(self):
    """Main running loop"""
    self.mutex.acquire()
    while not self.die:
      try:
        self.doWork()
      except Exception, e:
        self.log.error("Manager died unexpectedly:", e)
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
      raise Exception("Reader type %s not found" % reader)

  def kill(self):
    self.mutex.acquire()
    self.cleanup()
    self.die = True
    self.event.set()
    self.mutex.release()

  # Method for children to do cleanup
  def cleanup(self):
    pass

  # Method for children to define their string representation
  def __str__(self):
    return "%s:%d" % (self.__class__.__name__, self.id)

  # Children must implement this method
  def doWork(self):
    raise NotImplemented("BaseManager: You must implement doWork")


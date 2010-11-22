import threading
import traceback

from BaseManager import BaseManager

class TimerManager (BaseManager):
  def __init__(self, id, depot, args):
    self.reader = self.makeReader(args['reader'], args['reader_args'])
    self.interval_secs = args['interval']
    BaseManager.__init__(self, id, depot)

  def cleanup(self):
    try:
      self.timer.cancel()
    except:
      print "No timer found at kill-time"
      pass

  def doWork(self):
    self.timer = threading.Timer(self.interval_secs, self.check)
    self.timer.start()

  def check(self):
    self.mutex.acquire()
    try:
      items = self.reader.getUpdate()
      if items:
        self.depot.update(self, items)
      self.event.set()
    except Exception, e:
      print "TimerManager died while updating"
      traceback.print_exc()
      self.die = True
      self.event.set()
    self.mutex.release()



import threading

from BaseManager import BaseManager

class TimerManager (BaseManager):
  def __init__(self, depot, args):
    self.reader = self.makeReader(args['reader'], args['reader_args'])
    self.interval_secs = args['interval']
    BaseManager.__init__(self, depot)

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
        self.depot.update(items)
      else:
        print "No update"
      self.event.set()
    except Exception, e:
      print "TimerManager died while updating:", e
      self.die = True
      self.event.set()
    self.mutex.release()



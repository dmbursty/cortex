import threading
import traceback

from BaseManager import BaseManager

class TimerManager (BaseManager):
  def __init__(self, id, mixer, args):
    self.reader = self.makeReader(args['reader'], args['reader_args'])
    self.interval_secs = int(args['interval'])
    BaseManager.__init__(self, id, mixer)

    # Get initial items
    items = self.reader.getUpdate()
    if items:
      self.mixer.update(self, items)

  def cleanup(self):
    try:
      self.timer.cancel()
    except:
      self.log.warning("No timer found at kill-time")
      pass

  def doWork(self):
    self.timer = threading.Timer(self.interval_secs, self.check)
    self.timer.start()

  def check(self):
    if self.die:
      return
    self.mutex.acquire()
    try:
      items = self.reader.getUpdate()
      if items:
        self.mixer.update(self, items)
      self.event.set()
    except Exception, e:
      self.log.error("TimerManager died while updating: %s" %
                         traceback.format_exc())
      self.die = True
      self.event.set()
    self.mutex.release()

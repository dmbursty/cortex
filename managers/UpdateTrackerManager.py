import datetime
import pytz
import threading
import traceback

from BaseManager import BaseManager

weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

class UpdateTrackerManager (BaseManager):
  def __init__(self, id, mixer, args):
    self.reader = self.makeReader(args['reader'], args['reader_args'])
    self.interval_secs = 600
    self.summary_secs = 4 * 60 * 60
    self.summary_timer = threading.Timer(self.summary_secs, self.summarize)
    self.summary_timer.start()
    self.tz = pytz.timezone("US/Eastern")
    self.lastupdate = datetime.datetime.now(self.tz)
    BaseManager.__init__(self, id, mixer)

    # Get initial items
    items = self.reader.getUpdate()

  def cleanup(self):
    try:
      self.update_timer.cancel()
      self.summary_timer.cancel()
    except:
      self.log.warning("No timer found at kill-time")

  def doWork(self):
    self.update_timer = threading.Timer(self.interval_secs, self.check)
    self.update_timer.start()

  def check(self):
    if self.die:
      return
    self.mutex.acquire()
    try:
      items = self.reader.getUpdate()
      if items:
        self.gotUpdate()
      self.event.set()
    except Exception, e:
      self.log.error("UpdateTrackerManager died while checking for update: %s" %
                         traceback.format_exc())
      self.die = True
      self.event.set()
    self.mutex.release()

  def gotUpdate(self):
    now = datetime.datetime.now(self.tz)
    delta = (now - self.lastupdate).seconds / 60
    print "Update: hour(%d) day(%s) delta(%d)" % (now.hour,
                                                  weekday_names[now.weekday()],
                                                  delta)
    self.lastupdate = now

  def summarize(self):
    print "Summarize!"
    self.summary_timer = threading.Timer(self.summary_secs, self.summarize)
    self.summary_timer.start()

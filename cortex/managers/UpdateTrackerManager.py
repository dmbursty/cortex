import datetime
import threading
import traceback

from BaseManager import BaseManager

from common.histogram import Histogram
from readers.BaseReader import BaseItem

weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday",
                 "Friday", "Saturday", "Sunday"]

class UpdateTrackerItem(BaseItem):
  def __init__(self, hists, metadata):
    # hists is a list of histograms to pull data from
    BaseItem.__init__(self, metadata)
    reader_name = metadata['reader_desc'].split(": ", 1)[0]

    self.title = "Update summary for %s reader" % reader_name
    self.html = ("Update summary for the following reader:<br/>\n" +
                 metadata['reader_desc'] +
                 "<br/><br/>\n" +
                 "<br/>\n".join([h.getHTML() for h in hists]))

    self.content = ("Update summary for the following reader:\n" +
                    metadata['reader_desc'] + "\n\n" +
                    "\n".join([h.getStr() for h in hists]))

class UpdateTrackerManager (BaseManager):
  def __init__(self, id, mixer, args):
    self.reader = self.makeReader(args['reader'], args['reader_args'])
    self.reader_desc = "%s: %s" % (args['reader'], args['reader_args'])
    self.interval_secs = int(args['check_interval'])
    self.summary_secs = int(args['summary_interval'])

    self.day_hist = Histogram("Day of the week", weekday_names)
    self.hour_hist = Histogram("Hour of the day", range(24))
    self.delta_hist = Histogram("Time between updates (min)")

    self.summary_timer = threading.Timer(self.summary_secs, self.summarize)
    self.summary_timer.start()
    self.lastupdate = None
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
    now = datetime.datetime.now()
    self.day_hist.add(weekday_names[now.weekday()])
    self.hour_hist.add(now.hour)

    if self.lastupdate is not None:
      delta = (now - self.lastupdate).seconds / 60
      self.delta_hist.add(delta)

    self.lastupdate = now

  def summarize(self):
    hists = [self.day_hist, self.hour_hist, self.delta_hist]
    item = UpdateTrackerItem(hists, {'reader_desc': self.reader_desc})
    self.mixer.update(self, [item])
    self.summary_timer = threading.Timer(self.summary_secs, self.summarize)
    self.summary_timer.start()

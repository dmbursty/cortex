#!/usr/bin/python

import time
import threading

from RPCServer import RPCServer

from sources.HardCodeSource import HardCodeSource
from sources.TestSource import TestSource

SourceFactory = TestSource

class Controller:
  def __init__(self, sources):
    self.readers = []
    self.mutex = threading.Lock()

    self.rpc_server = RPCServer(self)
    self.rpc_server.start()
    time.sleep(1) # Wait for the rpc server to start

    for source in sources:
      reader = TimedReaderContainer(source['class'](source['args']),
                                      source['interval'], self)
      self.readers.append(reader)

    for reader in self.readers:
      reader.start()

  def foundUpdate(self, items):
    self.mutex.acquire()
    # Filtering to summaries here instead of in containers
    # for testing, so I don't get a screenful of data
    print "Found an update:"
    print items[0].toSummary()
    self.mutex.release()

  # This comes from the RPC Server
  def kill(self):
    self.mutex.acquire()
    for reader in self.readers:
      reader.kill()
    self.rpc_server.kill()
    self.mutex.release()

class TimedReaderContainer (threading.Thread):
  def __init__(self, reader, interval_secs, controller):
    self.reader = reader
    self.interval_secs = interval_secs
    self.event = threading.Event()
    self.timer = None
    self.mutex = threading.Lock()
    self.die = False
    threading.Thread.__init__(self)

  def run(self):
    self.mutex.acquire()
    while not self.die:
      self.event.clear()
      self.timer = threading.Timer(self.interval_secs, self.check)
      self.timer.start()
      self.mutex.release()
      self.event.wait()
      self.mutex.acquire()
    self.mutex.release()

  def kill(self):
    self.mutex.acquire()
    if self.timer is not None:
      self.timer.cancel()
    self.die = True
    self.event.set()
    self.mutex.release()

  def check(self):
    self.mutex.acquire()
    if self.reader.checkForUpdate():
      controller.foundUpdate(self.reader.getItems())
    else:
      print "No update"
    self.event.set()
    self.mutex.release()


if __name__ == "__main__":
  source = SourceFactory()
  controller = Controller(source.getSources())

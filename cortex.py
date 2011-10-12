#!/usr/bin/python

import logging
import logging.config
import sys
import time
import threading

from Controller import Controller
from RPCServer import RPCServer
from ConfigLoader import ConfigLoader

if __name__ == "__main__":
  # Set up logging
  logging.config.fileConfig("cortex_logging.conf")
  # Wish there was a better way around this, but logging is causing IOErrors
  logging.raiseExceptions = False

  controller = Controller()
  if len(sys.argv) > 1:
    rpc_server = RPCServer(controller, str(sys.argv[1]))
    if len(sys.argv) > 2:
      configer = ConfigLoader(rpc_server)
      configer.parseXML(sys.argv[2])
  else:
    rpc_server = RPCServer(controller)
  rpc_server.start()

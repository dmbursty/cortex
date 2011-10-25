#!/usr/bin/python

import script_init

import logging
import logging.config
import sys
import time
import threading

from cortex.Controller import Controller
from cortex.RPCServer import RPCServer
from cortex.ConfigLoader import ConfigLoader

# Set up logging
logging.config.fileConfig("logs/configs/cortex_logging.conf")
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

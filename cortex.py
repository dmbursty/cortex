#!/usr/bin/python

import sys
import time
import threading

from Controller import Controller
from RPCServer import RPCServer

if __name__ == "__main__":
  controller = Controller()
  if len(sys.argv) > 1:
    rpc_server = RPCServer(controller, str(sys.argv[1]))
  else:
    rpc_server = RPCServer(controller)
  rpc_server.start()

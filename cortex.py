#!/usr/bin/python

import time
import threading

from Controller import Controller
from RPCServer import RPCServer

if __name__ == "__main__":
  controller = Controller()
  rpc_server = RPCServer(controller)
  rpc_server.start()

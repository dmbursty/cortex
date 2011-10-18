#!/usr/bin/python

import script_init

import cmd
import os
import socket
import subprocess
import sys
import time
import traceback
import xmlrpclib

from cortex.registry.Registry import Registry

# Decorator for interface functions that attempt RPC calls
def netcall(f):
  def wrap(*args, **kwargs):
    try:
      return f(*args, **kwargs)
    except xmlrpclib.Fault, e:
      print e
    except socket.error, e:
      print "'%s' error in function %s()" % (e[1], f.__name__)
      print "Shutting down..."
      return True
  return wrap


class CortexCLI(cmd.Cmd):
  def __init__(self, name, port):
    cmd.Cmd.__init__(self)
    self.prompt = "%s >>> " % name

    # Connect to cortex
    self.server = xmlrpclib.ServerProxy("http://localhost:%d" % port)

  def cmdloop(self, intro=""):
    # Check that the system is actually running
    try:
      self.server.ping()
      cmd.Cmd.cmdloop(self, intro)
    except socket.error, e:
      if e[1] == "Connection refused":
        print "Server not running, aborting..."
      return

  @netcall
  def do_ping(self, line):
    print self.server.ping()

  @netcall
  def do_kill(self, line):
    print self.server.kill()
    return self.do_exit("")

  @netcall
  def do_steam(self, line):
    print self.server.addManager("TimerManager",
                                 {'interval': 600,
                                  'reader': 'SteamSale',
                                  'reader_args':  {},
                                 })

  # Utility functions
  def do_exit(self, line):
    print "\nGoodbye!"
    return True

  def do_EOF(self, line):
    return self.do_exit(line)


class RegistryCLI(cmd.Cmd):
  # Base class overrides
  def __init__(self, server=None):
    cmd.Cmd.__init__(self)
    self.prompt = ">>> "

    # Connect to the registry
    self.registry = xmlrpclib.ServerProxy("http://localhost:%d" % Registry.SERVER_PORT)

    # Check if a registry is running
    try:
      self.registry.ping()
    except socket.error, e:
      if e[1] == "Connection refused":
        print "No registry found, starting a new one"
        subprocess.Popen(["python", "registry.py"])

    if server is not None:
      self.do_connect(server)

  @netcall
  def do_stop(self, line):
    clients = self.registry.get_clients()
    if not clients.has_key(line):
      print "No cortex server found with that name (%s)" % line
      return False

    try:
      client = xmlrpclib.ServerProxy("http://localhost:%d" % clients[line])
      print client.kill()
    except socket.error:
      print "Could not connect to cortex server %s. Try refreshing." % line

  @netcall
  def do_start(self, line):
    """Start a new cortex server"""

    if not line:
      line = "cortex"

    # First, check that the name isn't already taken
    clients = self.registry.get_clients()
    if clients.has_key(line):
      print "A server already exists with that name (%s)" % line
      return False

    subprocess.Popen(["python", "cortex.py", line])
    # Wait for the system to init
    time.sleep(1)
    print "Started server, connecting..."
    return self.do_connect(line)
    

  # Registry function wrappers
  @netcall
  def do_refresh(self, line):
    print self.registry.refresh()
    self.do_clients('')

  def do_kill(self, line):
    print "Killing the registry can cause several errors, if you are sure use killkill"

  @netcall
  def do_killkill(self, line):
    """Kills the registry"""
    print self.registry.kill()
    return self.do_exit("")

  @netcall
  def do_ping(self, line):
    print self.registry.ping()

  @netcall
  def do_clients(self, line):
    print self.registry.get_clients()

  @netcall
  def do_ls(self, line):
    self.do_clients(line)

  @netcall
  def do_badcall(self, line):
    print self.registry.nonexistant_function()

  @netcall
  def do_connect(self, line):
    clients = self.registry.get_clients()
    try:
      port = clients[line]
    except KeyError, e:
      print "Client not found: %s" % line
      return False

    try:
      CortexCLI(line, port).cmdloop()
    except Exception, e:
      print "Unhandled exception in cortex system %s" % line
      traceback.print_exc()

  @netcall
  def do_shutdown(self, line):
    self.registry.refresh()
    clients = self.registry.get_clients()
    for name, port in clients.items():
      print "Stopping server %s" % name
      self.do_stop(name)
    print "Killing registry"
    print self.registry.kill()
    return self.do_exit('')


  # Utility functions
  def do_exit(self, line):
    print "\nGoodbye!"
    return True

  def do_EOF(self, line):
    return self.do_exit(line)


if __name__ == "__main__":
  if len(sys.argv) > 1:
    # Connect to given server right away
    RegistryCLI(sys.argv[1]).cmdloop()
  else:
    RegistryCLI().cmdloop()

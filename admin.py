import cmd
import socket
import sys
import traceback
import xmlrpclib

from Registry import Registry

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

    if server is not None:
      self.do_connect(server)

  # Registry function wrappers
  def do_kill(self, line):
    print "Killing the registry can cause several errors, if you are sure use killkill"

  @netcall
  def do_killkill(self, line):
    print self.registry.kill()

  @netcall
  def do_ping(self, line):
    print self.registry.ping()

  @netcall
  def do_clients(self, line):
    print self.registry.get_clients()

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

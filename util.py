#!/usr/bin/python

import sys
import socket
import traceback
import xmlrpclib

if len(sys.argv) != 2:
  print "Found %d arguments.  Expected 1" % (len(sys.argv) - 1)

try:
  server = xmlrpclib.ServerProxy("http://localhost:9047")
  if sys.argv[1] == 'kill':
    print server.kill()
  elif sys.argv[1] == 'killone':
    name, port = server.get_clients().popitem()
    s = xmlrpclib.ServerProxy("http://localhost:%d" % port)
    print s.kill()
  elif sys.argv[1] == 'killall':
    c = server.get_clients()
    for name, port in c.iteritems():
      s = xmlrpclib.ServerProxy("http://localhost:%d" % port)
      print s.kill()
  elif sys.argv[1] == 'clear':
    c = server.get_clients()
    for name, port in c.iteritems():
      print server.unregister(name, port)
  elif sys.argv[1] == 'test':
    #print server.addManager("TimerManager",
                            #{'interval': 600,
                             #'reader': 'RSS',
                             #'reader_args': 
        #{'source':"http://feeds.gawker.com/kotaku/full"},
                            #})
    #print server.addManager("TimerManager",
                            #{'interval': 600,
                             #'reader': 'Atom',
                             #'reader_args': 
        #{'source':"http://feeds2.feedburner.com/fmylife"},
                            #})
    print server.addManager("TimerManager",
                            {'interval': 600,
                             'reader': 'SteamSale',
                             'reader_args':  {},
                            })
  elif sys.argv[1] == 'hello':
    print server.get_clients()
  else:
    print "Unrecognized argument: %s" % sys.argv[1]
except socket.error, e:
  print "Connection error: %s" % e
except Exception, e:
  traceback.print_exc()

#!/usr/bin/python

import sys
import socket
import traceback
import xmlrpclib

if len(sys.argv) != 2:
  print "Found %d arguments.  Expected 1" % (len(sys.argv) - 1)

try:
  server = xmlrpclib.ServerProxy("http://localhost:8000")
  if sys.argv[1] == 'kill':
    server.kill()
  elif sys.argv[1] == 'test':
    print server.addManager("TimerManager",
                            {'interval': 600,
                             'reader': 'RSS',
                             'reader_args': 
        {'source':"http://feeds.gawker.com/kotaku/full"},
                            })
    print server.addManager("TimerManager",
                            {'interval': 600,
                             'reader': 'Atom',
                             'reader_args': 
        {'source':"http://feeds2.feedburner.com/fmylife"},
                            })
  else:
    print "Unrecognized argument: %s" % sys.argv[1]
except socket.error, e:
  print "Connection error: %s" % e
except Exception, e:
  traceback.print_exc()

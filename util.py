#!/usr/bin/python

import sys
import xmlrpclib

if len(sys.argv) == 2:
  if sys.argv[1] == 'kill':
    server = xmlrpclib.ServerProxy("http://localhost:8000")
    server.kill()
  else:
    print "Unrecognized argument: %s" % sys.argv[1]
else:
  print "Found %d arguments.  Expected 1" % (len(sys.argv) - 1)

#!/usr/bin/python

import sys
import xmlrpclib

if len(sys.argv) != 2:
  print "Found %d arguments.  Expected 1" % (len(sys.argv) - 1)

server = xmlrpclib.ServerProxy("http://localhost:8000")
if sys.argv[1] == 'kill':
  server.kill()
elif sys.argv[1] == 'test':
  print server.addManager("TimerManager",
                          {'interval': 60,
                           'reader': 'SimpleWebsite',
                           'reader_args': 
      {'source':"http://www.qwantz.com/index.php",
       #'regex':".*"
       #'regex':"<img src=\"http://www.qwantz.com/comics/.*?\" " + \
               #"class=\"comic\" title=\".*?\">"
       },
                           })
else:
  print "Unrecognized argument: %s" % sys.argv[1]

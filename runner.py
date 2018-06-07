#!/usr/bin/python
import os, sys

log_file = 'py_ns3_visualizer.log'

# Remove log file
if os.path.exists (log_file):
  os.system ('rm %s' % log_file)

if len (sys.argv) == 2 and sys.argv[1] == 'help': #not in [1, 2, 3]:
  print 'Usage: runner [<events.log>] [<interval>]'
  sys.exit (0)

if len (sys.argv) >= 2:
  events_log = sys.argv[1]
else:
  # Pick any link state periodic
  os.system ('find traces/ -name "events.log" | head -1 > tmp.txt')
  events_log = open ('tmp.txt', 'r').readline ().strip ()
  os.system ('rm tmp.txt')

if not os.path.exists (events_log):
  print 'File does not exist:', events_log
  sys.exit (0)

if len (sys.argv) >= 3:
  interval = sys.argv[2]
else:
  interval = '500'


sys.argv = [sys.argv[0], events_log, 'styles/node-styles010', 'styles/link-styles010', interval]
sys.path.append ('src')
from ns3.rapidnet.rapidnet_visualizer import main
main ()


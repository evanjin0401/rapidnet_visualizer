import sys
import ns3
from ns3.model.net_world_model import *
from ns3.rapidnet.model.rapidnet_world_model import *
from ns3.rapidnet.model.rapidnet_world_model import PointType, \
  RapidNetWorldPointEvent, GraphSpec, LabelSpec

ip_lookup = {}

def LoadLog (model, filename):
  ns3.logging.debug ('Log file: %s' % filename)

  try:
    file = open (filename, 'r')
    linecount = 0
    for line in file:
      linecount += 1
      if line.strip () == '':
        continue
      try:
        tokens = line.split (' ')
        if tokens[0] == 'arena':
          left = int (tokens [1])
          right = int (tokens [2])
          top = int (tokens [3])
          bottom = int (tokens [4])
          model.SetArenaBounds (left, top, right, bottom)
        if tokens[0] == 'info':
          if tokens[1] == 'graph':
            type = PointType.Lookup[tokens[2]]
            model.graphSpecs[type] = GraphSpec (type, tokens[3:])
          elif tokens[1] == 'label':
            model.labelSpecs[tokens[2]] = LabelSpec (tokens[2:])
          else:
            ns3.logging.error ("Parse error in line %d, info command. " \
                              "Unknown info type '%s'." % linecount, tokens[1])
            
        else:
          event = None
          time = float (tokens[0].strip ('nms'))
          if tokens[0].endswith ('ns'):
            time = time / 1000000.0
          elif tokens[0].endswith ('s'):
            time = time * 1000.0
          # else: #ms is millisecond so nothing to do

          if tokens[1] == 'position':
            if len (tokens) < 9:
              ns3.logging.error ("Parse error in line %d, position command " \
                                 "with not enough arguments." % linecount)
              continue
            id = int (tokens [2])
            x = float (tokens [3])
            y = float (tokens [4])
            z = float (tokens [5])
            xv = float (tokens [6])
            yv = float (tokens [7])
            zv = float (tokens [8])
            event = NetWorldPositionEvent (time, id, x, y, z, xv, yv, zv)

          elif tokens[1] == 'ip':
            if len (tokens) < 4:
              ns3.logging.error ("Parse error in line %d, ip command " \
                                 "with not enough arguments." % linecount)
              continue
            id = int (tokens [2])
            ip = tokens[3].strip ()
            ip_lookup[ip] = id
            event = NetWorldIPEvent (time, id, ip)
            

          elif tokens[1] == 'link':
            if len (tokens) < 5:
              ns3.logging.error ("Parse error in line %d, link command " \
                                 "with not enough arguments." % linecount)
              continue
            if tokens[4][0] != '+' and tokens[4][0] != '-':
              ns3.logging.error ("Parse error in line %d, link command "\
                                 "with bad style." % linecount)
              continue
            id = int (tokens [2])
#            event = RapidNetWorldTupleEvent (time, id, 'tLSU',
#              tokens[4][0] == '+', (id, ip_lookup [tokens[3].strip ()]))
#            print event
#            model.PushEvent (event)
            
            event = NetWorldLinkStateEvent (time, id, tokens[3].strip (), \
              tokens[4][0] == '+', tokens[4][1:].strip ())

          elif tokens[1] == 'state':
            if len (tokens) < 4:
              ns3.logging.error ("Parse error in line %d, state command "\
                                 "with not enough arguments." % linecount)
              continue
            if tokens[3][0] != '+' and tokens[3][0] != '-':
              ns3.logging.error ("Parse error in line %d, state command "\
                                 "with bad style." % linecount)
              continue
            id = int (tokens [2])
            event = NetWorldNodeStateEvent (time, id, tokens[3][0] == '+', \
              tokens[3][1:].strip ())
          
          # Code added for RapidNet
          elif tokens[1] == 'point':
            if len (tokens) < 4:
              ns3.logging.error ("Parse error in line %d, point command " \
                                 "with not enough arguments." % linecount)
              continue
            try:
              point_type = PointType.Lookup [tokens[2]]
            except KeyError:
              ns3.logging.warn ("Parse error in line %d, point command " \
                                 "with unknown type '%s'" % (linecount, tokens[2]))
              continue
            value = float (tokens [3])
            event = RapidNetWorldPointEvent(time, point_type, value)

          elif tokens[1] == 'tuple':
            from ns3.rapidnet.model.rapidnet_world_model import \
              RapidNetWorldTupleEvent
            
            if tokens[3][0] != '+' and tokens[3][0] != '-':
              ns3.logging.error ("Parse error in line %d, tuple command "\
                                 "missing +/- symbol in tuple name." % linecount)
              continue

            if tokens[3][1:] == 'tLSU':
              if len (tokens) < 5:
                ns3.logging.error ("Parse error in line %d, tuple tLSU command " \
                                   "with not enough arguments." % linecount)
                continue
              else:
                id = int (tokens[2])
                src = ip_lookup [tokens[4].strip ().partition (':')[2]]
                next = ip_lookup [tokens[5].strip ().partition (':')[2]]
                data = (id, src, next)
                event = RapidNetWorldTupleEvent (time, id, 'tLSU', tokens[3][0] == '+', \
                                                 data)
            else:
              ns3.logging.warning ("Log line %d, uknown tuple command '%s'." \
                                 % (linecount, tokens[3][1:]))
              continue
            
          # End of code added for RapidNet
          else:
            ns3.logging.warn ("Log line %d: Unknown event '%s'" % (linecount, tokens[1]))

          if event != None:
            ns3.logging.debug ("Log line %d: %s" % (linecount, event))
            model.PushEvent (event)

      except ValueError:
        ns3.logging.error ("Parse error in log line %d: '%s'" % (linecount, sys.exc_info ()[1]))

  except IOError:
    ns3.logging.error ("Could not open log file %s for read." % filename)

#model = NetWorldModel ()
#LoadLog(model, '../../../decorator.log')

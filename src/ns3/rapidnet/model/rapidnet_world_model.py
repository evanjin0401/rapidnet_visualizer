'''
Created on Jul 4, 2009

@author: shivkumar
'''

from ns3.model.net_world_model import NetWorldEvent, NetWorldModel
from ns3.rapidnet.model.rapidnet_world_node import RapidNetWorldNode

class PointType:
  Default = -1
  BandwidthSent = 0
  LossRate = 1
  Validity = 2
  Stretch = 3
  LinkEvent = 4
  tMessage = 5


  Values = [BandwidthSent, LossRate, Validity, Stretch, LinkEvent, tMessage]

  Lookup = { 'sent': BandwidthSent,
             'loss': LossRate,
             'validity': Validity,
             'stretch': Stretch,
             'linkevent': LinkEvent,
             'tmessage': tMessage
            }

  Lookdown = { BandwidthSent: 'sent',
               LossRate: 'loss',
               Validity: 'validity',
               Stretch: 'stretch',
               LinkEvent: 'linkevent',
               tMessage: 'tmessage'
              }

class GraphSpec:

  def __init__ (self, type, tokens):
    self.type = type
    self.title = tokens[0].replace ('_', ' ')
    self.xlabel = 'X Label'
    self.ylabel = 'Y Label'
    self.xlower = int (tokens[1])
    self.xupper = int (tokens[2])
    self.ylower = float (tokens[3])
    self.yupper = float (tokens[4])
    self.position = int (tokens[5]) - 1

    if self.type == PointType.LossRate:
      self.yupper = 100

    #Small hack
    if self.yupper == self.ylower:
      self.yupper = 10 # Pick a default value

    
class LabelSpec:
  
  def __init__ (self, tokens):
    self.type = tokens[0]
    self.name = tokens[1].replace ('_', ' ')
    self.value = tokens[2].replace ('_', ' ')
    self.text = self.name + ': ' + self.value
    self.position = int (tokens[3]) - 1

class RapidNetWorldPointEvent (NetWorldEvent):

  def __init__ (self, timestamp, type, value):
    NetWorldEvent.__init__(self, timestamp)
    self.type = type
    self.value = value

  def __repr__ (self):
    return "RapidNetWorldPointEvent (timestamp=%.3f, type=%s, value=%d)" % \
      (self.timestamp, PointType.Lookdown [self.type], self.value)

  def Process (self, rapidNetWorldModel):
    rapidNetWorldModel.AddPoint (self)


class RapidNetWorldTupleEvent (NetWorldEvent):
  Inserted = 1
  Deleted = 2

  EventLookup = {Inserted: 'inserted', Deleted: 'deleted'}

  def __init__ (self, timestamp, node, name, inserted, data):
    NetWorldEvent.__init__(self, timestamp)
    self.node = node
    self.name = name
    self.data = data
    if inserted:
      self.event = RapidNetWorldTupleEvent.Inserted
    else:
      self.event = RapidNetWorldTupleEvent.Deleted
    self.inserted = inserted

  def __repr__ (self):
    return "RapidNetWorldTupleEvent (timestamp=%.3f, node=%s, name=%s, event=%s, data=%s)" % \
      (self.timestamp, self.node, self.name, RapidNetWorldTupleEvent.EventLookup [self.event],
       self.data)

  def Process (self, rapidNetWorldModel):
    if self.event == RapidNetWorldTupleEvent.Inserted:
      rapidNetWorldModel.AddTuple (self.node, self.name, self.data)
    else:
      rapidNetWorldModel.RemoveTuple (self.node, self.name, self.data)


class RapidNetWorldModel (NetWorldModel):

  def __init__ (self):
    NetWorldModel.__init__(self)
    self.labelSpecs = {}
    self.graphSpecs = {}
    self.points = {}
    for type in PointType.Values:
      self.points[type] = ([], [])
      
  def GetLabelText (self, name):
    if name in self.labelSpecs:
      return self.labelSpecs[name].value
    else:
      return ''

  def AddPoint (self, point):
    self.points[point.type][0].append (point.timestamp / 1000.0)
    self.points[point.type][1].append (point.value)

  def Clear (self):
    NetWorldModel.Clear(self)
    for type in PointType.Values:
      self.points[type] = ([], [])

  def GetPoints (self, type):
    return self.points[type]

  def GetNode (self, id):
    if id not in self.nodes:
      node = RapidNetWorldNode(id)
      self.nodes[id] = node
      return node
    else:
      return self.nodes [id]

  def AddTuple (self, node, name, data):
    node_obj = self.GetNode(node)
    node_obj.AddTuple (name, data)

  def RemoveTuple (self, node, name, data):
    node_obj = self.GetNode(node)
    node_obj.RemoveTuple(name, data)

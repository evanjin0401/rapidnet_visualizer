import ns3
from ns3.model.net_world_node import NetWorldNode

class NetWorldEvent:

  def __init__ (self, timestamp):
    self.timestamp = timestamp

  def Process (self, netWorldModel):
    pass



class NetWorldIPEvent (NetWorldEvent):

  def __init__ (self, timestamp, id, ip):
    NetWorldEvent.__init__(self, timestamp)
    self.node = id
    self.ip = ip

  def Process (self, netWorldModel):
    ns3.logging.debug ("Bind ip for %d to %s" % (self.node, self.ip))
    netWorldModel.MapIP (self.ip, self.node)

  def __repr__ (self):
    return "NetWorldIPEvent (timestamp=%.3f, node=%d, ip='%s')" % \
      (self.timestamp, self.node, self.ip)


class NetWorldPositionEvent (NetWorldEvent):

  def __init__ (self, timestamp, id, x, y, z, xv, yv, zv):
    NetWorldEvent.__init__(self, timestamp)
    self.node = id
    self.x = x
    self.y = y
    self.z = z
    self.xvel = xv
    self.yvel = yv
    self.zvel = zv

  def Process (self, netWorldModel):
    netWorldModel.SetPosition (self.node, self.timestamp, \
                               self.x, self.y, self.z, self.xvel, \
                               self.yvel, self.zvel)

  def __repr__ (self):
    return "NetWorldPositionEvent (timestamp=%.3f, node=%d, x=%.2f, y=%.2f, xvel=%.2f, yvel=%.2f)" % \
      (self.timestamp, self.node, self.x, self.y, self.xvel, self.yvel)

class NetWorldLinkStateEvent (NetWorldEvent):

  def __init__ (self, timestamp, id, target, link, state):
     NetWorldEvent.__init__(self, timestamp)
     self.node = id
     self.target = target
     self.link = link
     self.state = state

  def Process (self, netWorldModel):
    if self.link:
      ns3.logging.debug ("Add state %s to link %d -> %s" % \
                         (self.state, self.node, self.target))
      netWorldModel.AddLinkState (self.node, self.target, self.state)
    else:
      ns3.logging.debug ("Remove state %s to link %d -> %s" % \
                         (self.state, self.node, self.target))
      netWorldModel.RemoveLinkState (self.node, self.target, self.state)

  def __repr__ (self):
    return "NetWorldLinkStateEvent (timestamp=%.3f, node=%d, target='%s', link=%s, state=%s)" % \
      (self.timestamp, self.node, self.target, self.link, self.state) 

class NetWorldNodeStateEvent (NetWorldEvent):

  def __init__ (self, timestamp, id, add, state):
    NetWorldEvent.__init__(self, timestamp)
    self.node = id
    self.add = add
    self.state = state

  def Process (self, netWorldModel):
    # Defining the node state 'Clear' as a keyword
    # that clears all states in the node
    if self.state == 'Clear':
      ns3.logging.debug ("Clear states of %d" % (self.node))
      netWorldModel.ClearNodeState (self.node)
    if self.add:
      ns3.logging.debug ("Add state %s to %d" % (self.state, self.node))
      netWorldModel.AddNodeState (self.node, self.state)
    else:
      ns3.logging.debug ("Remove state %s to %d" % (self.state, self.node))
      netWorldModel.RemoveNodeState (self.node, self.state)

  def __repr__ (self):
    return "NetWorldNodeStateEvent (timestamp=%.3f, node=%d, add=%s, state=%s)" % \
      (self.timestamp, self.node, self.add, self.state)

class NetWorldModel:

  def __init__ (self):
    self.left = 0
    self.bottom = 0
    self.right = 400
    self.top = 400
    self.nodes = {}
    self.ips = {}
    self.events = []
    self.currentEvent = -1

  def __del (self):
    self.Clear ()

  def Clear (self):
     self.nodes.clear()
     self.ips.clear()

  def SetArenaBounds(self, x1, x2, y1, y2):
    if x1 <= x2:
      self.left = x1
      self.right = x2
    else:
      self.left = x2
      self.right = x1

    if y1 <= y2:
      self.bottom = y1
      self.top = y2
    else:
      self.bottom = y2
      self.top = y1

    ns3.logging.debug ("bounds %d, %d --- %d, %d" % \
                       (self.left, self.bottom, self.right, self.top))

  def PushEvent (self, event):
    self.events.append(event)

  def Start (self):
    self.Clear()
    self.currentEvent = 0

  def End (self):
    return self.currentEvent >= len (self.events)

  def ProcessUpTo (self, timestamp):
    #ns3.logging.debug("Bound %d" % timestamp)
    while not self.End() and self.events[self.currentEvent].timestamp <= timestamp:
      self.events[self.currentEvent].Process (self)
      self.currentEvent += 1

  def GetLastTimestamp (self):
    if len (self.events) <= 0:
      return 0
    else:
      return self.events[len (self.events) - 1].timestamp

  def GetNode (self, id):
    if id not in self.nodes:
      node = NetWorldNode(id)
      self.nodes[id] = node
      return node
    else:
      return self.nodes [id]

  def GetNodeByIP (self, ip):
    if ip in self.ips:
      return self.ips [ip]
    else:
      return None

  def MapIP (self, ip, nodeId):
    ns3.logging.debug ("Map %s -> %d" % (ip, nodeId))
    node = self.GetNode(nodeId)
    if ip in self.ips:
      ns3.logging.warn ("Warning: IP %s already points to node %d" \
                        (ip, self.ips[ip]))
    node.AddIP(ip)
    self.ips[ip] = node

  def SetPosition (self, nodeId, time, x, y, z, xv, yv, zv):
    node = self.GetNode(nodeId)
    node.SetPosition(x, y, time, xv, yv)

  def AddLinkState (self, nodeId, target, state):
    ns3.logging.debug ("Add link state %s to %d -> %s" % (state, nodeId, target))
    node = self.GetNode(nodeId)
    node.AddLinkState(target, state)

  def RemoveLinkState (self, nodeId, target, state):
    ns3.logging.debug ("Remove link state %s from %d -> %s" % (state, nodeId, target))
    node = self.GetNode(nodeId)
    node.RemoveLinkState(target, state)

  def AddNodeState (self, nodeId, state):
    ns3.logging.debug ("Add state %s to %d" % (state, nodeId))
    node = self.GetNode (nodeId)
    node.AddNodeState (state)

  def RemoveNodeState (self, nodeId, state):
    ns3.logging.debug ("Remove state %s from %d" % (state, nodeId))
    node = self.GetNode (nodeId)
    node.RemoveNodeState (state)

  def ClearNodeState (self, nodeId):
    ns3.logging.debug ("Clear state for %d" % (nodeId))
    node = self.GetNode (nodeId)
    node.ClearNodeState ()


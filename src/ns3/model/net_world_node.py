import ns3

class NetWorldNode:

  def __init__ (self, id):
    self.id = id
    self.hasPosition = False
    self.x = 0.0
    self.y = 0.0
    self.xvel = 1.0
    self.yvel = 1.0
    self.positionTimestamp = 0.0
    self.ips = []
    self.links = {}
    self.states = []#set ()

  def __repr__ (self):
    return "NetWorldNode (id=%d, x=%.2f, y=%.2f, xvel=%.2f, yvel=.2f, " \
      "timestamp=%.3f, ips=%s, links=%s, states=%s)" % (self.id, self.x, \
      self.y, self.xvel, self.yvel, self.positionTimestamp, self.ips, \
      self.links, self.states)

  def GetPosition (self, time):
    diff = float (time) - self.positionTimestamp
    fract = float (diff) / 1000.0
    x = self.x + (fract * self.xvel)
    y = self.y + (fract * self.yvel)
    return (self.hasPosition, x, y)

  def SetPosition (self, x, y, tstamp, xvel = 0, yvel = 0):
    self.hasPosition = True
    self.x = x
    self.y = y
    self.positionTimestamp = tstamp
    self.xvel = xvel
    self.yvel = yvel

  def AddIP (self, ip):
    self.ips.append(ip)

  def GetID (self):
    return self.id

  def AddLinkState (self, ip, state):
    if ip not in self.links:
      self.links[ip] = set ()
    self.links[ip].add (state)

  def RemoveLinkState (self, ip, state):
    if ip in self.links:
      if state in self.links[ip]:
        self.links[ip].remove(state)

  def AddNodeState (self, state):
    ns3.logging.debug ("Node %d adding state %s" % (self.id, state))
    self.states.append (state)

  def RemoveNodeState (self, state):
    ns3.logging.debug ("Node %d removing state %s" % (self.id, state))
    self.states.remove (state)

  def ClearNodeState (self):
    ns3.logging.debug ("Node %d clearing state" % (self.id))
    self.states = []#.clear ()


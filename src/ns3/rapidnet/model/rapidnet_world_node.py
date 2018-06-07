'''
Created on Jul 6, 2009

@author: shivkumar
'''

import ns3
from ns3.model.net_world_node import NetWorldNode
from ns3.rapidnet.algorithms.build_routing_table import getRoutingTable

class RapidNetWorldNode (NetWorldNode):

  def __init__ (self, id):
    NetWorldNode.__init__(self, id)
    self.database = {}
    self.database['tLSU'] = []

  def AddTuple (self, name, data):
    if data in self.database [name]:
      ns3.logging.warning("AddTuple: Node %d already has a '%s' tuple with data %s" % \
                          (self.id, name, data))
    else:
      self.database [name].append(data)
      #print 'Node %d: AddTuple %s%s' % (self.id, name, data)

  def RemoveTuple (self, name, data):
    if data not in self.database[name]:
      ns3.logging.warning ("RemoveTuple: Node %d does not have a '%s' tuple with data %s" % \
                          (self.id, name, data))
    else:
      self.database [name].remove(data)
      #print 'Node %d: Remove %s%s' % (self.id, name, data)

  def GetRoutingTable (self):
    name = 'tLSU'
    if name not in self.database:
      ns3.logging.error ("GetTableAsString: Node %d has no table with name '%s'." % \
                          (self.id, name))
      return ''
    graph = {}
    for tLSU in self.database[name]:
      if tLSU[1] not in graph:
        graph[tLSU[1]] = {}
      if tLSU[2] not in graph:
        graph[tLSU[2]] = {}
      graph[tLSU[1]][tLSU[2]] = 1
    try:
      routingTable = getRoutingTable(graph, self.id)
    except KeyError:
      print 'KeyError while computing routing table, skipping...'
      return 'RapidNet'
    keys = routingTable.keys()
    keys.sort ()
    retval = 'Routing Table\nNode %d\nDest : NextHop\n' % self.id
    for key in keys:
      retval += '%6d  : %d\n' % (key, routingTable[key][0])
    return retval.strip ()



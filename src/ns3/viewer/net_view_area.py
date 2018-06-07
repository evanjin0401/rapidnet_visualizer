import math, sys
import gtk, cairo
import ns3
from animation_model import AnimationNotifier
from ns3.viewer.link_style import LinkStyle
from ns3.viewer.node_style import NodeStyle, NodeShape

class RenderUtils:

  def DrawNode (self, cr, x, y, nodeStyle, id = None):
    cr.save()
    if nodeStyle.shape == NodeShape.SQUARE:
      cr.move_to (x - nodeStyle.radius, y - nodeStyle.radius)
      cr.line_to (x - nodeStyle.radius, y + nodeStyle.radius)
      cr.line_to (x + nodeStyle.radius, y + nodeStyle.radius)
      cr.line_to (x + nodeStyle.radius, y - nodeStyle.radius)
      cr.close_path ()
    else: #nodeStyle.shape == NodeShape.CIRCLE:
      cr.arc (x, y, nodeStyle.radius, 0, 2 * math.pi)    

    cr.set_source_rgba (nodeStyle.r, nodeStyle.g, nodeStyle.b, nodeStyle.a)
    cr.set_line_width (nodeStyle.lineWidth)

    if id != None:
      #cr.set_source_rgba (1, 0, 0, 0)
      cr.show_text (str(id))
    
    cr.fill_preserve ()
    cr.set_source_rgba (nodeStyle.lr, nodeStyle.lg, nodeStyle.lb, nodeStyle.la)
    cr.stroke ()

    if nodeStyle.double:
      if nodeStyle.shape == NodeShape.SQUARE:
        cr.move_to (x - nodeStyle.radius - nodeStyle.lineWidth * 2, \
            y - nodeStyle.radius - nodeStyle.lineWidth * 2)
        cr.line_to (x - nodeStyle.radius - nodeStyle.lineWidth * 2, \
            y + nodeStyle.radius + nodeStyle.lineWidth * 2)
        cr.line_to (x + nodeStyle.radius + nodeStyle.lineWidth * 2, \
            y + nodeStyle.radius + nodeStyle.lineWidth * 2)
        cr.line_to (x + nodeStyle.radius + nodeStyle.lineWidth * 2, \
            y - nodeStyle.radius - nodeStyle.lineWidth * 2)
        cr.close_path ()

      else: #if nodeStyle.shape == NodeShape.CIRCLE
        cr.arc (x, y, nodeStyle.radius + nodeStyle.lineWidth \
            * 2, 0, 2 * math.pi)
      cr.stroke ()

    cr.restore()
    
    #if id != None:
    #  cr.save ()
    #  cr.move_to (x - nodeStyle.radius/2, y + nodeStyle.radius)
    #  cr.show_text (str (id))
    #  cr.stroke ()
    #  cr.restore ()

class NetViewArea (gtk.DrawingArea, AnimationNotifier):

  __gsignals__ = { "expose-event": "override" }

  def __init__ (self):
    gtk.DrawingArea.__init__(self)
    self.__model = None
    self.viewTime = 0
    self.linkStyles = {}
    self.nodeStyles = {}
    self.nodePosition = {}
    self.tooltips = gtk.Tooltips ()
    self.tooltips.set_tip(self, 'RapidNet')
    #self.connect("query-tooltip", self.do_query_tooltip)
    self.xscale = 1
    self.yscale = 1

  def SetWorldModel (self, netWorldModel):
    ns3.logging.debug ("NetViewArea.SetWorldModel ()")
    self.__model = netWorldModel
    self.tooltips.set_tip (self, self.__model.GetLabelText ('protocol'))
    self.queue_draw()

  def SetAnimationTime (self, time):
    self.viewTime = time
    self.queue_draw()

  def do_expose_event (self, event):
    window = self.get_window ()
    if window != None and self.__model != None:

      allocation = self.get_allocation ()
      width = float (allocation.width)
      height = float (allocation.height)

      minx = self.__model.left
      miny = self.__model.bottom
      maxx = self.__model.right
      maxy = self.__model.top

      self.xscale = width / (maxx - minx)
      self.yscale = height / (maxy - miny)
      
      cr = self.window.cairo_create ()
      cr.rectangle (event.area.x, event.area.y, event.area.width, event.area.height)
      cr.clip ()
      
      for node in self.__model.nodes.values ():
        (hasPosition, x, y) = node.GetPosition (self.viewTime)
        if hasPosition:
          x -= minx
          y -= miny

          x *= self.xscale
          y *= self.yscale

          for ip, linkStates in node.links.iteritems ():
            if len (linkStates) != 0:
              style = LinkStyle ()
              for styleKey in linkStates:
                if styleKey in self.linkStyles:
                  #ns3.logging.debug ("Found link style '%s' in library." % styleKey)
                  st = self.linkStyles[styleKey]
                  if st.hasLineWidth:
                    style.lineWidth = st.lineWidth
                  if st.hasColor:
                    style.r = st.r
                    style.g = st.g
                    style.b = st.b
                    style.a = st.a
              target = self.__model.GetNodeByIP (ip)
              if target == None:
                ns3.logging.warn ("No node for target ip for link %d . %s " % (node.id, ip))
                continue

              (hasPos, tx, ty) = target.GetPosition(self.viewTime)
              if hasPos:
                ty -= miny

                tx *= self.xscale
                ty *= self.yscale

                cr.save ()
                cr.set_line_width (style.lineWidth)
                cr.set_source_rgba (style.r, style.g, style.b, style.a)

                cr.move_to (x, height - y)
                cr.line_to (tx, height - ty)
                cr.stroke ()
                cr.restore ()

      for node in self.__model.nodes.values ():
        (hasPos, x, y) = node.GetPosition (self.viewTime)
        id = node.GetID ()
        if hasPos:
          nodeStyle = NodeStyle()
          nodeStyle.id = id
          for state in node.states:
            if state in self.nodeStyles:
              #ns3.logging.debug ("Found node style '%s' in library." % state)
              ns = self.nodeStyles[state]
              if ns.hasLineWidth:
                nodeStyle.lineWidth = ns.lineWidth
              if ns.hasLineColor:
                nodeStyle.lr = ns.lr
                nodeStyle.lg = ns.lg
                nodeStyle.lb = ns.lb
                nodeStyle.la = ns.la
              if ns.hasColor:
                nodeStyle.r = ns.r
                nodeStyle.g = ns.g
                nodeStyle.b = ns.b
                nodeStyle.a = ns.a
              if ns.hasRadius:
                nodeStyle.radius = ns.radius
              if ns.hasShape:
                nodeStyle.shape = ns.shape
              if ns.hasDouble:
                nodeStyle.double = ns.double

          x -= minx
          y -= miny

          x *= self.xscale
          y *= self.yscale

          self.nodePosition[node] = (x, y, nodeStyle.radius)

          utils = RenderUtils ()
          utils.DrawNode(cr, x, height - y, nodeStyle, id)

    return True
  
  def do_query_tooltip (self, widget, x, y, keyboard_mode, tooltip):
    pass
    # ########  DO NOT DELETE - ROUTING TABLE COMPUTATION ###### 
    #mindist = sys.maxint
    #mindist_node = None
    #mindist_pos = None
    #for node, pos in self.nodePosition.iteritems():
    #  dist = math.sqrt (math.pow (pos[0] - x, 2) + \
    #                               math.pow (pos[1] - y, 2))
    #  #print ('node %d at pos(%.0f, %.0f, %.0f) and tooltip at (%s, %s), dist = %.0f' % \
    #  #                  (node, pos[0], pos[1], pos[2], x, y, dist))
    #  if dist < mindist:
    #    mindist = dist
    #    mindist_node = node 
    #    mindist_pos = pos
    #
    ##tooltip.set_text (mindist_node.GetRoutingTable ())
    ##tooltip.set_text ('node %d at pos(%.0f, %.0f, %.0f) \ntooltip at (%s, %s)' % \
    ##                  (mindist_node.id, mindist_pos[0], mindist_pos[1], mindist_pos[2], x, y))

    return True

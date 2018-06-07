import os
import gtk, cairo
from ns3.rapidnet.rapidnet_config import *
from ns3.viewer.net_view_area import RenderUtils
from ns3.viewer.node_style import *

YLEVEL_NODE = 17
YLEVEL_TEXT = 22

# Initial base
XBASE = 20 

# Default space between 2 legend entries
XSLOT = 110

# Space between legend and text
XPAD_L_T = {NodeShape.CIRCLE: 12, NodeShape.SQUARE: 20}

# Pad between text and next legend
XPAD_T_L = 20

# Space occupied by the legend image
XLEGENDSPACE = {NodeShape.CIRCLE: 27, NodeShape.SQUARE: 45}

class Legend (gtk.DrawingArea):
  
  __gsignals__ = { "expose-event": "override" }

  def __init__ (self, nodeStyles, linkStyles):
    gtk.DrawingArea.__init__(self)
    self.renderUtils = RenderUtils ()
    self.nodeStyles = nodeStyles
    self.linkStyles = linkStyles
    self.nodeStyles['Default'] = NodeStyle ()
    self.set_tooltip_text ('Legend')
    
  def SetModel (self, model):
    self.__model = model
    self.queue_draw()
    
  def RenderText (self, cr, x, y, styleObj, text, font_size = 12,
    xlegendspace = XLEGENDSPACE[NodeShape.CIRCLE]):
    cr.save ()
    cr.move_to (x, y)
    cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    xadv = cr.text_extents(text)[4]
    #print cr.text_extents(text)
    xslot = xadv + XPAD_T_L + xlegendspace
    cr.set_font_size(font_size)
    cr.show_text (text)
    cr.stroke ()
    cr.restore ()
    return xadv

  def do_expose_event (self, event):
    window = self.get_window ()
    if window != None and self.__model != None:
      cr = self.window.cairo_create ()
      cr.rectangle (event.area.x, event.area.y, event.area.width, event.area.height)
      cr.clip ()

      protocol = self.__model.GetLabelText ('protocol')
      legends = LookupConfig (Config_Legends, protocol)

      xpos = XBASE# - XSLOT
      xslot = 0
      for index in legends:
        pair = legends[index]
        style = pair[0]
        name = pair[1]
        styleObj = self.nodeStyles[style]

        # Draw node
        xpos += xslot
        self.renderUtils.DrawNode (cr, xpos, YLEVEL_NODE, styleObj)      

        # Write text
        xadv = self.RenderText (cr, xpos + XPAD_L_T[styleObj.shape], \
          YLEVEL_TEXT, styleObj, name, 12, XLEGENDSPACE[styleObj.shape])
        #cr.save ()
        #cr.move_to (xpos + XPAD_L_T[styleObj.shape], YLEVEL_TEXT)
        #cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        #xadv = cr.text_extents(name)[4]
        ##print cr.text_extents(name)
        xslot = xadv + XPAD_T_L + XLEGENDSPACE[styleObj.shape]
        #cr.set_font_size(12)
        #cr.show_text (name)
        #cr.stroke ()
        #cr.restore ()

      xpos += xslot
      linkLegends = LookupConfig (Config_Link_Legends, protocol)
      for index in linkLegends:
        pair = linkLegends[index]
        style = pair[0]
        name = pair[1]
        styleObj = self.linkStyles[style]
        
        cr.save ()
        cr.set_line_width (styleObj.lineWidth)
        cr.set_source_rgba (styleObj.r, styleObj.g, styleObj.b, styleObj.a)
        # Small hacks here to fit DSR link legend
        cr.move_to (xpos - 5, YLEVEL_NODE)
        cr.line_to (xpos + 25, YLEVEL_NODE)
        cr.stroke ()
        cr.restore ()
        xadv = self.RenderText (cr, xpos + XPAD_L_T[NodeShape.SQUARE] + 10, \
          YLEVEL_NODE + 3, styleObj, name, 8, 45)

    return True

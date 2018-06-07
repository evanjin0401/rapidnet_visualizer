'''
Created on Jul 4, 2009

@author: shivkumar
'''
import matplotlib
matplotlib.use('GTK')
import gobject

from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk import FigureCanvasGTK
from ns3.rapidnet.model.rapidnet_world_model import PointType
from ns3.rapidnet.model.rapidnet_world_model import GraphSpec

class GraphView:

  def __init__ (self, type = PointType.Default, title = '', xupper = 1.0,
    yupper = 1.0, xlower = 0, ylower = 0, xlabel = '', ylabel = '',
    grid = True):

    self.type = type
    self.model = None
    self.figure = Figure ()
    self.axis = self.figure.add_subplot (111)
    self.axis.set_title (title)
    self.axis.set_xlabel (xlabel)
    self.axis.set_ylabel (ylabel)
    self.axis.grid (grid)
    self.axis.set_xbound (xlower, xupper)
    self.axis.set_ybound (ylower, yupper)
    self.axis.set_autoscale_on (False)
    self.canvas = FigureCanvasGTK (self.figure)
    self.line, = self.axis.plot ([], [])
    self.axis.set_position ([0.15, 0.1, 0.80, 0.85])
    # There seems no better way to animate matplotlib figures
    # than having a separate periodic refresh which calls
    # a synchronous draw on the canvas
    self.cid = gobject.timeout_add (200, self.expose_event)
    
  def SetSpec (self, spec):
    self.type = spec.type
    #self.axis.set_title (spec.title);
    self.axis.set_xbound (spec.xlower, spec.xupper)
    self.axis.set_ybound (spec.ylower, spec.yupper)
    #self.axis.set_xlabel (spec.xlabel)
    text = self.axis.set_ylabel (spec.title)
    #if len (spec.title) > 16:
    text.set_size ('small')
    self.canvas.set_tooltip_text(spec.title)

  def SetWorldModel (self, model):
    self.model = model
    
  def expose_event (self):
    x, y = self.model.GetPoints (self.type)
    self.line.set_xdata (x)
    self.line.set_ydata (y)
    self.figure.canvas.draw ()
    return True
  
  #def __del__ (self):
  #  gobject.source_remove (self.cid)

import sys, gc
import gtk, pango
from ns3.viewer.net_view_area import NetViewArea
from ns3.viewer.time_slider import TimeSlider
from ns3.viewer.node_style import NodeStyle, NodeShape
from ns3.viewer.link_style import LinkStyle
from ns3.drivers.node_style_driver import LoadNodeStyles
from ns3.drivers.link_style_driver import LoadLinkStyles
from ns3.drivers.file_driver import LoadLog
from ns3.viewer.animation_model import AnimationModel
from ns3.rapidnet.viewer.graph_view import GraphView
from ns3.rapidnet.model.rapidnet_world_model import PointType, RapidNetWorldModel
from ns3.rapidnet.viewer.menu_bar import RapidNetVisualizerMenuBar
from ns3.rapidnet.rapidnet_config import *
from ns3.rapidnet.viewer.legend import Legend
from ns3.rapidnet.viewer.speed_adjust import SpeedAdjust

class RapidNetVisualizer:

  def __init__ (self):
    self.NUM_GRAPHS = 4
    # Only UI components here
    self.initialized = False
    self.netViewArea = NetViewArea()
    self.playback = TimeSlider()
    self.playbutton = gtk.Button (stock = gtk.STOCK_MEDIA_PAUSE)
    self.window = gtk.Window ()

    # Maintain a list of MAX_GRAPHS graphs as a buffer
    self.graphsList = []
    for i in range (0, self.NUM_GRAPHS):
      self.graphsList.append (GraphView ())
    # The actual set of graphs to be used mapped on their type for quick lookup
    self.graphsMap = {}

    self.legend = None
    # Simulation parameters
    self.info = gtk.ListStore (str, str, str, str)

    self.speedAdjust = SpeedAdjust ()
    
    self.menubar = RapidNetVisualizerMenuBar (self)
    self.window.connect ("delete-event", gtk.main_quit)
    self.playbutton.connect("clicked", self.TogglePlaying)
    self.SetDefaultStyles ()

  def Initialize (self, decorator_log, nodeStyle_file = None, \
                  linkStyle_file = None, interval = None):
    # Data models here
    self.netWorldModel = RapidNetWorldModel()
    self.animationModel = AnimationModel()
    print 'Loading trace file: %s' % decorator_log
    LoadLog (self.netWorldModel, decorator_log)
    if nodeStyle_file != None:
      LoadNodeStyles(nodeStyle_file, self.netViewArea.nodeStyles)
    if linkStyle_file != None:
      LoadLinkStyles(linkStyle_file, self.netViewArea.linkStyles)
    #if interval != None:
    #  self.animationModel.SetInterval (interval)
    self.initialized = True

    self.playback.SetWorldModel (self.netWorldModel)
    self.playback.SetAnimationModel(self.animationModel)
    self.netViewArea.SetWorldModel (self.netWorldModel)
    self.animationModel.SetWorldModel (self.netWorldModel)
    self.animationModel.AddNotifier(self.netViewArea)
    self.animationModel.AddNotifier(self.playback)
    self.ReadGraphs ()
    self.ReadInfo ()

    # Legend initialized only first time    
    if self.legend == None:
      self.legend = Legend (self.netViewArea.nodeStyles, self.netViewArea.linkStyles)

    self.legend.SetModel (self.netWorldModel)
    
    initialValue = LookupConfig (Config_AnimationSpeed, self.netWorldModel.GetLabelText ('protocol'))
    self.animationModel.SetInterval (initialValue)

    self.speedAdjust.SetAnimationModel (self.animationModel)
    #self.speedAdjust.adjustment.set_value (initialValue)

    self.animationModel.ResetTo(0)
  
  def ReadGraphs (self):
    for graphType, graphSpec in self.netWorldModel.graphSpecs.iteritems ():
      graph = self.graphsList[graphSpec.position]
      graph.SetSpec (graphSpec)
      self.graphsMap[graphType] = graph

    for graph in self.graphsMap.values():
      graph.SetWorldModel (self.netWorldModel)
    
  def ReadInfo (self):
    # Add data in 2 steps, even and odd to make sure order of the labels is right
    data = {}
    for labelType, labelSpec in self.netWorldModel.labelSpecs.iteritems ():
      pos = labelSpec.position
      if pos % 2 == 0:
        #print 'Reading info at', pos, labelSpec.name, labelSpec.value
        data[pos] = [labelSpec.name, labelSpec.value]

    for labelType, labelSpec in self.netWorldModel.labelSpecs.iteritems ():
      pos = labelSpec.position
      if pos % 2 == 1:
        #print 'Reading info at', pos - 1, labelSpec.name, labelSpec.value
        data[pos - 1] += [labelSpec.name, labelSpec.value]

    # Add the data to the list in sorted order  
    keys = data.keys ()
    keys.sort ()
    for key in keys:
      self.info.append (data[key])
      
  def ReInitialize (self, decorator_log):
    print 'Re-initializing...'
    print 'Stopping...'
    self.menubar.visualizer.SetPlaying (False)
    interval = self.animationModel.interval
    del self.netWorldModel
    del self.animationModel
    self.graphsMap = {}
    self.info.clear()
    gc.collect()
    self.menubar.visualizer.Initialize (decorator_log, None, None, interval)
    self.menubar.visualizer.SetPlaying (True)
    print 'Done...'

  def SetDefaultStyles (self):
    self.netViewArea.nodeStyles["command"] = NodeStyle(lineWidth = 0.25, \
         r = 0, g = 0, b = 1, a = 1, hasLineWidth = True, hasColor = True)
    self.netViewArea.nodeStyles["user"] = NodeStyle (lineWidth = 4, \
                                                     hasLineWidth = True)
    self.netViewArea.nodeStyles["client"] = NodeStyle (lineWidth = 0, \
         r = 1, g = 0, b = 1, a = 1, hasLineWidth = True, hasColor = True)
    self.netViewArea.linkStyles['week'] = LinkStyle (0, 1, 0, 1, 1)
    self.netViewArea.linkStyles['strong'] = LinkStyle (10, 0, 0, 0, 1)
    self.netViewArea.linkStyles["fancy"] = LinkStyle (4, 1, 0, 0.5, 1)

  def PackAll (self):
    
    ####  Initialize Graph View ###
    scrWinNetView = gtk.ScrolledWindow ()
    scrWinNetView.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    scrWinNetView.add_with_viewport(self.netViewArea)
    scrWinNetView.set_shadow_type(gtk.SHADOW_NONE)
    scrWinNetView.set_size_request(100, 250)
    arenaFrame = gtk.Frame ('Arena')
    arenaFrame.add (scrWinNetView)
    

    vboxLeft = gtk.VBox ()
    for i in range (0, self.NUM_GRAPHS):
      scrWin = gtk.ScrolledWindow ()
      scrWin.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
      scrWin.add_with_viewport(self.graphsList[i].canvas)
      vboxLeft.pack_start(scrWin)

    ####  Initialize Simulation parameters ###
    infoFrame = gtk.Frame ('Simulation Parameters')
    infoFrame.set_tooltip_text ('Simulation Parameters')
    #infoFrame.set_label_align (0, 0)
    hBoxTable = gtk.HBox ()
    infoFrame.add (hBoxTable)
    
    self.tableLeft = gtk.TreeView (self.info)
    self.tableRight = gtk.TreeView (self.info)
    for i in range (0, 2):
      self.tableLeft.append_column (gtk.TreeViewColumn ("Col%d" % i, \
        gtk.CellRendererAccel (), text = i))
      self.tableRight.append_column (gtk.TreeViewColumn ("Col%d" % i, \
        gtk.CellRendererAccel (), text = i+2))

    self.tableLeft.set_headers_visible(False)
    self.tableLeft.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)
    self.tableRight.set_headers_visible(False)
    self.tableRight.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_BOTH)

    infoFrameLeft = gtk.Frame (None)
    infoFrameLeft.add (self.tableLeft)
    hBoxTable.pack_start(infoFrameLeft, padding = 2)
    
    infoFrameRight = gtk.Frame (None)
    infoFrameRight.add(self.tableRight)
    hBoxTable.pack_start(infoFrameRight, padding = 2)

    ####  Initialize Legend ###
    legendFrame = gtk.Frame ('Legend')
    legendWin = gtk.ScrolledWindow ()
    legendWin.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    legendWin.add_with_viewport(self.legend)
    legendWin.set_shadow_type(gtk.SHADOW_NONE)
    legendFrame.add (legendWin)
    legendWin.set_size_request(10, 35)
    
    ####  Compose all ###
    vboxRight = gtk.VBox ()
    vboxRight.pack_start (arenaFrame, expand = True, padding = 2)
    vboxRight.pack_start (legendFrame, expand = False, padding = 2)
    vboxRight.pack_start (infoFrame, expand = False, padding = 2)

    hboxUpper = gtk.HBox ()
    hboxUpper.pack_start (vboxLeft, expand = True)
    hboxUpper.pack_start (vboxRight, expand = True)
    hboxUpper.set_spacing(4)

    vboxFull = gtk.VBox ()
    vboxFull.pack_start (self.menubar, expand = False)
    self.window.add (vboxFull)
    vboxFull.pack_start (hboxUpper, expand = True)

    hboxLower = gtk.HBox ()
    vboxFull.pack_start (hboxLower, expand = False)
    
    hboxLower.pack_start (self.playbutton, expand = False)
    hboxLower.pack_start (self.playback, expand = True)
    hboxLower.pack_start (self.speedAdjust, expand = False)

  def Show (self):
    self.window.set_title ("RapidNet Demo Visualizer")
    self.window.set_border_width (0)
    self.window.set_size_request (800, 550)
    self.window.maximize ()

    label = self.playbutton.get_children()[0].get_children ()[0].get_children()[1]
    label.set_label ('')
    self.playbutton.set_focus_on_click(False)

    self.PackAll()
    self.window.show_all()
    self.window.present ()

  def TogglePlaying (self, widget, data = None):
    self.SetPlaying(not self.animationModel.playing)

  def SetPlaying (self, value = True):
    self.animationModel.SetPlaying(value)
    if value:
      self.playbutton.set_label(gtk.STOCK_MEDIA_PAUSE)
      self.playbutton.set_tooltip_text ('Pause')
    else:
      self.playbutton.set_label(gtk.STOCK_MEDIA_PLAY)
      self.playbutton.set_tooltip_text ('Play')
    label = self.playbutton.get_children()[0].get_children ()[0].get_children()[1]
    label.set_label ('')

  def Start (self):
    self.animationModel.Start()

  def Run (self):
    if not self.initialized:
      raise Exception ("RapidNetVisualizer instance is not initialized. " \
                       "Invoke the 'Initialize' method before running.")
    else:
      self.Show()
      self.Start ()
      gtk.main ()


def main ():
  hasInterval = False
  interval = 100

  if len (sys.argv) <= 1:
    print 'Usage: test_gui_playback decorator.log ' \
          '[linkstyle_file nodestyle_file interval]'
    sys.exit (0)

  decorator_log = sys.argv[1]
  linkStyle_file = None
  nodeStyle_file = None
  if len (sys.argv) >= 4:
    nodeStyle_file = sys.argv[2]
  if len (sys.argv) >= 3:
    linkStyle_file = sys.argv[3]
  if len (sys.argv) >= 5:
    hasInterval = True
    interval = int (sys.argv[4])

  visualizer = RapidNetVisualizer ()
  visualizer.Initialize(decorator_log, nodeStyle_file, linkStyle_file, interval)
  visualizer.Run ()

if __name__ == "__main__":
    main ()


import sys
import gtk
from ns3.viewer.net_view_area import NetViewArea
from ns3.viewer.time_slider import TimeSlider
from ns3.viewer.node_style import NodeStyle, NodeShape
from ns3.viewer.link_style import LinkStyle
from ns3.drivers.node_style_driver import LoadNodeStyles
from ns3.drivers.link_style_driver import LoadLinkStyles
from ns3.drivers.file_driver import LoadLog
from ns3.model.net_world_model import NetWorldModel
from ns3.viewer.animation_model import AnimationModel

def main ():
  hasInterval = False
  interval = 100

  if len (sys.argv) <= 1:
    print 'Usage: test_gui_playback decorator.log [linkstyle_file nodestyle_file interval]'
    sys.exit (0)

  decorator_log = sys.argv[1]
  linkstyle_file = None
  nodestyle_file = None
  if len (sys.argv) >= 3:
    linkstyle_file = sys.argv[3]
  if len (sys.argv) >= 4:
    nodestyle_file = sys.argv[2]
  if len (sys.argv) >= 5:
    hasInterval = True
    interval = int (sys.argv[4])

  window = gtk.Window()
  window.connect ("delete-event", gtk.main_quit)
  window.set_title ("py ns3-decorator")
  window.set_border_width (0)
  window.set_size_request (410, 440)

  netView = NetViewArea ()
  scrolledWindow = gtk.ScrolledWindow ()
  scrolledWindow.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
  scrolledWindow.add_with_viewport(netView)

  playback = TimeSlider()

  vbox = gtk.VBox ()
  window.add (vbox)
  vbox.pack_start (scrolledWindow, expand = True)

  hbox = gtk.HBox ()
  vbox.pack_start (hbox, expand = False)

  pButton = gtk.Button (stock = gtk.STOCK_MEDIA_PAUSE)
  label = pButton.get_children()[0].get_children ()[0].get_children()[1]
  label.set_label ('')
  
  hbox.pack_start (pButton, expand = False)
  hbox.pack_start (playback, expand = True)

  window.show_all()
  window.present ()

  #Setup some default styles
  linkStyles = {}
  linkStyles['week'] = LinkStyle (0, 1, 0, 1, 1)
  linkStyles['strong'] = LinkStyle (10, 0, 0, 0, 1)
  linkStyles["fancy"] = LinkStyle (4, 1, 0, 0.5, 1)
  if linkstyle_file != None:
    LoadLinkStyles(linkstyle_file, linkStyles)

  nodeStyles = {}
  nodeStyles["command"] = NodeStyle(lineWidth = 0.25, r = 0, g = 0, b = 1, \
    a = 1, hasLineWidth = True, hasColor = True)
  nodeStyles["user"] = NodeStyle (lineWidth = 4, hasLineWidth = True)
  nodeStyles["client"] = NodeStyle (lineWidth = 0, r = 1, g = 0, b = 1, \
    a = 1, hasLineWidth = True, hasColor = True)
  if nodestyle_file != None:
    LoadNodeStyles(nodestyle_file, nodeStyles)

  netView.linkStyles = linkStyles
  netView.nodeStyles = nodeStyles

  netWorldModel = NetWorldModel ()
  LoadLog (netWorldModel, decorator_log)

  #for event in netWorldModel.events:
  #  print event, event.__dict__

  playback.SetWorldModel (netWorldModel)
  netView.SetWorldModel (netWorldModel)

  anim = AnimationModel ()
  anim.SetWorldModel (netWorldModel)
  if hasInterval:
    anim.SetInterval (interval)
  anim.AddNotifier (netView)
  anim.AddNotifier (playback)

  anim.ResetTo (0)
  anim.Start()

  gtk.main ()

if __name__ == "__main__":
    main ()

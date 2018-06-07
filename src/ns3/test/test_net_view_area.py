import sys
import gtk
from ns3.viewer.net_view_area import NetViewArea
from ns3.model.net_world_model import NetWorldModel
from ns3.drivers.file_driver import LoadLog

def main ():
  window = gtk.Window ()
  window.connect("delete-event", gtk.main_quit)
  window.set_title("py ns-3 Decorator")
  window.set_border_width(0)
  window.set_size_request(410, 440)
  
  scrolledWindow = gtk.ScrolledWindow ()
  scrolledWindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
  
  netView = NetViewArea()
  scrolledWindow.add_with_viewport(netView)
  window.add(scrolledWindow)
  window.show_all()
  
  netWorldModel = NetWorldModel()
  netView.SetWorldModel(netWorldModel)
  
  gtk.main()
  
if __name__ == "__main__":
  main ()
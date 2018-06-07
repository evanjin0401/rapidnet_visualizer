'''
Created on Jul 6, 2009

@author: shivkumar
'''
import gtk
import os
from ns3.rapidnet.rapidnet_config import *
from gtkcodebuffer import CodeBuffer, SyntaxLoader

lang = SyntaxLoader("cpp")

class SimulateMenu (gtk.MenuItem):

  def __init__ (self, menubar):
    gtk.MenuItem.__init__ (self, 'Protocols')
    self.menubar = menubar
    self.rootmenu = gtk.Menu ()
    self.set_submenu(self.rootmenu)
    self.SetupMenuTree('traces', self.rootmenu)
  
  def SetupMenuTree (self, folder, menu):
    if 'events.log' in os.listdir(folder):
      return
    subfolders = os.listdir(folder)
    subfolders.sort ()
    for entry in subfolders:
      abs_entry = os.path.join (folder, entry)
      if os.path.isdir(abs_entry) and entry != '.svn':
        submenu = gtk.Menu ()
        print 'Found', abs_entry
        menuitem = gtk.MenuItem (entry[2:].replace ('_', ' '))
        menu.append (menuitem)
        self.SetupMenuTree(abs_entry, submenu)
        if len (submenu.get_children()) > 0:
          menuitem.set_submenu (submenu)
        else:
          menuitem.connect('activate', self.Activated, abs_entry)

  def Activated (self, menuitem, path):
    self.menubar.visualizer.ReInitialize (os.path.join (path, 'events.log'))
    
# Global map to cache code buffers 
CodeBuffers = {}

# To initialize and retrieve code buffers 
def GetCodeBuffer (filename):
  codeBuffer = None
  if filename not in CodeBuffers:
    codeBuffer = CodeBuffer (lang=lang)
    filePath = os.path.join (Config_Application_Folder, filename)
    fileContents = open (filePath, 'r').read ()
    codeBuffer.set_text (fileContents)
    CodeBuffers[filename] = codeBuffer
  else:
    codeBuffer = CodeBuffers[filename]
  return codeBuffer

# Scrolled Window to show code
class CodeView (gtk.ScrolledWindow):

  def __init__(self, ext):
    gtk.ScrolledWindow.__init__(self)
    self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    self.ext = ext
    
    gtk.ScrolledWindow.__init__(self)
    self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    
    #self.textBuffer = gtk.TextBuffer ()
    #self.textBuffer  = CodeBuffer(lang=lang)

  def ShowFile (self, filename):
    #filePath = os.path.join (Config_Application_Folder, filename + self.ext)
    #fileContents = open (filePath, 'r').read ()
    #self.textBuffer.set_text(fileContents)
    self.textView = gtk.TextView ()
    self.textView.set_editable(False)
    self.add (self.textView)
    self.textBuffer = GetCodeBuffer (filename + self.ext)
    self.textView.set_buffer (self.textBuffer)

    # Make it scroll
    end_iter = self.textBuffer.get_end_iter()
    self.textBuffer.insert(end_iter, '')
    self.textView.scroll_to_mark(self.textBuffer.get_insert(), 0)


class ApplicationMenu (gtk.MenuItem):

  def __init__ (self, menubar, name, width = 800, height = 550):
    gtk.MenuItem.__init__ (self, name)
    self.set_name (name)
    self.menuItem2filenameMap = {}
    self.menubar = menubar
    self.rootmenu = gtk.Menu ()
    self.set_submenu (self.rootmenu)
    self.SetupMenuTree (Config_Application_Folder, self.rootmenu)
    self.codeViews = []
    self.width = width
    self.height = height

  def AddCodeView (self, codeView):
    self.codeViews.append (codeView)
    
  def SetupMenuTree (self, folder, menu):
    for key,value in Config_Applications.iteritems ():
      self.menuItem2filenameMap[value[1]] = value[0] 
      menuitem = gtk.MenuItem (value[1])
      menuitem.set_name (value[1])
      menuitem.connect('activate', self.Activated)
      menu.append (menuitem)

  def Activated (self, menuitem):
    self.codeWindow = gtk.Window ()
    hBox = gtk.HBox ()
    for codeView in self.codeViews:
      codeView.ShowFile (self.menuItem2filenameMap[menuitem.get_name ()])
      hBox.pack_start (codeView, padding = 5)
    
    self.codeWindow.set_title (self.get_name() + ' - ' + menuitem.get_name())
    self.codeWindow.set_size_request (self.width, self.height)
    self.codeWindow.set_position (gtk.WIN_POS_CENTER)
    self.codeWindow.add (hBox)
    self.codeWindow.show_all ()
    self.codeWindow.show ()
    self.codeWindow.present ()
    

class ShowRulesMenu (ApplicationMenu):
  
  def __init__ (self, menubar):
    ApplicationMenu.__init__(self, menubar, 'NDlog Rules')
    
  def Activated (self, menuitem):
    self.codeViews = []
    self.nDlogView = CodeView ('.olg')
    self.AddCodeView(self.nDlogView)
    ApplicationMenu.Activated(self, menuitem)

class GenCodeMenu (ApplicationMenu):
  
  def __init__ (self, menubar):
    ApplicationMenu.__init__(self, menubar, 'Generated Code', 1000, 550)

  def Activated (self, menuitem):
    self.codeViews = []
    self.headerView = CodeView ('.h')
    self.AddCodeView(self.headerView)
    self.ccView = CodeView ('.cc')
    self.AddCodeView(self.ccView)
    ApplicationMenu.Activated(self, menuitem)


class RapidNetVisualizerMenuBar (gtk.MenuBar):

  def __init__ (self, visualizer):
    gtk.MenuBar.__init__(self)
    self.visualizer = visualizer
    self.InitializeMenus ()

  def InitializeMenus (self):
    self.viewMenu = SimulateMenu (self)
    self.append(self.viewMenu)

    self.showRulesMenu = ShowRulesMenu (self)
    self.append(self.showRulesMenu)
    
    self.genCodeMenu = GenCodeMenu (self)
    self.append(self.genCodeMenu)


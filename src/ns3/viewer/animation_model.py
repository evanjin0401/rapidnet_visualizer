import gtk
import gobject
import ns3

class AnimationNotifier:

  def SetAnimationTime (self, time):
    pass



class AnimationModel:

  def __init__ (self):
    self.currentTime = 0
    self.__model = None
    self.interval = 250
    self.timeoutDuration = 10
    self.loop = True
    self.playing = False
    self.notifiers = []
    self.__animTimeout = None

  def ToggleLoop (self):
    self.loop = not self.loop

  def AddNotifier (self, notifier):
    self.notifiers.append(notifier)

  def SetWorldModel (self, model):
    self.__model = model

  def SetInterval (self, interval):
    self.interval = interval

  # Remember, time is in milliseconds
  def ResetTo(self, time = 0):
    self.currentTime = time
    self.__model.Start ()
    self.__model.ProcessUpTo (self.currentTime)
    self.__Notify (self.currentTime)

  def Start (self):
    self.__model.Start ()
    ns3.logging.debug ("AnimationModel.Start ()")
    self.__animTimeout = gobject.timeout_add (self.timeoutDuration, self.__Advance)
    self.playing = True

  def Stop (self):
    ns3.logging.debug ("AnimationModel.Stop ()")
    gobject.source_remove (self.__animTimeout)
    self.playing = False

  def TogglePlaying (self):
    self.SetPlaying (not self.playing)

  def SetPlaying (self, value = True):
    if value:
      self.Start()
    else:
      self.Stop()

  def __Notify (self, time):
    for notifier in self.notifiers:
      notifier.SetAnimationTime (time)

  def __Advance (self):
    res = True
    self.currentTime += self.interval
    #ns3.logging.debug ('AnimationModel.__Advance (): currentTime %d' % self.currentTime)
    if self.currentTime > self.__model.GetLastTimestamp():
      if self.loop:
        self.ResetTo(0)
      else:
        self.currentTime = self.__model.GetLastTimestamp ()
        self.__model.ProcessUpTo (self.currentTime)
        self.__Notify (time)
        self.Stop ()
        res = False
    else:
      self.__model.ProcessUpTo (self.currentTime)
      self.__Notify (self.currentTime)

    return res


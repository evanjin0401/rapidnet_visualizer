import gtk
import animation_model

class TimeSlider (gtk.HScale, animation_model.AnimationNotifier):

  def __init__ (self):
    gtk.HScale.__init__(self)
    self.adjustment = gtk.Adjustment (0, 0, 0)
    self.set_update_policy (gtk.UPDATE_DISCONTINUOUS)
    self.set_digits (1)
    self.set_value_pos (gtk.POS_TOP)
    self.set_adjustment (self.adjustment)
    self.__model = None
    self.__animationModel = None
    self.connect('change-value', self.MoveSlider)
    self.connect('button-release-event', self.Released)
    self.page_size = 30.0
    self.step_size = 0 # Don't care
    self.set_increments(self.step_size, self.page_size)
    self.target = 0.0
    self.set_tooltip_text('Time (Seconds)')

  def Released (self, event, data):
    #print 'released!', event, data
    self.__animationModel.ResetTo (self.target * 1000)

  def SetWorldModel (self, netWorldModel):
    self.__model = netWorldModel
    self.adjustment.lower = 0
    self.adjustment.upper = self.__model.GetLastTimestamp () / 1000

  def SetAnimationModel (self, animationModel):
    self.__animationModel = animationModel

  def SetAnimationTime (self, time):
    self.adjustment.set_value (time / 1000)

  def MoveSlider (self, range, scroll, value):
    self.target = value
    if scroll == gtk.SCROLL_PAGE_FORWARD:
      self.target = value + self.page_size
    elif scroll == gtk.SCROLL_PAGE_BACKWARD:
      self.target = value - self.page_size

    if self.target < 0.0:
      self.target = 0.0

    #print 'slider moved!', range, scroll, value, self.target
    
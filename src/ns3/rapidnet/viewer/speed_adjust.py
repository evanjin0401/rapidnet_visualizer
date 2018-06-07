import os, sys
import gtk
from ns3.rapidnet.rapidnet_config import *

class SpeedAdjust (gtk.SpinButton):
  
  def __init__ (self):
    self.FACTOR = 10
    self.STEP = 20
    default = Config_AnimationSpeed['Default'] / self.FACTOR
    min = Config_AnimationSpeed['MIN'] / self.FACTOR
    max = Config_AnimationSpeed['MAX'] / self.FACTOR
    self.adjustment = gtk.Adjustment (default, max, min, self.STEP / self.FACTOR)
    gtk.SpinButton.__init__(self, self.adjustment)
    self.set_tooltip_text('Animation Speed')
    self.sigId = self.connect('value_changed', self.SetSpeed)
    
  def SetAnimationModel (self, animationModel):
    self.__animationModel = animationModel
    # Temporarily disconnect to avoid infinite loop and then connect back
    self.disconnect(self.sigId)
    self.adjustment.set_value (animationModel.interval / self.FACTOR)
    self.sigId = self.connect('value_changed', self.SetSpeed)
    
  def SetSpeed (self, obj):
    self.__animationModel.SetInterval (self.adjustment.value * self.FACTOR)
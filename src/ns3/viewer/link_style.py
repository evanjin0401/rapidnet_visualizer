

class LinkStyle:

  def __init__ (self, lw = 1.5, r = 0.4, g = 0.4, b = 0.4, a = 1):
    self.hasColor = False
    self.hasLineWidth = False
    self.lineWidth = lw
    self.r = r
    self.g = g
    self.b = b
    self.a = a

  def __repr__ (self):
    return "LinkStyle (hasColor=%s, color=(r=%.1f, g=%.1f, b=%.1f, a=%.1f), hasLineWidth=%s, lineWidth=%.1f)" % \
      (self.hasColor, self.r, self.g, self.b, self.a, self.hasLineWidth, self.lineWidth)

class NodeShape:
  CIRCLE = 0
  SQUARE = 1

class NodeStyle:

  def __init__ (self, hasLineWidth = True, lineWidth = 2, hasLineColor = True, \
                lr = 0.01, lg = 0.2, lb = 0.9, la = 1.0, hasColor = True, \
                r = 0.25, g = 0.4, b = 1.0, a = 1, \
                hasRadius = False, radius = 8.0, hasShape = False, \
                shape = NodeShape.CIRCLE, hasDouble = False, double = False):

    self.hasLineWidth = hasLineWidth
    self.lineWidth = lineWidth
    self.hasLineColor = hasLineColor
    self.lr = lr
    self.lg = lg
    self.lb = lb
    self.la = la
    self.hasColor = hasColor
    self.r = r
    self.g = g
    self.b = b
    self.a = a
    self.hasRadius = hasRadius
    self.radius = radius
    self.hasShape = hasShape
    self.shape = shape
    self.hasDouble = hasDouble
    self.double = double


  def __repr__ (self):
    shape = 'Unknown'
    if self.shape == NodeShape.CIRCLE:
      shape = 'circle'
    elif self.shape == NodeShape.SQUARE:
      shape = 'square'
    return "NodeStyle (hasColor=%s, color=(r=%.1f, g=%.1f, b=%.1f, a=%.1f), hasLineColor=%s, " \
      "lineColor=(r=%.1f, g=%.1f, b=%.1f, a=%.1f), hasShape=%s, shape=%s, hasLineWidth=%s, " \
      "lineWidth=%s, hasRadius=%s, radius=%s, hasDouble=%s, double=%s)" % (self.hasColor, self.r,
      self.g, self.b, self.a, self.hasLineColor, self.lr, self.lg, self.lb, self.la,
      self.hasShape, shape, self.hasLineWidth, self.lineWidth, self.hasRadius, self.radius,
      self.hasDouble, self.double)

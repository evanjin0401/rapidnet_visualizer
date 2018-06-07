import ns3
from ns3.viewer.node_style import NodeStyle, NodeShape


def LoadNodeStyles (filename, nodeStyles):

  ns3.logging.debug ("LoadNodeStyles: filename = %s" % filename)

  try:
    file = open (filename, 'r')
    linecount = 0
    for line in file:
      linecount += 1
      line = line.strip ()
      if line.startswith ('#') or line == '':
        continue

      # Comments begin with # and cannot appear mid line
      # NodeStyle definition is of the following form
      # styleKey : styleBody
      # where styleKey is a string and styleBody is
      # a comma separated list of commands of the form
      # command=value
      # Example:
      # user: color=00ff00, double=true
      # white space are ignored and the nodeStyle definition
      # should be in one single line
      tokens = line.partition (':')
      if tokens [1] == ':':
        styleKey = tokens[0]
        style = ParseNodeStyle (tokens [2], linecount)
        nodeStyles[styleKey] = style
        ns3.logging.debug ("Line %d: NodeStyle['%s'] = %s" % (linecount, styleKey, str (style)))
      else:
        ns3.logging.error ("Line %d: Skipping line. Bad line: '%s'. " \
                           "Syntax is <style_name>=<command_name>=<value>, ..." % (linecount, line))
  except IOError:
    ns3.logging.error ("Could not open node style file %s" % filename)

  return nodeStyles


def ParseNodeStyle (body, linecount):
  style = NodeStyle ()
  commands = body.strip ().split (',')
  for command in commands:
    words = command.strip ().partition ('=')
    if words[1] != '=':
      ns3.logging.error ("Line %d: Skipping bad command '%s'. " \
                         "Syntax is <command_name>=<value>." % (linecount, command.strip ()))
    else:
      name = words[0].strip ().lower ()
      value = words[2].strip ()
      if name == 'color':
        ParseColor (value, style, linecount)
      elif name == 'linecolor':
        ParseLineColor (value, style, linecount)
      elif name == 'radius':
        ParseRadius (value, style, linecount)
      elif name == 'shape':
        ParseShape (value, style, linecount)
      elif name == 'double':
        ParseDouble (value, style, linecount)
      elif name == 'linewidth':
        ParseLineWidth (value, style, linecount)
      else:
        ns3.logging.error ("Line %d: Unknown node style command '%s'." % (linecount, command.strip ()))
  return style


def ParseColor (value, style, linecount):
  (success, r, g, b, a) = ParseRGBA (value, linecount, 'color')
  if success:
    style.hasColor = True
    style.r = r
    style.g = g
    style.b = b
    style.a = a


def ParseLineColor (value, style, linecount):
  (success, lr, lg, lb, la) = ParseRGBA (value, linecount, 'linecolor')
  if success:
    style.hasLineColor = True
    style.lr = lr
    style.lg = lg
    style.lb = lb
    style.la = la


def ParseRadius (value, style, linecount):
  try:
    style.radius = float (value)
    style.hasRadius = True
  except ValueError:
    ns3.logging.error ("Line %d: Bad radius value '%s'. " \
                       "Should be an real number." % (linecount, value))

def ParseShape (value, style, linecount):
  value = value.lower ()
  if value == 'square':
    style.hasShape = True
    style.shape = NodeShape.SQUARE
  elif value == 'circle':
    style.hasShape = True
    style.shape = NodeShape.CIRCLE
  else:
    ns3.logging.error ("Line %d: Unknown shape '%s'." % (linecount, value))


def ParseDouble (value, style, linecount):
  value = value.lower ()
  if value == 'true':
    style.hasDouble = True
    style.double = True
  elif value == 'false':
    style.hasDouble = True
    style.double = False
  else:
    ns3.logging.error ("Line %d: Bad double value '%s'. " \
                       "Should be 'true' or 'false'." % (linecount, value))


def ParseLineWidth (value, style, linecount):
  try:
    style.lineWidth = float (value)
    style.hasLineWidth = True
  except ValueError:
    ns3.logging.error ("Line %d: Bad linewidth value '%s'. " \
                       "Should be an real number." % (linecount, value))


def ParseRGBA (value, linecount, attr):
  if len (value) != 6 and len (value) != 8:
    ns3.logging.error ("Line %d: Bad RGBA value '%s' for attribute %s. " \
                       "Should be 6 or 8 digit hex number." % (linecount, value, attr))
    return (False, 0, 0, 0, 1)
  try:
    red = float (int (value[0:2], 16))
    green = float (int (value[2:4], 16))
    blue = float (int (value[4:6], 16))
    if len (value) == 8:
      alpha = float (int (value[6:], 16))
    else:
      alpha = 255.0
    return (True, red / 255.0, green / 255.0, blue / 255.0, alpha / 255.0)
  except ValueError:
    ns3.logging.error ("Line %d: Parse exception while reading color value '%s'." % (linecount, value))
    return (False, 0, 0, 0, 1)


#nodeStyles = {}
#LoadNodeStyles('../../../styles/node-styles010', nodeStyles)

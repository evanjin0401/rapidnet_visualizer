import ns3
from ns3.viewer.link_style import LinkStyle
from node_style_driver import ParseColor, ParseLineWidth


def LoadLinkStyles (filename, linkStyles):
  ns3.logging.debug ("LoadLinkStyles: filename = %s" % filename)

  try:
    file = open (filename, 'r')
    linecount = 0
    for line in file:
      linecount += 1
      line = line.strip ()
      if line.startswith ('#') or line == '':
        continue

      # Comments begin with # and cannot appear mid line
      # LinkStyle definition is of the following form
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
        style = ParseLinkStyle (tokens [2], linecount)
        linkStyles[styleKey] = style
        ns3.logging.debug ("Line %d: LinkStyle['%s'] = %s" % (linecount, styleKey, str (style)))
      else:
        ns3.logging.error ("Line %d: Skipping line. Bad line: '%s'. " \
                           "Syntax is <style_name>=<command_name>=<value>, ..." % (linecount, line))
  except IOError:
    ns3.logging.error ("Could not open link style file %s" % filename)

  return linkStyles


def ParseLinkStyle (body, linecount):
  style = LinkStyle ()
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
      elif name == 'linewidth':
        ParseLineWidth (value, style, linecount)
      else:
        ns3.logging.error ("Line %d: Unknown link style command '%s'." % (linecount, command.strip ()))
  return style


#linkStyles = {}
#LoadLinkStyles('../../../styles/link-styles010', linkStyles)

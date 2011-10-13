import xml.dom.minidom

class ConfigParseException (Exception):
  pass

class LogStub:
  def debug(self, s):
    print "DEBUG: " + s
  def info(self, s):
    print "INFO: " + s
  def warning(self, s):
    print "WARNING: " + s
  def errof(self, s):
    print "ERROR: " + s

"""Gets the concatenated textNode children of node"""
def getText(node):
  ret = ""
  for child in node.childNodes:
    if child.nodeName == "#text":
      ret += child.wholeText
  return ret

class ConfigLoader:
  def __init__(self, rpc):
    self.log = LogStub()#logging.getLogger("Cortex.ConfigLoader")
    self.rpc = rpc

  def parseXML(self, filename):
    try:
      dom = xml.dom.minidom.parse(filename)
    except IOError, e:
      print "Couldn't open file %s" % filename
      return None

    if not dom.getElementsByTagName("server"):
      self.log.warning("Found no server in config %s" % filename)
      return

    try:
      server = dom.getElementsByTagName("server")[0]
      for depot in server.getElementsByTagName("depot"):
        self.parseDepot(depot)
      for manager in server.getElementsByTagName("manager"):
        self.parseManager(manager)
    except ConfigParseException, e:
      self.log.error("Parse error for %s: %s" % (filename, e))

  def parseDepot(self, depot):
    # Parse the depot and init using RPC
    if not (depot.hasAttribute("name") and depot.hasAttribute("type")):
      raise ConfigParseException(
          "Depot missing name or type: %s" % depot.toxml())
    type = depot.getAttribute("type")
    name = depot.getAttribute("name")
    args = {}
    for arg in depot.childNodes:
      if arg.nodeName == "#text":
        continue
      args[arg.nodeName] = getText(arg)

    self.rpc.addDepot(type, name, args)
    
  def parseManager(self, manager):
    # Parse each manager and init using RPC
    if not manager.hasAttribute("type"):
      raise ConfigParseException("Manager missing type: %s" % manager.toxml())
    type = manager.getAttribute("type")
    args = {}
    for arg in manager.childNodes:
      if arg.nodeName == "#text":
        continue
      elif arg.nodeName == "reader":
        reader_type, reader_args = self.parseReader(arg)
        args['reader'] = reader_type
        args['reader_args'] = reader_args
      elif arg.nodeName == "to_depot":
        if "depot" in args:
          args["depots"].append(getText(arg))
        else:
          args["depots"] = [getText(arg)]
      else:
        args[arg.nodeName] = getText(arg)

    self.rpc.addManager(type, args)

  """This is different from the other parse methods, since it returns:
  returns (str: type, dict: reader_args)"""
  def parseReader(self, reader):
    args = {}
    if not reader.hasAttribute("type"):
      raise ConfigParseException("Reader missing type: %s" % reader.toxml())
    for reader_arg in reader.childNodes:
      if reader_arg.nodeName == "#text":
        continue
      else:
        args[reader_arg.nodeName] = getText(reader_arg)
    return reader.getAttribute("type"), args
        

if __name__ == "__main__":
  ConfigLoader(None).parseXML("config.xml")

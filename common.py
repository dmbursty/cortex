import re
import htmlentitydefs

class xmlentitydefs:
  name2codepoint = {"quot" : 34,
                    "amp"  : 38,
                    "apos" : 39,
                    "lt"   : 60,
                    "rt"   : 62}

  codepoint2name = {34 : "quot",
                    38 : "amp",
                    39 : "apos",
                    60 : "lt",
                    62 : "gt"}

  entitydefs     = {"quot" : "\"",
                    "amp"  : "&",
                    "apos" : "'",
                    "lt"   : "<",
                    "rt"   : ">"}

class codec:
  # DO NOT CALL THESE MEMBER FUNCTIONS, THEY ARE ABSTRACT YO
  @classmethod
  def encode(c, m):
    char = m.group(0)
    try:
      return "&%s;" % c.defs.codepoint2name[ord(char)]
    except KeyError:
      return char

  @classmethod
  def decode(c, m):
    text = m.group(0)
    if text[:2] == "&#":
      try:
        if text[:3] == "&#x":
          return unichr(int(text[3:-1], 16))
        else:
          return unichr(int(text[2:-1]))
      except ValueError:
        pass
        #print "ValueError: ",
    else:
      try:
        return unichr(c.defs.name2codepoint[text[1:-1]])
      except KeyError:
        pass
        #print "KeyError: ",
    print "Couldn't decode: %s" % text
    return text

  @classmethod
  def escape(c, text):
    return re.sub(".", c.encode, text)
    
  @classmethod
  def unescape(c, text):
    return re.sub("&#?\w+;", c.decode, text)

class xml(codec):
  defs = xmlentitydefs

class html(codec):
  defs = htmlentitydefs

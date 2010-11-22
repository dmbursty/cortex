from CoutDepot import CoutDepot
from RSSDepot import RSSDepot

_depot_lookup = {'Cout':CoutDepot,
                 'RSS':RSSDepot,
                }

def getDefaultDepot():
  return RSSDepot()

def getDepot(name):
  try:
    return _depot_lookup[name]
  except KeyError, e:
    return None

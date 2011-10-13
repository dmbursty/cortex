from TimerManager import TimerManager
from UpdateTrackerManager import UpdateTrackerManager

# Be aware, these methods return classes not instances!

_manager_lookup = {'TimerManager':TimerManager,
                   'UpdateTrackerManager':UpdateTrackerManager,
                  }

def getDefaultManager():
  return TimerManager

def getManager(name):
  try:
    return _manager_lookup[name]
  except KeyError, e:
    return None

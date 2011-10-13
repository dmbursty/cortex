def synchronize(lockname):
  def wrap(f):
    def new_f(self, *args, **kwargs):
      try:
        lock = getattr(self, lockname)
        lock.acquire()
        try:
          return f(self, *args, **kwargs)
        finally:
          lock.release()
      except AttributeError, e:
        raise Exception("Couldn't synchronize function %s" % f.__name__)
        return f(self, *args, **kwargs)
    return new_f
  return wrap

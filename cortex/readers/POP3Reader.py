import getpass
import poplib

from BaseReader import BaseReader

# DO NO USE ME.  POP3 is bad :( use IMAPReader
# Also, This has not been tested very well

class POP3Reader(BaseReader):
  """This reader is used to monitor an email inbox.
     WARNING: This reader will retrieve all of your emails, and treat
     each one as an item.
     An update will be triggered every time a new email is recieved.
     If you only want to retrieve meta info, and manually check your email,
     please use IMAPReader instead (see private option)
  """
  def __init__(self, args):
    self.server = args['server']
    self.account = args['account']
    if args['ssl']:
      self.pop3 = poplib.POP3_SSL
    else:
      self.pop3 = poplib.POP3
    self.data = None
    self.moredata = None
    self.identifier = None
    self.password = getpass.getpass("Enter password for %s:" % self.account)

    pop3 = self.pop3(self.server)
    pop3.user(self.account)
    try:
      pop3.pass_(self.password)
      self.state = pop3.stat()
    except poplib.error_proto:
      raise Exception("Incorrect username/password for %s" % self.account)
    finally:
      pop3.quit()

    BaseReader.__init__(self)
    self.log.log("Starting POP3 Reader for %s" % self.account)


  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    # Retrieve data through pop3
    pop3 = self.pop3(self.server)
    pop3.user(self.account)
    pop3.pass_(self.password)
    # Check if there are any new emails (will also trigger on deletes?)
    newstate = pop3.stat()
    if newstate != self.state:
      self.state = newstate
      # Make items
      self.items.append(POP3Item(self.state, {'account':self.account}))
    pop3.quit()


class POP3Item(BaseReader):
  """Object for storing an item. Has output formatters"""
  def __init__(self, data, metadata):
    BaseItem.__init__(self, metadata)
    self.set_all_content("%s now has %d emails" % (metadata['account'], data[0]))

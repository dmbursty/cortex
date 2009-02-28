import getpass
import poplib

# DO NO USE ME.  POP3 is bad :( use IMAPReader

class POP3Reader:
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
    self.email = args['email']
    if args['ssl']:
      self.pop3 = poplib.POP3_SSL
    else:
      self.pop3 = poplib.POP3
    self.data = None
    self.moredata = None
    self.identifier = None
    self.password = getpass.getpass("Enter password for %s:" % self.email)

    pop3 = self.pop3(self.server)
    pop3.user(self.account)
    try:
      pop3.pass_(self.password)
    except poplib.error_proto:
      raise Exception("Incorrect username/password for %s" % self.email)
    pop3.quit()

    print "Created POP3 Reader for %s" % self.email
    if not self.checkForUpdate():
      raise Exception("No update at Init")
    print "Latest: " + self.getItems[0].toSummary()

  def checkForUpdate(self):
    """Check the source for an update by comparing identifiers.
       This call will update self.data
    """
    self.retrieveData()
    # Functionality for identifiers goes here
    new_identifier = len(self.moredata.keys())
    if new_identifier != self.identifier:
      self.identifier = new_identifier
      return True
    return False

  def retrieveData(self):
    """Retrieve data from the source"""
    pop3 = self.pop3(self.server)
    pop3.user(self.account)
    pop3.pass_(self.password)
    self.data = pop3.list()
    pop3.quit()

  def getUpdate(self):
    """Return the latest update to the source"""

  def getItems(self):
    """Return all items of the source"""
    # Turn raw data into items, and return
    items = []
    for num, data in self.moredata.items():
      items.append(POP3Item(num, data))
    return items


class POP3Item:
  """Object for storing an item. Has output formatters"""
  def __init__(self, num, data, aux = None):
    self.num = num
    self.aux = aux

    self.headers = {}
    for line in data:
      k, v = line.split(": ")
      self.headers[k] = v

  def toString(self):
    """Get the item as a complete string"""
    return self.headers['Subject']

  def toSummary(self):
    """Get a short summary of the item"""
    return self.headers['Subject']

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    # Remember to escape when necessary
    return self.toString()

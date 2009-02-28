import getpass
import imaplib
import re

class IMAPReader:
  """This reader is used to monitor an email inbox."""
  def __init__(self, args):
    self.server = args['server']
    self.email = args['email']
    if args['ssl']:
      self.imap = imaplib.IMAP4_SSL
    else:
      self.imap = imaplib.IMAP4
    self.data = []
    self.identifier = 0
    self.password = getpass.getpass("Enter password for %s:" % self.email)

    imap = self.imap(self.server)
    try:
      imap.login(self.email, self.password)
    except imaplib.IMAP4.error:
      raise Exception("Incorrect username/password for %s" % self.email)
    imap.logout()

    print "Created IMAP Reader for %s" % self.email
    if not self.checkForUpdate():
      raise Exception("No update at Init")

  def checkForUpdate(self):
    """Check the source for an update by comparing identifiers.
       This call will update self.data
    """
    self.retrieveData()
    new_identifier = len(self.data) / 2
    if new_identifier != self.identifier:
      self.identifier = new_identifier
      return True
    return False

  def retrieveData(self):
    """Retrieve data from the source"""
    imap = self.imap(self.server)
    imap.login(self.email, self.password)
    num_mail = int(imap.select()[1][0])
    if num_mail > self.identifier:
      print "Retrieving emails %d through %d" % (self.identifier + 1, num_mail)
      response, new_data = imap.fetch("%d:%d" % (self.identifier + 1, num_mail),
                                      "(BODY[HEADER.FIELDS (DATE SUBJECT)])")
      self.data.extend(new_data)
    imap.logout()

  def getUpdate(self):
    """Return the latest update to the source"""

  def getItems(self):
    """Return all items of the source"""
    # Turn raw data into items, and return
    items = []
    filtered = [i for i in self.data if i != ')']
    filtered = [i[1] for i in filtered]
    filtered.reverse()
    items = [IMAPItem(i) for i in filtered]
    return items


class IMAPItem:
  """Object for storing an item. Has output formatters"""
  def __init__(self, data, aux = None):
    self.aux = aux
    self.subj = re.search("[Ss]ubject: ([\w\W]*?)\r\n(\r\n|[Dd]ate: )",
                          data).group(1)
    self.date = re.search("[Dd]ate: ([\w\W]*?)\r\n(\r\n|[Ss]ubject: )",
                          data).group(1)

  def toString(self):
    """Get the item as a complete string"""
    return "Recieved the following message on %s:\n%s " % (self.date, self.subj)

  def toSummary(self):
    """Get a short summary of the item"""
    return self.subj

  def toHTML(self):
    """Get the item as an HTML formatted string"""
    # Remember to escape when necessary
    return self.toString()


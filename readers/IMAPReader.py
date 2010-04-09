import getpass
import imaplib
import re

from BaseReader import BaseReader, BaseItem

class IMAPReader(BaseReader):
  """This reader is used to monitor an email inbox."""
  def __init__(self, args):
    self.server = args['server']
    self.email = args['email']
    if args['ssl']:
      self.imap = imaplib.IMAP4_SSL
    else:
      self.imap = imaplib.IMAP4
    self.password = getpass.getpass("Enter password for %s:" % self.email)

    imap = self.imap(self.server)
    try:
      imap.login(self.email, self.password)
      self.state = imap.select()
    except imaplib.IMAP4.error:
      raise Exception("Incorrect username/password for %s" % self.email)
    imap.logout()

    print "Created IMAP Reader for %s" % self.email
    BaseReader.__init__(self)

  def checkUpdate(self):
    """Check for an update, and put it in self.items"""
    imap = self.imap(self.server)
    imap.login(self.email, self.password)
    newstate = imap.select()
    if newstate != self.state:
      self.state = newstate
      self.items.append(IMAPItem(self.state, {'email':self.email}))
    imap.logout()


class IMAPItem(BaseItem):
  """Object for storing an item. Has output formatters"""
  def __init__(self, data, metadata):
    BaseItem.__init__(self, data, metadata)
    #self.subj = re.search("[Ss]ubject: ([\w\W]*?)\r\n(\r\n|[Dd]ate: )",
                          #data).group(1)
    #self.date = re.search("[Dd]ate: ([\w\W]*?)\r\n(\r\n|[Ss]ubject: )",
                          #data).group(1)

  def getDataString(self):
    """Get the complete item data as a string"""
    return "%s now has %d emails" % (self.metadata['email'], self.data[1][0])

  def getSummaryString(self):
    """Get a short summary of the item"""
    return "%s now has %d emails" % (self.metadata['email'], self.data[1][0])

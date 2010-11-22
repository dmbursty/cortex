from AtomReader import AtomReader
from IMAPReader import IMAPReader
from LocalFileReader import LocalFileReader
from RSSReader import RSSReader
from RegexWebsiteReader import RegexWebsiteReader
from SimpleWebsiteReader import SimpleWebsiteReader
from POP3Reader import POP3Reader

_reader_lookup = {'IMAP':IMAPReader,
                  'LocalFile':LocalFileReader,
                  'RSS':RSSReader,
                  'Atom':AtomReader,
                  'RegexWebsite':RegexWebsiteReader,
                  'SimpleWebsite':SimpleWebsiteReader,
                  #'POP3':POP3Reader,  # Not Supported
                 }

def getReader(name):
  try:
    return _reader_lookup[name]
  except KeyError, e:
    return None

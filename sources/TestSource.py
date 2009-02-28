from readers.RSSReader import RSSReader
from readers.IMAPReader import IMAPReader
from readers.LocalFileReader import LocalFileReader
from readers.RegexWebsiteReader import RegexWebsiteReader
from readers.SimpleWebsiteReader import SimpleWebsiteReader

SEC  = 1
MIN  = 60 * SEC
HR   = 60 * MIN
DAY  = 24 * HR
WEEK = 7  * DAY

class TestSource:
  """These sources change frequently and are used for testing purposes"""
  def __init__(self):
    self.sources = []

    #################
    ### RSS Feeds ###
    #################
    # Digg updates very frequently
    #self.sources.append({
        #'class':RSSReader,
        #'interval':2*MIN,
        #'args': {'source':"http://feeds.digg.com/digg/popular.rss"} })

    ################
    ### Websites ###
    ################
    # Try to get around the random content
    self.sources.append({
        'class':RegexWebsiteReader,
        'interval':30*SEC,
        'args': {
            'source':"http://www.qwantz.com/",
            'regex':"<img src=\"http://www.qwantz.com/comics/.*?\ " + \
                    "width=\"\d+\" height=\"\d+\" title=\".*?\" border=\"\d+\">"
        }
    })

    ######################
    ### Email accounts ###
    ######################
    ## Try to avoid too many email Readers as the init for each one is long
    # Combined email account
    #self.sources.append({
        #'class':IMAPReader,
        #'interval':10*MIN,
        #'args':{
            #'server' :"imap.gmail.com",
            #'email'  :"dmbursty@gmail.com",
            #'ssl'    :True} })

    #############
    ### Other ###
    #############
    #examples = """
    #self.sources.append({
        #'class':LocalFileReader,
        #'interval':15*SEC,
        #'args': {'source':"/home/mburstyn/update/sample.txt"} })
    #"""

  def getSources(self):
    """Get the various sources that dictate the elements of the system,
       Return should be a list of dictionaries, and each dictionary should
       have a class, interval, and args (dictionary)"""
    return self.sources

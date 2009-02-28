from readers.RSSReader import RSSReader
from readers.IMAPReader import IMAPReader
from readers.LocalFileReader import LocalFileReader

SEC  = 1
MIN  = 60 * SEC
HR   = 60 * MIN
DAY  = 24 * HR
WEEK = 7  * DAY

class HardCodeSource:
  """These sources are hard coded into the class"""
  def __init__(self):
    self.sources = []

    #################
    ### RSS Feeds ###
    #################
    # XKCD Comic Feed
    self.sources.append({
        'class':RSSReader,
        'interval':1*HR,
        'args': {'source':"http://xkcd.com/rss.xml"} })
    # XKCD Blag Feed
    self.sources.append({
        'class':RSSReader,
        'interval':1*DAY,
        'args': {'source':"http://blag.xkcd.com/feed/"} })
    # Penny Arcade Feed
    self.sources.append({
        'class':RSSReader,
        'interval':30*MIN,
        'args': {'source':"http://feeds.penny-arcade.com/pa-mainsite/"} })
    # Dinosaur Comics Feed
    self.sources.append({
        'class':RSSReader,
        'interval':30*MIN,
        'args': {'source':"http://rsspect.com/rss/qwantz.xml"} })
    # Kotaku Feed
    self.sources.append({
        'class':RSSReader,
        'interval':15*MIN,
        'args': {'source':"http://feeds.gawker.com/kotaku/full/"} })

    ######################
    ### Email accounts ###
    ######################
    ## Try to avoid too many email readers as the init for each one is long
    # Combined email account
    self.sources.append({
        'class':IMAPReader,
        'interval':10*MIN,
        'args':{
            'server' :"imap.gmail.com",
            'email'  :"dmbursty@gmail.com",
            'ssl'    :True} })

    #############
    ### Other ###
    #############
    examples = """
    self.sources.append({
        'class':LocalFileReader,
        'interval':15*SEC,
        'args': {'source':"/home/mburstyn/update/sample.txt"} })
    """

  def getSources(self):
    """Get the various sources that dictate the elements of the system,
       Return should be a list of dictionaries, and each dictionary should
       have a class, interval, and args (dictionary)"""
    return self.sources

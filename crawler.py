# Conrad Dean


# Explores the Internet so you don't have to!

"""
The web crawler should be able to move around the internet at a nice, leisurely pace collecting things about web pages.
It should collect links to other pages, and it should collect wordcounts of a page, because collecting the entire page would take up quite a bit of space-- maybe we can just get away with word counts?

Also, it should keep a record of previously explored pages so it doesn't do anything redundant
"""

#TODO
'''
make word frequency counter work

implement a constraint so it won't explore outside of its nth parent.
    example: carleton.edu/cs/comps/
    parent = 0 -> explores carleton.edu/cs/comps/*
    parent = 1 -> explores carleton.edu/cs/*
    parent = 2 -> explores carleton.edu/*
    parent = 3 -> explores *
    parent = -1 -> explores *

database is a pickled dictionary right now.  we should fix that

'''
import pickle
import urllib2
import urlparse
from HTMLParser import HTMLParser
class Page(HTMLParser):

    def __init__(self,url):
        HTMLParser.__init__(self)
        self.link_list = []
        self.url = url
        self._content = None

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.add_to_list_of_links(attrs)

    def add_to_list_of_links(self,attrs):
        linkstuff = attrs[0]
        type,url = linkstuff
        if type == "href":
            url = urlparse.urljoin(self.url,url)  #translate link to proper url
            if self.isValidLink(url):
                self.link_list.append(url)

    @property
    def content(self):
        if self._content == None:
            #print "content not loaded, loading now..."
            self._content = str(urllib2.urlopen(self.url).read())
        return self._content
        
        

    @property
    def links(self):
        self.feed(self.content)
        return self.link_list

    @property
    def words(self):
        #self.generateWordCount()
        self.word_counts = {"what":90}
        return self.word_counts


    def isValidLink(self,url):
        #make based off appropriate parent setting
        """ from pagerank assignment
        if (
            re.match( "^https?://apps.carleton.edu/curricular/cs/.*",url) and # stay within subsite
            #not re.match( ".*/$",url) and  # skip links to pages that the server would have to resolve: "...cirricular/cs/major/"
            #not re.match( ".*/@textonly=1",url) and
            True
            ):
            return True
        else:
            return False
            """
        return True

    def strip_anchor(self,url):
        if "#" in url:
            now = url[:url.find('#')]
            return now
        else:
            return url


class Crawler:

    def __init__(self,start_page,rest=1000,
                    pickled_dictionary_file="meh",
                    depth=5):
        
        self.pages_to_visit = [Page(start_page)]  # queue for pages to load
        self.rest = rest  # time in ms to wait between pageloads
        # database structure:
        # database[url_to_page] = ([link1,link2,...], {word:word_count,...})
        db = False
        if db:
            with open(pickled_dictionary_file,"rb") as f:
                self.database = pickle.load(f)
        else:
            self.database = {}
        self.depth=5  # distance allowed from start page


    def start(self):
        
        while len(self.pages_to_visit) > 0:
            current_page = self.pages_to_visit.pop(0)
            if current_page.url in self.database:
                continue #to next page on the list

            self.database[current_page.url] = ([], {}) # so you don't visit it again
            #print current_page.url
            #try:
            links = current_page.links
            word_counts = current_page.words
            self.database[current_page.url] = (links, word_counts)
            for url in links:
                self.pages_to_visit.append(Page(url))
                #print "\t",filename
            #good.append(current_page)
            """
            except IOError:
                #print "\tDoesn't exist, 404?"
                bad.append(current_page)
                continue
                """


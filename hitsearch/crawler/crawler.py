# Conrad Dean and Andy Freeland


# Explores the Internet so you don't have to!

"""
The web crawler should be able to move around the internet at a nice, leisurely pace collecting things about web pages.
It should collect links to other pages, and it should collect wordcounts of a page, because collecting the entire page would take up quite a bit of space-- maybe we can just get away with word counts?

Also, it should keep a record of previously explored pages so it doesn't do anything redundant
"""

#TODO
'''
implement a constraint so it won't explore outside of its nth parent.
    example: carleton.edu/cs/comps/
    parent = 0 -> explores carleton.edu/cs/comps/*
    parent = 1 -> explores carleton.edu/cs/*
    parent = 2 -> explores carleton.edu/*
    parent = 3 -> explores *
    parent = -1 -> explores *

'''

import urllib2
import urlparse
import posixpath
import time
import BeautifulSoup
import utils
from counter import Counter

class ParseError(Exception):
    pass

class Page:
    def __init__(self, url):
        self.links = []
        self.word_counts = None
        self.url = self.standardize_url(url)
        try:
            self.parse_page()
        except urllib2.URLError, e:
            print 'URL_ERROR', self.url, e
        except ParseError, e:
            print 'PARSE_ERROR', e

    def parse_page(self):
        page = urllib2.urlopen(self.url)
        strainer = BeautifulSoup.SoupStrainer({'a': True, 'title': True, 'body': True, 'script': True})
        soup = BeautifulSoup.BeautifulSoup(page, parseOnlyThese=strainer) # what if it fails to parse?
        links = soup('a')
        self.get_links(links)
        try:
            self.get_content(soup)
        except Exception, e:
            raise ParseError( '%s could not be parsed.' % self.url )

    def get_links(self, links):
        for link in links:
            target = link.get('href', '')
            if target != '':
                target = urlparse.urljoin(self.url, target) # translate link to proper url
                target = self.standardize_url(target) # standardize url
                if self.is_valid_link(target):
                    self.links.append(target)

    def get_content(self, soup):
        # based on http://groups.google.com/group/beautifulsoup/browse_thread/thread/9f6278ee2a2e4564
        #remove comments
        comments = soup(text=lambda text:isinstance(text, 
            BeautifulSoup.Comment))
        [comment.extract() for comment in comments]
        # remove javascript
        js = soup('script')
        [tag.extract() for tag in js]
        
        # count words!
        body = soup.body(text=True)
        words = ''.join(body).split()
        words = [utils.sanitize(word).lower() for word in words if len(word) != 0]
        self.word_count = Counter(words) 

    def __eq__(self,y):
        if type(y) is str or type(y) is unicode:
            return self.url == self.standardize_url(y)
        else:
            return self.url == y.url
    
    def standardize_url(self,url):
        url = self.strip_anchor(url)
        url = resolve_components(url)
        return url
    
    def resolve_components(self,url):
        # taken from http://stackoverflow.com/questions/4317242/python-how-to-resolve-urls-containing/4317446#4317446
        """
        >>> resolveComponents('http://www.example.com/foo/bar/../../baz/bux/')
        'http://www.example.com/baz/bux/'
        >>> resolveComponents('http://www.example.com/some/path/../file.ext')
        'http://www.example.com/some/file.ext'
        """
    
        parsed = urlparse.urlparse(url)
        new_path = posixpath.normpath(parsed.path)
        if parsed.path.endswith('/'):
            # Compensate for issue1707768
            new_path += '/'
        cleaned = parsed._replace(path=new_path)
        return cleaned.geturl()
    
    def strip_anchor(self,url):
        if "#" in url:
            now = url[:url.find('#')]
            return now
        else:
            return url

    def is_valid_link(self,url):
        return True


class Crawler:

    def __init__(self,start_page,rest=1000,
                    pickled_dictionary_file="meh",
                    depth=5):
        
        self.pages_to_visit = [(Page(start_page),0)]  # queue for pages to load
        # time in ms to wait between pageloads
        self.rest = rest
        # database structure:
        # database[url_to_page] = ([link1,link2,...], {word:word_count,...})
        db = False
        if db:
            with open(pickled_dictionary_file,"rb") as f:
                self.database = pickle.load(f)
        else:
            self.database = []
        self.depth = depth if depth > 0 else float("inf") # distance allowed from start page


    def start(self):
        
        while len(self.pages_to_visit) > 0:
            time.sleep(self.rest/1000.0)
            current_page,distance_from_start = self.pages_to_visit.pop(0)
            if current_page in self.database or distance_from_start > self.depth:
                continue #to next page on the list
            print "checking out page",current_page.url

            #self.database[current_page.url] = ([], {}) # so you don't visit it again
            self.database.append(current_page)
            #print current_page.url
            #try:
            #links = current_page.links
            #word_counts = current_page.words
            #self.database[current_page.url] = (links, word_counts)
            for url in current_page.links:
                self.pages_to_visit.append((Page(url),distance_from_start+1))
                #print "\t",filename
            #good.append(current_page)
            """
            except IOError:
                #print "\tDoesn't exist, 404?"
                bad.append(current_page)
                continue
                """


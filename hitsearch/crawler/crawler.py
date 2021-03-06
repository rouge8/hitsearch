# Conrad Dean and Andy Freeland


# Explores the Internet so you don't have to!

"""
The crawler moves around the internet at a nice leisurely pace, as specified by its "rest" argument, the time it waits between pages.  Additionally, if a web page is unresponsive, it will wait for a factor of rest*(2^n), where n is the number of timeouts that have happened before.

There are two parts to the crawler, Page objects, and the Crawler class.  Page objects do most of the grunt work with parsing the html found at a given URL and returning a list of new URL's back to the Crawler.  The Crawler itself coordinates which pages to load and collects the relevant ones for saving to the database.

The Crawler's crawl() method is an iterator that returns pages it finds.  It acts like a thread-safe buffer, letting the database pull pages out of it even while the Crawler is waiting for a page to load.  This lets us have the overhead from the database and the internet overlap letting us consume web pages more efficently.
"""

import httplib2
import urlparse
import posixpath
import time
import httplib # for exceptions >_<
import BeautifulSoup
import utils
import socket
from counter import Counter
from collections import defaultdict
import threading

class ParseError(Exception):
    pass

class InvalidPageError(Exception):
    pass

class TimeoutError(Exception):
    pass

class Page:
    """Page objects used by the crawler."""

    def __init__(self, url, url_depth, word_counts=[]):
        self.links = defaultdict(list) # a dictionary of {urls: [link text]}
        self.word_counts = Counter(word_counts)
        self.url = self.standardize_url(url)
        self.title = ''
        self.parsed = False
        self.url_depth = url_depth  # controls allowable URLS to crawl. -1: same domain, 0: everything, 1: same dir, 2: parent dir of current dir, etc
        self.timeouts = 0 # number of times page has timed out

    def parse(self):
        """Loads and parses the page."""
        try:
            self.parse_page()
            self.parsed = True
        except ParseError, e:
            raise InvalidPageError(str(e))
        except httplib2.HttpLib2Error as e:
            raise InvalidPageError(str(e))
        except socket.timeout:
            self.timeouts += 1
            raise TimeoutError('%s timed out.' % self.url)

    def parse_page(self):
        try:
            h = httplib2.Http('.cache', timeout=5) # timeout in seconds
            resp, page = h.request(self.url, 'GET')
        except AttributeError:
            raise httplib2.HttpLib2Error('could not open a socket for %s.' %self.url)

        # parses only the parts of the page that we want
        strainer = BeautifulSoup.SoupStrainer({'a': True, 'title': True, 'body': True, 'script': True})
        try:
            soup = BeautifulSoup.BeautifulSoup(page, parseOnlyThese=strainer) # what if it fails to parse?
        except UnicodeEncodeError, e:
            raise ParseError('%s is not HTML.' % self.url)
        except httplib.IncompleteRead, e:
            raise ParseError(self.url +' '+  str(e))
        try:
            self.get_content(soup)
            links = soup('a')
            self.get_links(links)
        except Exception, e:
            raise ParseError( '%s could not be parsed.' % self.url )

    def get_links(self, links):
        """Gets the links on the page and their link texts."""
        for link in links:
            target = link.get('href', '')
            if target != '':
                target = urlparse.urljoin(self.url, target) # translate link to proper url
                target = self.standardize_url(target) # standardize url
                if self.is_valid_link(target):
                    # get link text
                    words = link.findAll(text=True)
                    words = ' '.join(words).split()
                    link_words = [utils.sanitize(word).lower() for word in words if len(word) != 0]
                    # links are now dictionaries of url: list_of_words
                    self.links[target].extend(link_words)


    def get_content(self, soup):
        """Gets counts of all of the words on the page."""
        # based on http://groups.google.com/group/beautifulsoup/browse_thread/thread/9f6278ee2a2e4564
        # remove comments
        comments = soup(text=lambda text:isinstance(text, 
            BeautifulSoup.Comment))
        [comment.extract() for comment in comments]
        # remove javascript
        js = soup('script')
        [tag.extract() for tag in js]
        
        # count words!
        body = soup.body(text=True)
        title = soup.title(text=True)
        self.title = ' '.join(title).strip()
        if len(self.title) == 0: self.title = self.url
        words = ' '.join(body).split() + ' '.join(title).split()
        words = [utils.sanitize(word).lower() for word in words if len(word) != 0]
        self.word_counts += Counter(words) 

    def __eq__(self,y):
        if type(y) is str or type(y) is unicode:
            return self.url == self.standardize_url(y)
        else:
            return self.url == y.url
    
    def standardize_url(self,url):
        url = self.strip_anchor(url)
        url = self.resolve_components(url)
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
        if parsed.path.endswith('/') and new_path[-1] != '/':
            # Compensate for issue1707768
            new_path += '/'
        cleaned = parsed._replace(path=new_path)
        if cleaned.geturl()[-1] == '.':
            return cleaned.geturl()[:-1]
        else:
            return cleaned.geturl()
    
    def strip_anchor(self,url):
        if "#" in url:
            now = url[:url.find('#')]
            return now
        else:
            return url

    def proper_prefix(self,url,depth):
        # -1: stay on domain
        #  0: go anywhere
        #  1: stay in folder
        #  2: go one outside folder
        if depth > url.count("/")-3:
            return self.proper_prefix(url,-1) # if you accidently exceed, just stay in domain
        if depth == -1:
            return urlparse.urljoin(url,"/")  # returns just the domain
        if depth == 0:
            return ""  # will match anything
        if depth > 0:
            for i in range(depth):
                url = url.rstrip("/")
                slash = url.rfind("/") +1
                url = url[:slash]
            return url

    def correct_parent(self,site,next_site):
        pre = self.proper_prefix(site,self.url_depth)
        return next_site.startswith(pre)

    def is_valid_link(self,url):
        # just a few cases
        if not self.correct_parent(self.url,url):
            return False
        if url.startswith('mailto:') or url.startswith('javascript:'):
            return False
        elif url.startswith('webcal:') or url.startswith('callto:'):
            return False
        elif url.endswith('textonly=1'):
            return False
        else:
            return True

class CrawlerWorker(threading.Thread):
    '''This a worker thread for the Crawler.
    It lets you continue to explore the internet without needing to wait
    for the database to finish saving a page'''

    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.parent = parent

    def run(self):
        print "thread started",self
        #while len(self.pages_to_visit) > 0:#and any(member.is_alive() for member in self.worker_threads):
        while True:
            self.pages_to_visit_empty_lock.acquire()
            while len(self.pages_to_visit) == 0:
                self.waiting_threads_up()
                self.pages_to_visit_empty_lock.wait()
                self.waiting_threads_up()
            if self.crawl_died.is_set():
                break
            current_page,distance_from_start = self.pages_to_visit_pop()
            self.pages_to_visit_empty_lock.release()
            if current_page.url in self.database or distance_from_start > self.depth:
                print "skipping",current_page.url
                continue #to next page on the list
            sleep_time = (self.rest/1000.0) + 2**current_page.timeouts
            time.sleep(sleep_time)
            print "checking out page",current_page.url

            try:
                if not(current_page.parsed):
                    current_page.parse()
            except InvalidPageError, e:
                print 'InvalidPageError', e
                continue # to next page on the list
            except TimeoutError as e:
                print 'TimeoutError', e
                if current_page.timeouts > 3:
                    continue # to next page on the list
                self.add_page_to_pages_to_visit((current_page, distance_from_start))

            self.add_page_to_database(current_page.url)
            
            for url in current_page.links:
                word_counts = current_page.links[url]
                self.add_page_to_pages_to_visit((Page(url, self.url_depth, word_counts=word_counts), distance_from_start+1))

            self.add_page_to_out_queue(current_page)
        print "Thread exit",self
        print "pages left to write to DB",len(self.parent.out_queue)

    def add_page_to_out_queue(self,page):
        self.parent.out_queue_lock.acquire()
        self.parent.out_queue.append(page)
        self.parent.out_queue_lock.release()

    @property
    def url_depth(self):
        return self.parent.url_depth

    @property
    def rest(self):
        return self.parent.rest

    @property
    def depth(self):
        return self.parent.depth

    @property
    def database(self):
        return self.parent.database
    
    def add_page_to_database(self,page):
        self.parent.database_lock.acquire()
        self.parent.database.append(page)
        self.parent.database_lock.release()

    @property
    def pages_to_visit(self):
        return self.parent.pages_to_visit

    @property
    def crawl_died(self):
        return self.parent.crawl_died

    @property
    def worker_threads(self):
        return self.parent.worker_threads

    def pages_to_visit_pop(self):
        self.parent.pages_to_visit_lock.acquire()
        page_to_vist = self.parent.pages_to_visit.pop(0)
        self.parent.pages_to_visit_lock.release()
        return page_to_vist
    
    @property
    def pages_to_visit_empty_lock(self):
        return self.parent.pages_to_visit_empty_lock
    
    @property
    def waiting_threads(self):
        return self.parent.waiting_threads
    
    def waiting_threads_up(self):
        self.parent.waiting_threads_lock.acquire()
        self.parent.waiting_threads += 1
        self.parent.waiting_threads_lock.release()
        
    def waiting_threads_down(self):
        self.parent.waiting_threads_lock.acquire()
        self.parent.waiting_threads -= 1
        self.parent.waiting_threads_lock.release()
        
    def add_page_to_pages_to_visit(self,page):
        self.parent.pages_to_visit_lock.acquire()
        self.parent.pages_to_visit.append(page)
        self.parent.pages_to_visit_lock.release()

        self.pages_to_visit_empty_lock.acquire()
        self.pages_to_visit_empty_lock.notify_all()
        self.pages_to_visit_empty_lock.release()
        

class Crawler:
    """Crawler object crawls web pages. Has parameters start_page=url, rest=milliseconds,
       url_depth=integer{-1: restrict to URLs of same domain name,
       0: allow all URLS,
       1: stay in same directory as source URL,
       2: stay within parent directory of the directory you're currently in, etc...},
       and depth=depth of crawler, number of links away from start_page allowed. """

    def __init__(self,
                start_page,
                rest=1000,
                url_depth=0,
                depth=5):
        
        # time in ms to wait between pageloads
        self.rest = rest
        self.depth = depth if depth > 0 else float("inf") # distance allowed from start page
        self.url_depth = url_depth

        self.worker_threads = []
        self.worker_threads.append(CrawlerWorker(self))
        #self.worker_thread = CrawlerWorker(self)


        # Thread-shared data structures
        self.out_queue = []
        self.database = []
        self.pages_to_visit = [(Page(start_page,self.url_depth),1)]  # queue for pages to load
        self.waiting_threads = 0

        # Locks for shared data structures
        self.out_queue_lock = threading.Lock()
        self.database_lock= threading.Lock()
        self.pages_to_visit_lock= threading.Lock()
        self.pages_to_visit_empty_lock = threading.Condition()
        self.waiting_threads_lock = threading.Lock()

        # Event for killing all threads
        self.crawl_died = threading.Event()

    def crawl(self):
        self.crawl_died.clear() # let the threads thrive
        for worker in self.worker_threads:
            worker.start()# start the crawl
        try:
            while True:
                if len(self.pages_to_visit) == 0 \
                    and not any(w.is_alive() for w in self.worker_threads)\
                    and len(self.worker_threads) == self.waiting_threads:
                    self.crawl_died.set()
                    self.pages_to_visit_empty_lock.acquire()
                    self.pages_to_visit_empty_lock.notify_all()
                    self.pages_to_visit_empty_lock.release()
                if len(self.out_queue) == 0 and not any(w.is_alive() for w in self.worker_threads):
                    raise StopIteration
                if len(self.out_queue) == 0:
                    time.sleep(.05)
                    continue
                self.out_queue_lock.acquire()
                page = self.out_queue.pop(0)
                self.out_queue_lock.release()
                yield page
        finally:
            self.crawl_died.set() # when threads see this they'll quit too 

def main():
    ''' crawler test'''
    start_site = "http://cs.carleton.edu/cs_comps/1011/robot_tour_guide/index.php"
    start_site = "http://people.carleton.edu/~deanc/testsite/deep/1.html"
    start_site = "http://people.carleton.edu/~deanc/testsite/a.html"
    #start_site = "http://people.carleton.edu/~deanc/testsite/connected/"

    depth = 600
    url_depth = 2 

    if depth:
        spider = Crawler(start_site,depth=int(depth),url_depth=url_depth, rest=0)
    else:
        spider = Crawler(start_site,url_depth=url_depth, rest=0)

    print 'starting crawl'
    
    datas = []
    for page in spider.crawl(): 
        #print "DATABASE   PUSH     < ----------- |",
        #print page.url
        datas.append(page)

        """
        # save links!
        print "save links"
        for link in page.links:
            print "\t",
            print link
            
        # save word counts!
        print "save words"
        for word in page.word_counts.keys():
            print "\t",
            print word
        """
    print len(datas), "pages found"

if __name__ == '__main__':
    main()

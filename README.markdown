# A `HITS`-based search engine
# Data Mining Final Project
# Conrad Dean, Andy Freeland, Dan Levy

Google uses PageRank.  HITS is just like PageRank, except it figures out how to automatically deal with spider-traps AND deadends.  It also tells you about the hubbiness of pages in addition to their page ranks or authorities as HITS calls it.  Way cool.

This engine is based off the [Django framework](https://www.djangoproject.com/). Our crawler uses all sorts of things from the Python standard library as well as [httplib2](http://code.google.com/p/httplib2/) as our http client and [Beautiful Soup](http://www.crummy.com/software/BeautifulSoup/) which lets us pretend most of the awful HTML on the web is actually beautiful and usable.

We also use a backport of collections.Counter from Python 2.7 to make counting things better. It can be found at <http://code.activestate.com/recipes/576611/>.

Fortunately we've included the exact versions of everything you need in with the repository so you don't need to download them on your own.  Is that violating some copyright laws? Let's hope not.

# How to Use

Go to the `hitsearch` directory in your terminal and run `./install`.  This will setup all the dependencies (locally, no system installs, so don't worry!) and setup the database.  Also, you will be asked to create an administrator account for the database.

Now you can run the server with the command `./runserver`.

If you want our fairly large (230+MB, 211000+ pages!) database, you can download it from <http://people.carleton.edu/~freelana/hitsearch.db> or run ./get-sample-database

Once the server is running, point your browser to <http://localhost:8000> and search away!

You can also populate the database with pages yourself by running `./crawl <url> <depth>'. For a while, this would eat all of our RAM for no apparent reason, no matter what we tried. We did some more research and discovered that Django's debug mode does not garbage collect objects written to the database. Turning off debug mode made the crawler manageable.

Want to play around like an admin? Go to <http://localhost:8000/admin/>. The username and password on our massive sample database are both 'admin'. From the admin page you can delete and edit objects as well as search them. It's easier and faster for searching than mucking around in the shell.

Our search page has a few options that are not found on your typical search engine. We let you sort pages by authority or hubbiness, and we have a beta value. Beta can range from 0.0 to 1.0 and determine how much of the authority and hubbiness are influenced by the word frequency. As beta increases, pages get a boost for every time those terms appear on that page. Thus, when beta=0.0, the authorities and hubbiness are 100% HITS. When beta=0 term frequency is the only thing that matters when ranking pages. If we had more time, we would have liked to have done more with Term Frequency and IDFs to improve our results.

# Cleanup

Dependencies can be removed with `remove-dependencies.sh`.

# What are all these files? (interesting version)

If you're just interested in the important and interesting stuff, I recommend looking at:

- hitsearch/crawler/crawler.py is the actual crawler.
- hitsearch/search/management/commands/crawl.py is the django command hook that handles interaction between the crawler and the database.
- hitsearch/HITS.py implements HITS
- hitsearch/query.py does all the queries
- hitsearch/search/models.py contains our database models

# What are all these files? (complete version)

That's a terrific question. There's a lot of stuff going on. Let's start in this directory.

- crawl runs the crawler. run it like ./crawl <url> <depth>
- deps/ contains all the dependencies.
- django-admin.py lets you start django projects and apps and all that. don't worry about it.
- ./get-sample-database downloads our sample database
- hitsearch/ contains the the hitsearch project. we'll get to that in a bit.
- ./install sets up all the dependencies and creates the initial database at hitsearch/hitsearch.db
- README.markdown is this.
- remove-dependencies.sh removes dependencies.
- runserver runs the server at <http://localhost:8000> (actually, <http://0.0.0.0:8000> so you can access it from outside the local machine if say, you're testing this on skittles).
- setup-dependencies.sh setups in the dependencies. ./install will call it, so don't worry.
- syncdb sets up the database. also called by ./install

This is a lot. And it doesn't even cover the project itself.

## in hitsearch/

We'll only mention things that we've touched (i.e. not simply part of django) or are important.

- crawler/ is the crawler. will be explained in a bit.
- hitsearch.db is the database of everything you've crawled! it's pretty exciting.
- HITS.py implements the HITS algorithm
- manage.py is a piece of django magic. it has commands like `manage.py runserver <host:port>` or `manage.py syncdb` or `manage.py crawl <url> <depth>` or `manage.py shell`. This last command opens a python shell with the django settings and path set correctly so you can play around with the database with `from search.models import Page, Link, Tag`
- query.py is a beautiful place. it queries the database for pages matching the input terms and sends them off to HITS to calculate. and then it returns the sorted results. documented more thoroughly in file.
- settings.py is all of our django settings.
- templates/ contains all of our django templates. the ones for our search app are in templates/search/
- urls.py uses regular expressions to map urls to django views.
- utils.py once had grand purposes for all sorts of utilities. now it just holds a function that strips accents from unicode characters and strips punctuation

## in hitsearch/crawler/

Our crawler lives here.

- crawler.py is our actual crawler. documented much more thoroughly in the file.
- utils.py is a link to utils.py in the parent directory so that we can access our utils nicely.

## in hitsearch/search/

Our search application!

- admin.py registers our models with the admin framework. 
- models.py contains our database models. explained more in file.
- static/ contains our static files. Our CSS is done in [LESS](http://lesscss.org/), which has all of the things CSS can do plus so much more.
- views.py contains the views of our application. documented more in the file.
- management/commands/crawl.py is what links our crawler to our database and lets us run the crawler with manage.py crawl. documented more in file

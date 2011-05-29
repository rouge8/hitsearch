import crawler

reload(crawler)  #for my slime vim env
#start = "http://people.carleton.edu/~deanc/testsite/a.html"
start = "http://people.carleton.edu/~deanc/testsite/deep/1.html"
c = crawler.Crawler(start,rest=0,depth=0)
c.start()

"""
print len(c.database), "many pages found"
for page,stuff in sorted(c.database.items(),key= lambda x:x[0]):
    print page,stuff
"""
if start in c.database:
    print "everything is good"
else:
    print "bad!"

n = "http://people.carleton.edu/~deanc/testsite/deep/5.html"
if n in c.database:
    print "everything is good"
else:
    print "bad!"


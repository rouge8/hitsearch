import crawler

reload(crawler)  #for my slime vim env
#start = "http://people.carleton.edu/~deanc/testsite/a.html"
start = "http://people.carleton.edu/~deanc/testsite/deep/1.html"
c = crawler.Crawler(start,rest=500)
c.start()

print len(c.database), "many pages found"
for page,stuff in sorted(c.database.items(),key= lambda x:x[0]):
    print page,stuff




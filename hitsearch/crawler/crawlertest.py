import crawler

reload(crawler)  #for my slime vim env
start = "http://people.carleton.edu/~deanc/testsite/a.html"
#start = "http://people.carleton.edu/~deanc/testsite/deep/1.html"
c = crawler.Crawler(start,rest=0,depth=0)
c.start()

for page in c.database:
    print page.url
    for l in page.links:
        print "\t",l

    print "words, counts"
    for w in page.word_count:
        print "\t",w,page.word_count[w]


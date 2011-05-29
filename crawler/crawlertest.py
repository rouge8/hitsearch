import crawler

reload(crawler)  #for my slime vim env
start = "http://people.carleton.edu/~deanc/testsite/a.html"
c = crawler.Crawler(start)
c.start()

for page,stuff in c.database.items():
    print page,stuff




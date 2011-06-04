from maker import Maker
from time import sleep
m = Maker()
m.go()
print "sleeping..."
sleep(2)
for thing in m.box:
    print thing

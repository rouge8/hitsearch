from maker import Maker
from time import sleep
m = Maker()
m.go()
print "sleeping..."
sleep(10)
for thing in m.box:
    print thing
sleep(4)
for i in m.box:
    print m.box.pop(0)

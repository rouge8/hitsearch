from time import sleep
import time
import threading
class BoxFiller(threading.Thread):
    def __init__(self,parent):
        threading.Thread.__init__(self)
        self.parent = parent
    def run(self):
        count = 0
        for i in range(30):
            sleep(.5)
            count += 1
            self.parent._box_lock.acquire()
            self.parent._box.append(count)
            self.parent._box_lock.release()

class Maker:
    def __init__(self):
        self._box = []
        self._box_lock = threading.Lock()
        self.filler = BoxFiller(self)
    
    def go(self):
        self.filler.start()

    @property
    def box(self):
        while True:
            self._box_lock.acquire()
            tmp = self._box.pop(0)
            self._box_lock.release()
            yield tmp



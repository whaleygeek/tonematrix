# Timer.py  30/09/2015  D.J.Whale
#
# Simple cooperative timer services for repeating events

import time


#----- TIMER ------------------------------------------------------------------

class Timer():
    def __init__(self, ratesec=1):
        self.config(ratesec)

    def config(self, ratesec):
        self.rate = ratesec
        self.sync()

    def sync(self, timenow=None):
        if timenow == None:
            timenow = time.time()
        self.nexttick = timenow + self.rate

    def check(self):
        """Maintain the timer and see if it is time for the next tick"""
        now = time.time()

        if now >= self.nexttick:
            # asynchronous tick, might drift, but won't stack up if late
            self.sync(now)
            return True

        return False

# END
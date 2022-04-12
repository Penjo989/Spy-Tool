import time

class Timer:
    def __init__(self, deltaTime):
        self.startTime = 0
        self.deltaTime = deltaTime

    def start(self):
        self.startTime = time.time()
    def isOver(self):
        return time.time() - self.startTime >= self.deltaTime
    def resetDelta(self, deltaTime):
        self.deltaTime = deltaTime
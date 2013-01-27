import time
import threading
# import XBMC

class Slider(object):
    """docstring for Slider"""
    totaltime = 0.0
    timeprefix = 0.0
    timestart = 0.0
    isRunning = False
    XBMC = None
    dead = False

    def __init__(self, XBMC):
        super(Slider, self).__init__()
        self.XBMC = XBMC
        self.XBMC.updateItem()
        self.reconfSlider()
        self.updateSlider()
        self.autoUpdateSlider()
        self.autoSetSlider()

    def play(self):
        self.isRunning = True
        self.updateSlider()

    def pause(self):
        self.updateSlider()
        self.isRunning = False

# get position of slider time/pct
    def getTime(self):
        currentTime = self.timeprefix
        if self.isRunning:
            currentTime += (time.time() - self.timestart)

        return currentTime

    def getPercent(self):
        if self.totaltime != 0:
            return self.getTime() / float(self.totaltime)
        else:
            return 0

# adjust state of slider
    def resetSlider(self):
        self.totaltime = 0.0
        self.timeprefix = 0.0
        self.timestart = 0.0
        self.isRunning = False

    def reconfSlider(self):
        totaltime = self.XBMC.getTotalTime()
        if totaltime is None:
            self.resetSlider()
        else:
            self.totaltime = totaltime

    def updateSlider(self):
        if self.totaltime is None:
            self.reconfSlider()
        if self.totaltime is not None:
            self.isRunning = self.XBMC.isPlaying()
            self.setTime(self.XBMC.getTime())
            self.setSlider()

    def setTime(self, newTime):
        if self.timeprefix != newTime:
            self.timeprefix = newTime
            if self.isRunning:
                self.timestart = time.time()

    def setPercent(self, newPercent):
        self.timeprefix = (newPercent * self.totaltime) / float(100)

    def setSlider(self):
        str_list = []
        str_list.append('setslider[')
        str_list.append('totaltime: ')
        str_list.append(repr(self.totaltime))
        str_list.append(' | time: ')
        str_list.append(repr(self.getTime()))
        str_list.append(' | pct: ')
        str_list.append(repr(self.getPercent()))
        str_list.append(' | running: ')
        str_list.append(repr(self.isRunning))
        str_list.append(']')
        print ''.join(str_list)

# Do stuff based on time
    def autoUpdateSlider(self):
        if not self.dead:
            self.updateSlider()
            threading.Timer(1, self.autoUpdateSlider).start()

    def autoSetSlider(self):
        if not self.dead:
            self.setSlider()
            threading.Timer(3, self.autoSetSlider).start()

    def stopAuto(self):
        self.dead = True

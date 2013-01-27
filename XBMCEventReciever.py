import socket
import json
from pprint import pprint
from sliderControler import Slider
from XBMC import XBMC


class XBMCEventReciever(object):
    """docstring for XBMCEventReciever"""
    XBMC = None
    slid = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    methodDict = None

    def __init__(self):
        super(XBMCEventReciever, self).__init__()
        self.XBMC = XBMC()
        if self.XBMC.playerExists():
            self.slid = Slider(self.XBMC)
        self.s.connect(('192.168.178.52', 9090))
        self.methodDict = {"Player.OnPlay": self.onPlay,
                           "Player.OnPause": self.onPause,
                           "Player.OnStop": self.onStop,
                           "Player.OnSeek": self.onSeek,
                          }

    def handleMsg(self, msg):
        jsonmsg = json.loads(msg)
        method = jsonmsg["method"]
        pprint(method)
        if method in self.methodDict:
            methodHandler = self.methodDict[method]
            methodHandler(json)

    def listen(self):
        currentBuffer = []
        msg = ""
        depth = 0
        while True:
            chunk = self.s.recv(1)
            for c in chunk:
                currentBuffer.append(c)

                if c == '{':
                    depth += 1
                elif c == '}':
                    depth -= 1
                    if not depth:
                        msg = ''.join(currentBuffer)
                        self.handleMsg(msg)
                        currentBuffer = []
        self.s.close()

    def onPlay(self, json):
        if self.slid is not None:
            self.slid.play()
        else:
            self.slid = Slider(self.XBMC)

    def onPause(self, json):
        if self.slid is not None:
            self.slid.pause()
        else:
            self.slid = Slider(self.XBMC)

    def onStop(self, json):
        self.slid.stopAuto()
        self.slid = None

    def onSeek(self, json):
        if self.slid is not None:
            self.slid.updateSlider()
        else:
            self.slid = Slider(self.XBMC)


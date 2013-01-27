import jsonrpclib


class XBMC(object):
    """docstring for XBMC"""
    server = jsonrpclib.Server('http://xbmc:xbmc@192.168.178.52:8081/jsonrpc')
    playerID = None
    currItem = None
    itemProp = ["time", "totaltime", "speed", "canchangespeed"]

    def __init__(self):
        super(XBMC, self).__init__()

    def playerExists(self):
        return self.updatePlayerID()

    def updatePlayerID(self):
        success = False
        try:
            players = self.server.Player.GetActivePlayers()

        except Exception, e:
            print e
            return success
        else:
            if len(players) > 0:
                self.playerID = players[0]["playerid"]
                success = True
            else:
                self.playerID = None
            return success

    def updateItem(self):
        if self.playerID is None:
            self.updatePlayerID()
        else:
            try:
                newcurrItem = self.server.Player.GetProperties(
                                            self.playerID, self.itemProp)
            except Exception, e:
                print e

            else:
                self.currItem = newcurrItem



    def getTotalTime(self):
        self.updateItem()
        if self.currItem is None:
            return None
        totaltime = self.currItem["totaltime"]
        returnval = (totaltime["hours"] * 3600 +
                     totaltime["minutes"] * 60 +
                     totaltime["seconds"] * 1 +
                     totaltime["milliseconds"] * 0.001)
        return returnval

    def getTime(self):
        self.updateItem()
        if self.currItem is None:
            return None
        time = self.currItem["time"]
        returnval = (time["hours"] * 3600 +
                     time["minutes"] * 60 +
                     time["seconds"] * 1 +
                     time["milliseconds"] * 0.001)
        return returnval

    def isPlaying(self):
        self.updateItem()
        if self.currItem is not None:
            if self.currItem["speed"] == 0:
                return False
            else:
                return True
        else:
            return False

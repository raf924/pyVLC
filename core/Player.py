# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject,  pyqtSlot,  pyqtSignal,  QVariant
import vlc
from threading import Thread
from core import Media

class Player(QObject,Thread):
    events = pyqtSignal([str], [str, QVariant])
    def __init__(self,instance=None, parent=None):
        QObject.__init__(self,  parent)
        Thread.__init__(self)
        self._nowPlaying = None
        self.player = vlc.MediaPlayer(instance)
    def run(self):
        self.attachEvent(vlc.EventType.MediaPlayerPositionChanged, self.get_position)
        self.attachEvent(vlc.EventType.MediaPlayerLengthChanged, self.get_length)
        self.attachEvent(vlc.EventType.MediaPlayerTimeChanged, self.get_time)
        self.attachEvent(vlc.EventType.MediaPlayerMediaChanged, self.nowPlaying)
        self.attachEvent(vlc.EventType.MediaPlayerPaused, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerPlaying, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerEndReached, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerStopped, self.getState)
    def attachEvent(self, event, callback=None):
        self.event_manager().event_attach(event, self.emit,event, callback)
    def getState(self):
        return hash(self.get_state())
    @pyqtSlot(QVariant)
    def seek(self, newPos):
        sT = Thread(None,self.player.set_time,None,(int(newPos),))
        sT.start()
    def emit(self, *args):
        eventType = str(args[0].type).split(".")[1]+".invlc.player"
        params = (eventType, )+args[2:]
        if len(params)==1:
            self.events[str].emit(eventType)
        else:
            self.events[str, QVariant].emit(*params)
    def nowPlaying(self):
        return self._nowPlaying
    def setLibrary(self,  library):
        self.library = library
    def setMedia(self,  location):
        self.player.set_mrl(location.encode("utf-8").decode("mbcs"))
    def __call__(self):
        return self.player
    def __getattr__(self,  name):
        return getattr(self.player, name)
    @pyqtSlot(str)
    @pyqtSlot(int)
    @pyqtSlot()
    def play(self, id=None):
        path = None
        if isinstance(id, int):
           path = self.library.getPath(id)
        if isinstance(id, str):
           path = id
        if id is None:
            t = Thread(None,self.player.play)
            t.start()
        else:
            self._nowPlaying = self.library.getSong(id)
            self.setMedia(path)
            self.play()

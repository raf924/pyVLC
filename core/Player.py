# -*- coding: utf-8 -*-
from PyQt5.QtCore import QObject,  pyqtSlot,  pyqtSignal,  QVariant
import vlc
from threading import Thread
from core import Media

def emit(event,*args):
    eventType = str(args[0]).split(".")[1]+".invlc.player"
    listeners = args[1].listeners
    value = args[2]()
    params = (eventType, value)
    for listener in listeners:
        listener.emitEvent(*params)

class Player(QObject,Thread):
    events = pyqtSignal([str], [str, QVariant])
    def __init__(self,player=None, parent=None):
        QObject.__init__(self,  parent)
        Thread.__init__(self)
        self.listeners = []
        self._nowPlaying = None
        self.player = player
    def addListener(self,listener):
        self.listeners.append(listener)
    def run(self):
        pass
        self.attachEvents()
    def detachEvents(self):
        self.detachEvent(vlc.EventType.MediaPlayerPositionChanged)
        self.detachEvent(vlc.EventType.MediaPlayerLengthChanged)
        self.detachEvent(vlc.EventType.MediaPlayerTimeChanged)
        self.detachEvent(vlc.EventType.MediaPlayerMediaChanged)
        self.detachEvent(vlc.EventType.MediaPlayerPaused)
        self.detachEvent(vlc.EventType.MediaPlayerPlaying)
        self.detachEvent(vlc.EventType.MediaPlayerEndReached)
        self.detachEvent(vlc.EventType.MediaPlayerStopped)
    def detachEvent(self,event):
        self.event_manager().event_detach(event)
    def attachEvents(self):
        self.attachEvent(vlc.EventType.MediaPlayerPositionChanged, self.get_position)
        self.attachEvent(vlc.EventType.MediaPlayerLengthChanged, self.get_length)
        self.attachEvent(vlc.EventType.MediaPlayerTimeChanged, self.get_time)
        self.attachEvent(vlc.EventType.MediaPlayerMediaChanged, self.nowPlaying)
        self.attachEvent(vlc.EventType.MediaPlayerPaused, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerPlaying, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerEndReached, self.getState)
        self.attachEvent(vlc.EventType.MediaPlayerStopped, self.getState)
    def attachEvent(self, event, callback=None):
        self.event_manager().event_attach(event, emit,event,self, callback)
    def getState(self):
        return hash(self.get_state())
    @pyqtSlot(QVariant)
    def seek(self, newPos):
        self.player.set_time(int(newPos))
    def nowPlaying(self):
        return self._nowPlaying
    def setLibrary(self,  library):
        self.library = library
    def setMedia(self,location):
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
            self.player.play()
        else:
            self._nowPlaying = self.library.getSong(id)
            self.setMedia(path)
            self.play()

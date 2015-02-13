from PyQt5.QtCore import QObject, pyqtSignal,  pyqtSlot,  QVariant,  pyqtProperty, pyqtBoundSignal
import vlc
#from web import htmlview
class WebInterface(QObject):
    close = pyqtSignal()
    currentMediaChanged = pyqtSignal(QVariant)
    expand = pyqtSignal()
    restore = pyqtSignal()
    expanded = pyqtSignal()
    restored = pyqtSignal()
    hide = pyqtSignal()
    play = pyqtSignal(int)
    pause = pyqtSignal()
    addFile = pyqtSignal()
    seek = pyqtSignal(QVariant)
    libraryUpdated = pyqtSignal()
    openFile = pyqtSignal()
    events = pyqtSignal(str, QVariant)
    
    def __init__(self,  parent=None):
        QObject.__init__(self, parent)
        self.songlist = []
        self._tags = []
        for i in range(22):
            self._tags.append(str(vlc.Meta(i)).split(".")[1])
        self._tags.append("Duration")
    @pyqtSlot(str)
    @pyqtSlot(str, QVariant)
    def emitEvent(self, *args):
        if len(args)==1:
            self.events.emit(args[0], "")
        else:
            params = ()
            for arg in args:
                p = arg
                if callable(arg):
                    p = arg()
                params = params + (p, )
            self.events[str, QVariant].emit(*params)
        
    @pyqtProperty(QVariant)
    def library(self):
        return self.songlist
    @pyqtSlot(str, str)
    @pyqtSlot(str)
    @pyqtSlot(dict)
    def action(self, actionData,  arg = None):
        print(actionData)
        action = None
        data = None
        if isinstance(actionData, str):
            action = actionData
            data = arg
        else :
            action = actionData["action"]        
            if "data" in actionData:
                data = actionData["data"]
        if isinstance(getattr(self, action), pyqtBoundSignal):
            method = getattr(self, action)
            if data is None:
                method.emit()
            else:
                method.emit(data)
        else:
            method(data)
    @pyqtProperty(QVariant)
    def tags(self):
        return self._tags

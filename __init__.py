# -*- encoding: utf-8 -*-
from core import *
from library import *
import ressources
from web import *
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import vlc

class Application(QApplication):
    def __init__(self, *args):
        import ctypes
        myappid = 'r@f924.pyvlc.0-1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        QApplication.__init__(self, *args)
        #instance = vlc.Instance(["-Incurse"])
        self.view = htmlview.HtmlView()
        self.view.view.load(QUrl.fromLocalFile(QFileInfo("html/index.html").absoluteFilePath()))
        self.view.setMinimumSize(830, 360)
        self.view.setWindowFlags(Qt.CustomizeWindowHint)
        self.library = Library.Library()
        self.updateLibrary()
        self.library.libraryUpdated.connect(self.updateLibrary)
        print("Library loaded")
        self.player = Player.Player(vlc.MediaPlayer())
        self.player.addListener(self.view.interface)
        self.player.start()
        print("Player loaded")
        self.view.show()
        self.player.setLibrary(self.library)
        self.view.interface.play.connect(self.player.play,Qt.QueuedConnection)
        self.view.interface.addFile.connect(self.addFile,Qt.QueuedConnection)
        self.view.interface.openFile.connect(self.openFile,Qt.QueuedConnection)
        #self.player.events[str].connect(self.view.interface.emitEvent,Qt.QueuedConnection)
        #self.player.events[str, QVariant].connect(self.view.interface.emitEvent,Qt.QueuedConnection)
        self.view.interface.seek.connect(self.player.seek,Qt.QueuedConnection)
        self.view.interface.pause.connect(self.player.pause,Qt.QueuedConnection)
        self.view.fileToAdd.connect(self.library.addFile)
        print("End of __init__")
    @pyqtSlot()
    def addFile(self):
        (file, filter) = QFileDialog.getOpenFileName(None, "Add a media to the library", None, "Audio (*.mp3 *.flac)")
        self.library.addFile(file)
    @pyqtSlot()
    def openFile(self):
        (file, filter) = QFileDialog.getOpenFileName(self, "Open a media", None, "Audio (*.mp3 *.flac)")
        self.fileToPlay.emit(file)
    def exec(self, *args):
        code = QApplication.exec(*args)
        try:
            self.player.stop()
        except:
            pass
        self.library.cur.close()
        return code
    @pyqtSlot()
    def updateLibrary(self):
        self.view.interface.songlist = self.library.songList()
        self.view.interface.libraryUpdated.emit()
if __name__ == "__main__":
    app = Application(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    code = app.exec()
    sys.exit(code)

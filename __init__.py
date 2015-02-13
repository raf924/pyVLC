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
        instance = vlc.Instance(["-Incurse"])
        self.view = htmlview.HtmlView()
        self.view.view.load(QUrl.fromLocalFile(QFileInfo("html/index.html").absoluteFilePath()))
        self.view.setMinimumSize(830, 360)
        self.view.setWindowFlags(Qt.CustomizeWindowHint)
        self.library = Library.Library()
        self.updateLibrary()
        self.library.libraryUpdated.connect(self.updateLibrary)
        print("Library loaded")
        self.player = Player.Player(instance)
        self.player.start()
        print("Player loaded")
        self.view.show()
        self.player.setLibrary(self.library)
        self.view.interface.play.connect(self.player.play)
        self.view.interface.addFile.connect(self.view.addFile)
        self.view.interface.openFile.connect(self.view.openFile)
        self.player.events[str].connect(self.view.interface.emitEvent)
        self.player.events[str, QVariant].connect(self.view.interface.emitEvent)
        self.view.interface.seek.connect(self.player.seek)
        self.view.interface.pause.connect(self.player.pause)
        print("End of __init__")
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
        print("songlist",self.view.interface.songlist)
        self.view.interface.libraryUpdated.emit()
if __name__ == "__main__":
    app = Application(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    code = app.exec()
    sys.exit(code)

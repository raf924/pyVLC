from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebKitWidgets import QWebInspector
import sys
from web import webview,  webinterface
from threading import Thread
class HtmlView(QWidget):
    instance = None
    fileToAdd = pyqtSignal(str)
    fileToPlay = pyqtSignal(str)
    def load(self, parent=None):
        if self.instance is None:
            self.instance = HtmlView()
        return self.instance
    def __init__(self, parent=None):
        print("init")
        super(HtmlView, self).__init__(parent)
        self.setupUi()
        self.interface = webinterface.WebInterface()
        self.setupConnections()
        
    def setupConnections(self):
        self.view.page().mainFrame().javaScriptWindowObjectCleared.connect(self.addInterface)
        self.interface.close.connect(self.close)
        self.interface.expand.connect(self.showMaximized)
        self.interface.restore.connect(self.showNormal)
        
    def setupUi(self):
        self.view = webview.WebView()
        self.view.setAcceptHoverEvents(True)
        scene = QGraphicsScene()
        scene.addItem(self.view)
        scene.setActiveWindow(self.view)
        self.gview = QGraphicsView(scene, self)
        self.gview.setFrameShape(QFrame.NoFrame)
        self.gview.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.gview.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.gview)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)
        if "dev" in sys.argv:
            print("Dev mode")
            inspector = QWebInspector()
            inspector.setPage(self.view.page())
            inspector.setVisible(True)
            inspector.show()
        self.setWindowIcon(QIcon("python.png"))  
        
    def event(self,  event):
        return QWidget.event(self, event)
        
    def resizeEvent(self,  event):
        self.gview.resize(QSize(self.size()))
        self.view.resize(QSizeF(self.size()))
        if self.isMaximized():
            self.interface.expanded.emit()
        elif not self.isMinimized():
            self.interface.restored.emit()
    @pyqtSlot()
    def addInterface(self):
        self.view.page().mainFrame().addToJavaScriptWindowObject("interface", self.interface)
        script = QFile(":application.js")        
        if script.open(QFile.ReadOnly):
            f = open("./application.js", "r")
            scr = f.read()
            f.close()
            self.view.page().mainFrame().evaluateJavaScript(scr)
            script.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    hView = HtmlView()
    hView.showMaximized()
    sys.exit(app.exec())

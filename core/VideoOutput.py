from PyQt5.QtWidgets import *
import sys
class VideoOutput(QWidget):
    instance = None
    def __init__(self,  parent=None):
        QWidget.__init__(self, parent)
        print("VideoOutput")
    def mouseDoubleClickEvent(self,  event):
        print("Event")
        if self.isFullScreen():
            if self.wasMaximized:
                self.showMaximized()
            else:
                self.showNormal()
        else:
            self.wasMaximized = self.isMaximized()
            self.showFullScreen()
    @classmethod
    def load(cls, parent=None):
        if cls.instance is None:
            cls.instance = VideoOutput(parent)
        cls.instance.setParent(parent)
        return cls.instance
if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = VideoOutput.load()
    v.show()
    sys.exit(app.exec())

from PyQt5.QtCore import *
import vlc
class Media(QObject):
    def __init__(self, location, parent=None):
        QObject.__init__(self,  parent)
        self.media = vlc.Media(location.encode("utf-8").decode("mbcs"))
        self.media.parse()
        self.metaData = self.getMetaData()
        
    def __call__(self):
        return self.media
    def getMetaData(self):
        self.media.parse()
        metaData = {}
        for i in range(0, 22):
            metaData[str(vlc.Meta(i)).split(".")[1]] = self.media.get_meta(i) 
        metaData["Duration"] = self.media.get_duration()
        return metaData

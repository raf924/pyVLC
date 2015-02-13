from PyQt5.QtWebKit import QWebPluginFactory
from core.VideoOutput import VideoOutput
class PluginsFactory(QWebPluginFactory):
    def __init__(self, parent=None):
        QWebPluginFactory.__init__(self, parent)
    def create(self,  *args):
        print(*args)
        return VideoOutput.load(self.parent())
    def plugins(self):
        plugin = QWebPluginFactory.Plugin
        plugin.name = "Video output"
        plugin.description = "A video output"
        plugin.mimeTypes = None
        return [plugin]

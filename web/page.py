from PyQt5.QtWebKit import  QWebSettings
from PyQt5.QtWebKitWidgets import QWebPage
from web.PluginsFactory import PluginsFactory
class Page(QWebPage):
    def __init__(self,  parent=None):
        QWebPage.__init__(self, parent)
        self.settings().setAttribute(QWebSettings.PluginsEnabled,  True)
        self.setPluginFactory(PluginsFactory())
    """def createPlugin(self,  classId, url, mNames, paramValues):
        if classId=="VideoOutput":
            return VideoOutput.load(self.view())
        return QWidget(self.view())"""

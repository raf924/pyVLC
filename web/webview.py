from PyQt5.QtWebKit import  QWebSettings
from PyQt5.QtWebKitWidgets import QGraphicsWebView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from web import page
import sys
class WebView(QGraphicsWebView):
    def __init__(self, item=None):
        QGraphicsWebView.__init__(self, item)
        self.settings().setAttribute(QWebSettings.PluginsEnabled,  True)
        self.setPage(page.Page())
        if 'dev' in sys.argv:
            self.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
"""
    def hoverMoveEvent(self, event):
        print(event.pos().x())
        left = False
        right = False
        bottom = False
        top = False
        if event.pos().x()==0:
            left = True
            self.setCursor(QCursor(Qt.SizeHorCursor))
        if event.pos().x()==self.size().width()-1:
            right = True
        if event.pos().y()==self.size().height()-1:
            bottom = True
        if event.pos().y()==0:
            top = True
        if bottom and left or top and right:
            self.setCursor(QCursor(Qt.SizeBDiagCursor))
        if bottom and right or top and left:
            self.setCursor(QCursor(Qt.SizeFDiagCursor))
        if not bottom and not top and not left and not right:
            QGraphicsWebView.hoverMoveEvent(self, event)
    """

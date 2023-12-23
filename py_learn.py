from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QUrl
from cProfile import Profile
class Browser(QtWebEngineWidgets.QWebEngineView):
    _windows = set()

    @classmethod
    def _removeWindow(cls, window):
        cls._windows.discard(window)

    @classmethod
    def newWindow(cls):
        window = cls()
        cls._windows.add(window)
        return window

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.page().geometryChangeRequested.connect(self.handleGeometryChange)
        self.page().titleChanged.connect(self.setWindowTitle)

    def closeEvent(self, event):
        self._removeWindow(self)
        event.accept()

    def handleGeometryChange(self, rect):
        window = QtGui.QWindow.fromWinId(self.winId())
        if window is not None:
            rect = rect.marginsRemoved(window.frameMargins())
        self.resize(rect.size())
        self.setFocus()
        self.show()

    def createWindow(self, mode):
        window = self.newWindow()
        if mode != QtWebEngineWidgets.QWebEnginePage.WebDialog:
            window.resize(800, 600)
            window.show()
        return window
def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    browser = Browser()
    browser.setUrl(QUrl("https://pylearn.ddns.net/"))
    browser.setGeometry(600, 100, 400, 200)
    browser.show()
    app.exec_()

if __name__ == '__main__':
    main()

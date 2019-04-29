import sys
import threading

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication

from webgui.home import app


def run_app(app_port=8050, debugging=False):
    app.run_server(port=app_port,
                   debug=debugging)


if __name__ == '__main__':
    port = 8050

    threading.Thread(target=run_app, args=(port, False), daemon=False).start()


    def _downloadRequested(item):  # QWebEngineDownloadItem
        print('downloading file to:', item.path())
        item.accept()


    qtapp = QApplication(sys.argv)

    web = QWebEngineView()
    web.setContextMenuPolicy(Qt.PreventContextMenu)
    web.page().profile().downloadRequested.connect(_downloadRequested)
    web.load(QUrl("http://127.0.0.1:8050"))
    web.show()

    sys.exit(qtapp.exec_())

    # run_app(debugging=True)

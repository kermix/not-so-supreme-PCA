import sys
import threading

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWidgets import QApplication

from misc import get_free_port_number
from webgui.home import app


def run_app(app_port=8050, debugging=False):
    app.run_server(port=app_port,
                   debug=debugging)


def _downloadRequested(item):  # QWebEngineDownloadItem
    print('downloading file to:', item.path())
    item.accept()


def start_gui():
    port = get_free_port_number()

    threading.Thread(target=run_app, args=(port, False), daemon=False).start()

    # qtapp = QApplication(sys.argv)

    # web = QWebEngineView()

    # web.setWindowTitle("Not so supreme PCA")
    # web.setWindowIcon(QIcon('icon.png'))
    # web.setContextMenuPolicy(Qt.PreventContextMenu)
    # web.page().profile().downloadRequested.connect(_downloadRequested)

    # web.load(QUrl("http://127.0.0.1:{}".format(port)))
    # web.showMaximized()

    # sys.exit(qtapp.exec_())

import os
import platform
import socket
import sys
from contextlib import closing


def activate_venv():
    script_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    system_type = platform.system().lower()

    if system_type == "windows":
        activate_this = os.path.join(script_path, r"Scripts\activate_this.py")
    elif system_type == "linux":
        activate_this = os.path.join(script_path, r"bin/activate_this.py")

        # Fixes segmentation fault when creating QtWebEngineView()
        # https://bugs.launchpad.net/ubuntu/+source/qtbase-opensource-src/+bug/1761708/comments/6
        os.environ['QT_XCB_GL_INTEGRATION'] = 'xcb_egl'
    elif system_type == 'darwin':
        activate_this = os.path.join(script_path, r"bin/activate_this.py")
    else:
        print("Not sure what to do on that OS")

    if os.path.exists(activate_this):
        exec(open(activate_this).read(), {'__file__': activate_this})
        return True

    return False


def get_free_port_number():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('127.0.0.1', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


if __name__ == '__main__':
    if activate_venv():
        import threading

        from PyQt5.QtCore import *
        from PyQt5.QtGui import *
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        from PyQt5.QtWidgets import QApplication

        from webgui.home import app


        def run_app(app_port=8050, debugging=False):
            app.run_server(port=app_port,
                           debug=debugging)


        port = get_free_port_number()

        threading.Thread(target=run_app, args=(port, False), daemon=False).start()


        def _downloadRequested(item):  # QWebEngineDownloadItem
            print('downloading file to:', item.path())
            item.accept()


        qtapp = QApplication(sys.argv)

        web = QWebEngineView()

        web.setWindowTitle("Not so supreme PCA")
        web.setWindowIcon(QIcon('icon.png'))
        web.setContextMenuPolicy(Qt.PreventContextMenu)
        web.page().profile().downloadRequested.connect(_downloadRequested)

        web.load(QUrl("http://127.0.0.1:{}".format(port)))
        web.showMaximized()

        sys.exit(qtapp.exec_())
    else:
        configure_script = {'linux': 'Please source configure.sh',
                            'windows': 'Please run configure.bat',
                            'darwin': 'Please source configure.sh. OSX in not fully supported.'}
        try:
            message = configure_script[platform.system().lower()]
        except KeyError:
            message = "Unsupported operating system."
        finally:
            print("Something went wrong. You dont have virtualenv in programdir.",
                  "{}".format())

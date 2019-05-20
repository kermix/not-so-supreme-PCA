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

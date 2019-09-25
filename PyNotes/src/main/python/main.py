from fbs_runtime.application_context.PySide2 import ApplicationContext
from PySide2.QtWidgets import QMainWindow

import sys

from package.main_window import MainWindow
from package.api.note import Notes

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    a = Notes()
    window = MainWindow(ctx=appctxt)
    window.resize(750, 750)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
from fbs_runtime.application_context.PySide2 import ApplicationContext, cached_property
from PySide2.QtWidgets import QMainWindow
from PySide2 import QtGui

import sys

from package.main_window import MainWindow

class AppContext(ApplicationContext):
    def run(self):
        self.main_window.show()
        return self.app.exec_()

    @cached_property
    def img_checked(self):
        return QtGui.QIcon(self.get_resource("images/checked.png"))

    @cached_property
    def img_unchecked(self):
        return QtGui.QIcon(self.get_resource("images/unchecked.png"))

if __name__ == '__main__':
    appctxt = AppContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(appctxt)
    window.resize(1920 / 4, 1200 / 2)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
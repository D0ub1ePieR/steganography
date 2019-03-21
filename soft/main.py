import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import *

if __name__ == '__main__':
    '''
        主函数入口
    '''
    app = QApplication(sys.argv)

    # 显示主界面
    main_window = mainwindow_ui()
    main_window.figure.show()

    sys.exit(app.exec_())
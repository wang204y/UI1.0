import image
import sys
import login
from PyQt5.QtWidgets import QApplication,QMainWindow
if __name__ == '__main__':
  myapp = QApplication(sys.argv)
  myDlg = QMainWindow()
  myUI = login.Ui_MainWindow()
  myUI.setupUi(myDlg)
  myDlg.show()
  sys.exit(myapp.exec_())
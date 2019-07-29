import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow,QWidget
from PyQt5.QtGui import QMovie
import os
from emss0726 import *
import image

class Ui(QMainWindow,Ui_MainWindow):   #定义Ui的类，继承Qmainwindow 类（护住创建和显示），和引用的类）
    def __init__(self,parent=None):
        super(Ui,self).__init__(parent)    #继承权
        self.setupUi(self)
        self.gif()
    def gif(self):
        self.movie = QMovie("./resource/beijin2.gif")
        self.label_RO_gif.setMovie(self.movie)
        self.movie.start()
        #创建界面内容

if __name__ ==  "__main__":
    app = QApplication(sys.argv)              #启动程序
    mywin = Ui()                              # 创建类中内容
    mywin.show()                              #内容显示
    sys.exit(app.exec())                      #循环


import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import QtSql
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
    #view.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('./PycharmProjects/mem.db')
    model = QtSql.QSqlTableModel()
    model.setTable('men1')


    model.select()
    view = QTableView()      #建立显示窗口对象实例
    view.setModel(model)     #将数据库装入窗口中
    view.clicked()
    dlg = QDialog()
    layout = QVBoxLayout()
    layout.addWidget(view)
    dlg.setLayout(layout)
    dlg.resize(400,500)
    dlg.show()
    # dlg = QDialog()
    # layout = QVBoxLayout()
    #
    # layout.addWidget(view)
    sys.exit(app.exec())
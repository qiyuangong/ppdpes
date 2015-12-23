#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial

In this example, we create a simple
window in PyQt4.

by Qiyuan Gong
qiyuangong@gmail.com

"""

import sys
from PyQt4 import QtGui


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        btn1 = QtGui.QPushButton(u'缺失数据匿名')
        btn1.setFixedHeight(80)
        # btn1.resize(btn1.sizeHint())
        gridlayout = QtGui.QGridLayout()
        gridlayout.setSpacing(10)
        gridlayout.setMargin(10)
        gridlayout.addWidget(btn1, 0, 0)
        # btn1.move(50, 25)
        btn2 = QtGui.QPushButton(u'高维数据匿名', self)
        btn2.setFixedHeight(80)
        # btn2.resize(btn2.sizeHint())
        gridlayout.addWidget(btn2, 1, 0)
        # btn2.move(50, 50)
        btn3 = QtGui.QPushButton(u'高维数据匿名', self)
        btn3.setFixedHeight(80)
        # btn3.resize(btn3.sizeHint())
        gridlayout.addWidget(btn3, 2, 0)
        # btn3.move(50, 75)
        edit = QtGui.QTextEdit('')
        # edit.resize(80, 60)
        gridlayout.addWidget(edit, 0, 2, 3, 2)
        # edit.move(300, 25)

        # self.setGeometry(500, 300, 500, 350)
        self.setWindowTitle(u'数据匿名原型系统')
        self.setLayout(gridlayout)
        self.resize(600, 500)
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

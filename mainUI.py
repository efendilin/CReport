# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1369, 772)
        font = QtGui.QFont()
        font.setFamily("新細明體")
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.treeReportView = QtWidgets.QTreeView(self.centralwidget)
        self.treeReportView.setGeometry(QtCore.QRect(4, 3, 301, 101))
        self.treeReportView.setObjectName("treeReportView")
        self.reportUP = QtWidgets.QPushButton(self.centralwidget)
        self.reportUP.setGeometry(QtCore.QRect(310, 3, 31, 31))
        self.reportUP.setObjectName("reportUP")
        self.reportDown = QtWidgets.QPushButton(self.centralwidget)
        self.reportDown.setGeometry(QtCore.QRect(310, 40, 31, 31))
        self.reportDown.setObjectName("reportDown")
        self.fileUP = QtWidgets.QPushButton(self.centralwidget)
        self.fileUP.setGeometry(QtCore.QRect(970, 3, 31, 31))
        self.fileUP.setObjectName("fileUP")
        self.fileDown = QtWidgets.QPushButton(self.centralwidget)
        self.fileDown.setGeometry(QtCore.QRect(970, 40, 31, 31))
        self.fileDown.setObjectName("fileDown")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(3, 110, 1361, 621))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textEEdit.setObjectName("textEEdit")
        self.horizontalLayout.addWidget(self.textEEdit)
        self.textCEdit = QtWidgets.QTextEdit(self.layoutWidget)
        self.textCEdit.setObjectName("textCEdit")
        self.horizontalLayout.addWidget(self.textCEdit)
        self.lineIDEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineIDEdit.setGeometry(QtCore.QRect(350, 5, 151, 21))
        self.lineIDEdit.setObjectName("lineIDEdit")
        self.Search = QtWidgets.QPushButton(self.centralwidget)
        self.Search.setGeometry(QtCore.QRect(510, 4, 31, 21))
        self.Search.setObjectName("Search")
        self.dirPath = QtWidgets.QLineEdit(self.centralwidget)
        self.dirPath.setGeometry(QtCore.QRect(1010, 5, 201, 21))
        self.dirPath.setObjectName("dirPath")
        self.DirButton = QtWidgets.QToolButton(self.centralwidget)
        self.DirButton.setGeometry(QtCore.QRect(1220, 10, 22, 18))
        self.DirButton.setObjectName("DirButton")
        self.fileList = QtWidgets.QTreeView(self.centralwidget)
        self.fileList.setGeometry(QtCore.QRect(687, 3, 281, 101))
        self.fileList.setObjectName("fileList")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1369, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.reportUP.setText(_translate("MainWindow", "PushButton"))
        self.reportDown.setText(_translate("MainWindow", "PushButton"))
        self.fileUP.setText(_translate("MainWindow", "PushButton"))
        self.fileDown.setText(_translate("MainWindow", "PushButton"))
        self.Search.setText(_translate("MainWindow", "PushButton"))
        self.DirButton.setText(_translate("MainWindow", "..."))


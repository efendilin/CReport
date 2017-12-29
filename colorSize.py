# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'colorSize.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ColorSizeDialog(object):
    def setupUi(self, ColorSizeDialog):
        ColorSizeDialog.setObjectName("ColorSizeDialog")
        ColorSizeDialog.resize(305, 147)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(ColorSizeDialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(ColorSizeDialog)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(ColorSizeDialog)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.spinBox = QtWidgets.QSpinBox(ColorSizeDialog)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(ColorSizeDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(ColorSizeDialog)
        self.buttonBox.accepted.connect(ColorSizeDialog.accept)
        self.buttonBox.rejected.connect(ColorSizeDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ColorSizeDialog)

    def retranslateUi(self, ColorSizeDialog):
        _translate = QtCore.QCoreApplication.translate
        ColorSizeDialog.setWindowTitle(_translate("ColorSizeDialog", "Dialog"))
        self.pushButton.setText(_translate("ColorSizeDialog", "前景"))
        self.pushButton_2.setText(_translate("ColorSizeDialog", "背景"))


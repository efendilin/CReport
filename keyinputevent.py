class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.lineEdit.setAttribute(Qt.WA_InputMethodEnabled)

        return

    def inputMethodEvent(self, a0: QtGui.QInputMethodEvent):

        print(a0)

        return

    def keyPressEvent(self, event: QtGui.QKeyEvent):

        print(event.text())

        return
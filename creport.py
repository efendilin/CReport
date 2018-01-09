# -*- coding: utf-8 -*-

import sys
#import subprocess
import requests
import re
import time
import win32clipboard
import win32con

from bs4 import BeautifulSoup
from os import walk, path, stat, linesep, getcwd, system
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from nmainUI import Ui_MainWindow
from hotstr import Ui_Dialog

class MyDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.dia = Ui_Dialog()
        self.dia.setupUi(self)

        self.shortcut = QtWidgets.QShortcut(Qt.QKeySequence("Enter"), self)
        self.shortcut.activated.connect(self.accept)

        #self.kl = pyHook.HookManager()
        #self.kl.KeyDown = self.KeyStroke
        #self.kl.HookKeyboard()

        return

    #def KeyStroke(self, event):
    #    Text = self.dia.lineEdit.text()
    #    Text = Text + chr(event.Ascii)
    #    self.dia.lineEdit.setText(Text)
    #    return True

    def getInputs(self):
        return self.dia.lineEdit.text()

class MyHighlighter( QtGui.QSyntaxHighlighter ):

    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightingRules = []

        keyword = Qt.QTextCharFormat()
        #keyword.setBackground(QtGui.QColor('darkYellow'))
        keyword.setBackground(QtGui.QColor(255, 229, 25))
        keyword.setFontWeight(Qt.QFont.Bold)

        warmword = Qt.QTextCharFormat()
        warmword.setForeground(QtGui.QColor(255, 85, 0))
        warmword.setFontWeight(Qt.QFont.Bold)

        malword = Qt.QTextCharFormat()
        malword.setForeground(QtGui.QColor(255, 0, 0))
        malword.setFontWeight(Qt.QFont.Bold)

        keywords = ["Diagnosis", "Brains:", "Whole Body:", "CONCLUSIONS", "Impression：", "Comment :"]
        warmwords = ['Fatty liver', 'Polyp', 'Polyps', 'cyst', 'cysts', 'stone', 'stones', 'adenoma', 'polyp']
        malwords = ['cancer', 'malignancy', 'malignant','carcinoma', 'adenocarcinoma', 'sacroma', 'lymphoma', 'metastastic']

        for word in keywords:
            pattern = Qt.QRegExp("\\b" + word)
            self.highlightingRules.append((pattern, keyword))

        for word in warmwords:
            pattern = Qt.QRegExp("\\b" + word + "\\b")
            self.highlightingRules.append((pattern, warmword))

        for word in malwords:
            pattern = Qt.QRegExp("\\b" + word + "\\b")
            self.highlightingRules.append((pattern, malword))

        self.highlightingRules.append((Qt.QRegExp("\\b^[0-9]{1,2}.\s\\b"), keyword))
        return

    def highlightBlock(self, text):
        if text:
            for pattern, keyword in self.highlightingRules:
                i = pattern.indexIn(text, 0)
                while i >= 0:
                    length = pattern.matchedLength()
                    self.setFormat(i, length, keyword)
                    i = pattern.indexIn(text, i + length)
        return

class MyTextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super(MyTextEdit, self).__init__(*args, **kwargs)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)

    def __contextMenu(self):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.phraseFunc()
        else:
            self._normalMenu = self.createStandardContextMenu()
            self._addCustomMenuItems(self._normalMenu)
            self._normalMenu.exec_(QtGui.QCursor.pos())

    def _addCustomMenuItems(self, menu):
        menu.addSeparator()
        menu.addAction('片語', self.phraseFunc)

    def phraseFunc(self):
        submenu = QtWidgets.QMenu()
        phymenu = submenu.addMenu("生理性")
        infmenu = submenu.addMenu("發炎")
        malgmenu = submenu.addMenu("惡性")
        mesmenu = submenu.addMenu("測量")
        echomenu = submenu.addMenu("超音波")
        ctmenu = submenu.addMenu("電腦斷層")
        fumenu = submenu.addMenu("追蹤")
        for key in keydict['phymenu']:
            phymenu.addAction(key, lambda term=keydict['phymenu'][key]: self.insertPlainText(term))
        for key in keydict['infmenu']:
            infmenu.addAction(key, lambda term=keydict['infmenu'][key]: self.insertPlainText(term))
        for key in keydict['mesmenu']:
            mesmenu.addAction(key, lambda term=keydict['mesmenu'][key]: self.insertPlainText(term))
        for key in keydict['echomenu']:
            echomenu.addAction(key, lambda term=keydict['echomenu'][key]: self.insertPlainText(term))
        for key in keydict['malgmenu']:
            malgmenu.addAction(key, lambda term=keydict['malgmenu'][key]: self.insertPlainText(term))
        for key in keydict['ctmenu']:
            ctmenu.addAction(key, lambda term=keydict['ctmenu'][key]: self.insertPlainText(term))
        for key in keydict['fumenu']:
            fumenu.addAction(key, lambda term=keydict['fumenu'][key]: self.insertPlainText(term))

        submenu.exec_(QtGui.QCursor.pos())
        return

class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        nmohighlight = MyHighlighter(self.ui.nmorep)
        pathhighlight = MyHighlighter(self.ui.pathreps)
        radhighlight = MyHighlighter(self.ui.radiorep)
        scopyhighlight = MyHighlighter(self.ui.scopyrep)
        othhighlight = MyHighlighter(self.ui.othersrep)


        self.ui.DirButton.clicked.connect(self.showFileDialog)
        self.ui.search.clicked.connect(self.searchF)
        self.ui.testDown.clicked.connect(self.testF)
        self.ui.saveClose.clicked.connect(lambda: self.saveF('close'))
        self.ui.saveOnly.clicked.connect(self.saveF)
        self.ui.genRep.clicked.connect(self.genRepF)
        #self.ui.actionFont_Size.triggered.connect()
        self.ui.actionFcolor.triggered.connect(self.colorFpicker)
        self.ui.actionBcolor.triggered.connect(self.colorBpicker)
        self.ui.sendButton.clicked.connect(self.Sender)
        self.ui.closeButton.clicked.connect(lambda :self.ui.tabCReport.removeTab(self.ui.tabCReport.currentIndex()))
        self.ui.VBox.addItem('')
        self.ui.RBox.addItem('')
        self.ui.VBox.addItems(ourVS)
        self.ui.RBox.addItems(ourR)

        #self.shortcut = QtWidgets.QShortcut(Qt.QKeySequence("F12"), self)
        #self.shortcut.activated.connect(self.thef12fun)

        return

    def GetClipboard(self):
        win32clipboard.OpenClipboard()
        temp = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
        win32clipboard.CloseClipboard()
        return temp

    def SetClipboard(self, text):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
        win32clipboard.CloseClipboard()
        return


    def thef12fun(self):
        currentFile = ''
        mydia = MyDialog(myapp)
        if mydia.exec_():
            hotkey = mydia.getInputs()
            if hotkey in hotkeystr:
                currentFile = self.ui.tabCReport.currentWidget().objectName()
                for Ctext in self.ui.tabCReport.findChildren(QtWidgets.QTextEdit, currentFile + 'Edit'):
                    Ctext.insertPlainText(hotkeystr[hotkey])

        return

    def sepdeler(self, text):
        lines = []
        for line in text.splitlines():
            if line.strip():
                lines.append(line)
        text = linesep.join(lines)
        return text


    def Sender(self):
        comm = str()
        petfind = str()
        sonofind = ''
        r = ""
        v = ""
        if self.ui.RBox.currentIndex():
            r = self.ui.RBox.currentText()
        if self.ui.VBox.currentIndex():
            v = self.ui.VBox.currentText()
        currentFile = self.ui.tabCReport.currentWidget().objectName()
        for Ctext in self.ui.tabCReport.findChildren(QtWidgets.QTextEdit, currentFile + 'Edit'):
            currentText = Ctext.toPlainText()
        temp = currentText.split('應注意事項與醫師總評 :')
        comm = self.sepdeler(temp[1])
        temp = temp[0].split('正子斷層造影判讀 :')
        petfind = self.sepdeler(temp[1])
        temp = temp[0]
        if '腹部超音波檢查 :' in temp:
            sonofind = self.sepdeler(temp.split('腹部超音波檢查 :')[1])
        ctext = comm + 'IamSep' + petfind + 'IamSep' + sonofind + 'IamSep' + r + 'IamSep' + v + 'IamSep' + currentFile
        #ctext = ctext.replace('\r','')
        self.SetClipboard(ctext)
        system("sender.exe")
        #authotkey_process = subprocess.Popen(["sender.exe", "*"], shell=False,\
        #                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,\
        #                                             stderr=subprocess.PIPE, encoding='cp950')
        #authotkey_process.communicate(ctext)
        #authotkey_process.kill()
        return

    def colorFpicker(self):
        textc = QtWidgets.QColorDialog.getColor()
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Text, textc)
        for Ctext in self.ui.tabCReport.findChildren(QtWidgets.QTextEdit):
            Ctext.setPalette(pal)
            #Ctext.setStyleSheet("font: 12pt \"細明體\";color:{}".format(color.name()))

        return

    def colorBpicker(self):
        backc = QtWidgets.QColorDialog.getColor()

        for Ctext in self.ui.tabCReport.findChildren(QtWidgets.QTextEdit):
            Ctext.setStyleSheet("QWidget {font: 14pt \"細明體\"; background-color: %s}" % backc.name())
        return


    def genRepF(self):
        pid = self.ui.pName.text().split(',')[0]
        if not self.nmonums:
            repPair = {}
            repsText = self.ui.nmorep.toPlainText()
            if repsText:
                for repCatText in repsText.split('------------END------------------'):
                    repTempText = [x for x in repCatText.split('\n') if x]
                    title = ''
                    for line in repTempText:
                        if not title:
                            if '----' in line:
                                title = line.split('----')[1].split(' ')[0]
                                repPair[title] = ''
                            else:
                                title = ''
                        if title:
                            if not '------------END------------------' in line:
                                repPair[title] = repPair[title] + line + linesep
        if len(self.nmonums) == 1:
            repForm = creptemp[1]
        else:
            repForm = creptemp[0] + linesep + creptemp[1]
            numwin = '血液癌症腫瘤篩檢皆在正常範圍。'
            if '生化血清' in self.nmonums:
                for line in self.nmonums['生化血清']:
                    if 'Red' in line[1]:
                        numwin = ''
                        if line[0] in makerTemp:
                            num = re.sub('<span style="font-weight:800; color:(Red|DarkRed)">', '', line[1]).replace('</span>','').strip()
                            #num = line[1].replace('<span style="font-weight:800; color:Red" >', '').replace('</span>','').strip()
                            repForm = repForm + linesep + '血液癌症腫瘤篩檢發現' + line[0] + ':' + makerTemp[line[0]].format(num)
                repForm = repForm + linesep + numwin

        object = self.ui.tabCReport.findChildren(QtWidgets.QTextEdit, pid + 'Edit')
        if object:
            for Ctext in object:
                Ctext.append(repForm)
        else:
            self.ui.pid = QtWidgets.QWidget()
            self.ui.tabCReport.addTab(self.ui.pid, pid)
            self.ui.pid.setObjectName(pid)
            self.gridLayout_2 = QtWidgets.QGridLayout(self.ui.pid)
            pid_edit = pid + 'Edit'  # 產生新的TextEdit
            self.ui.pid_edit = MyTextEdit(self.ui.pid)
            self.ui.pid_edit.setObjectName(pid_edit)
            self.ui.pid_edit.setAcceptRichText(0)
            self.gridLayout_2.addWidget(self.ui.pid_edit, 0, 0, 1, 1)
            self.ui.pid_edit.append(repForm)

        return

    def saveF(self, arug):
        currentFile = self.ui.tabCReport.currentWidget().objectName()
        for Ctext in self.ui.tabCReport.findChildren(QtWidgets.QTextEdit, currentFile + 'Edit'):
            currentText = Ctext.toPlainText()
        dname = self.ui.dirPath.text()
        if not dname:
            self.showFileDialog()
            dname = self.ui.dirPath.text()
        try:
            f = open(dname + '/' + currentFile + '.txt', 'w', encoding='utf8')
        except UnicodeDecodeError:
            f = open(dname + '/' + currentFile + '.txt', encoding='cp950')
        f.write(currentText)
        f.close()

        if arug == 'close':
            self.ui.tabCReport.removeTab(self.ui.tabCReport.currentIndex())
        return

    def openMenu(self, position):
        menu = QtWidgets.QMenu()
        self.actionA = menu.addAction("Quit")
        menu.exec_(self.ui.nmorep.viewport().mapToGlobal(position))
        return

    def cleanEtab(self):
        for textEdit in self.ui.tabEReport.findChildren(QtWidgets.QTextEdit):
            textEdit.clear()
        return

    def numPrinter(self, target, numlist):
        numitem = ""
        numitem = "{:^8} : {:^6}".format(numlist[0], numlist[1])
        if numlist[5]:
            numitem = numitem + " ({}) {}".format(numlist[5], numlist[2])
        else:
            numitem = numitem + " {}".format(numlist[2])
        if numlist[3]:
            numitem = numitem + ", 參考值( {:^5} - {:^5} )".format(numlist[3], numlist[4])
        if numlist[6]:
            numitem = numitem + ", 前次數值: {:^6} at {:^6}".format(numlist[6], numlist[7])
        if target == 'nmo':
            self.ui.nmorep.append(numitem)
        elif target == 'oth':
            self.ui.othersrep.append(numitem)
        else:
            print('faile')
        return

    def showFileDialog(self):
        dname = QtWidgets.QFileDialog.getExistingDirectory(self, 'Directory', '')
        if dname:
            self.ui.dirPath.setText(dname)
            if self.ui.tabCReport.count():
                s = self.ui.tabCReport.count()
                for i in range(s):
                    self.ui.tabCReport.removeTab(0)
            for (dirpath, dirnames, filenames) in walk(dname):
                filenames
                break
            #pal = QtGui.QPalette()
            #pal.setColor(QtGui.QPalette.Text, textc)
            #pal.setColor(QtGui.QPalette.Base, backc)

            for file in filenames:
                if ".txt" in file:
                    name = file.split('.')[0] #產生新的tab
                    self.ui.name = QtWidgets.QWidget()
                    self.ui.tabCReport.addTab(self.ui.name, name)
                    self.ui.name.setObjectName(name)
                    self.gridLayout_2 = QtWidgets.QGridLayout(self.ui.name)
                    name_edit = name + 'Edit' #產生新的TextEdit
                    self.ui.name_edit = MyTextEdit(self.ui.name)
                    self.ui.name_edit.setObjectName(name_edit)
                    self.ui.name_edit.setAcceptRichText(0)
                    self.ui.name_edit.setStyleSheet("font: 14pt \"細明體\"")
                    #self.ui.name_edit.setPalette(pal)
                    self.gridLayout_2.addWidget(self.ui.name_edit, 0, 0, 1, 1)

                    try:
                        f = open(dname + '/' + file, 'r', encoding='utf8')
                        self.ui.name_edit.setText(f.read())
                        f.close()
                    except UnicodeDecodeError:
                        f = open(dname + '/' + file,'r', encoding='cp950')
                        self.ui.name_edit.setText(f.read())
                        f.close()
        else:
            self.statusBar().showMessage("No Path is input !!!!!!")

        return
    def searchF(self):
        self.nmonums = {}
        repCount = [0,0,0,0,0,0]
        payloadi = {}
        pages = []
        pages.append('')
        tabpages =[]
        replink = []
        pid = self.ui.pID.text()
        if not pid:
            pid = self.ui.tabCReport.currentWidget().objectName()
            if not "tab" in pid:
                self.ui.pID.setText(pid)
            else:
                pid = ""
        if pid:
            self.cleanEtab()
            s =requests.Session()
            r = s.post(url, headers=headers)
            soup = BeautifulSoup(r.text, 'lxml')
            for i in range(4):
                payloadi[soup.find_all('input')[i]['name']] = soup.find_all('input')[i]['value']
            payloadi['txtASTR'] = txtASTR
            payloadi['txtCHRT'] = pid
            payloadi['dpDate'] = dpDate
            payloadi['dpKind'] = dpKind
            payloadi['btnQuery'] = btnQuery
            r = s.post(url, headers=headers, data=payloadi)
            soup = BeautifulSoup(r.text, 'lxml')
            payloadi[soup.find_all('input')[2]['name']] = soup.find_all('input')[2]['value']
            del payloadi['btnQuery']
            # get main page numbers and links
            # check if there is any report for the ID patient
            repnums = len(soup.find_all('a', text='內容'))
            prog = 0
            self.ui.progressBar.setValue(prog)
            if repnums:
                pages = []
                pages.append('')
                page = len(soup.find_all('table')[2].find_all('a')) - 15
                if page > 0:
                    for i in range(page):
                        pages.append(":".join(soup.find_all('table')[2].find_all('a')[15+i]['href'].split("'")[1].split("$")))
                progperpage = 100/len(pages)

                for page in pages:
                    replink = []
                    if page:
                        payloadi['__EVENTTARGET'] = page
                        r = s.post(url, headers=headers, data=payloadi)
                        soup = BeautifulSoup(r.text, 'lxml')
                        payloadi[soup.find_all('input')[2]['name']] = soup.find_all('input')[2]['value']
                # report link
                    repnums = len(soup.find_all('a', text='內容'))
                    progperrep = progperpage/repnums
                    for n in range(repnums):
                        replink.append(":".join(soup.find_all('a', text='內容')[n]['href'].split("'")[1].split("$")))
                    if replink:
                        for link in replink:
                            payloadi['__EVENTTARGET'] = link
                            r = s.post(url, headers=headers, data=payloadi)
                            soup = BeautifulSoup(r.text, 'lxml')
                            payloadi[soup.find_all('input')[2]['name']] = soup.find_all('input')[2]['value']
                            #get patient name
                            pname = soup.find_all('span', id="lblPnam")[0].text.strip()
                            psex = soup.find_all('span', id="lblSex")[0].text.strip()
                            pageold = soup.find_all('span', id="lblAge")[0].text.strip()
                            self.ui.pName.setText('{}, {} {} {}性'.format(pid, pname, pageold, psex))
                            drname = soup.find_all('span', id="lblDtid")[0].text.strip()
                            repkind = soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[2].text.strip()
                            repdate = soup.find_all('table')[2].find_all('tr', bgcolor="#FFCC66")[0].find_all('td')[1].text.strip()
                            if len(soup.find_all('table')) == 5:
                                reptext = soup.textarea.text
                                if reptext:
                                    if drname in ourVS:
                                        self.ui.nmorep.append(reptemp.format(repkind, repdate, drname, reptext))
                                        self.nmonums[repkind] = reptext
                                        repCount[0] += 1
                                    elif repkind == "病理細胞":
                                        self.ui.pathreps.append(reptemp.format(repkind, repdate, drname, reptext))
                                        repCount[2] += 1
                                    elif repkind == "放射科":
                                        self.ui.radiorep.append(reptemp.format(repkind, repdate, drname, reptext))
                                        repCount[3] += 1
                                    elif repkind == "內視鏡":
                                        self.ui.scopyrep.append(reptemp.format(repkind, repdate, drname, reptext))
                                        repCount[4] += 1
                                    else:
                                        self.ui.othersrep.append(reptemp.format(repkind, repdate, drname, reptext))
                                        repCount[5] += 1
                            elif len(soup.find_all('table')) == 6:
                                datalines = []
                                tpages = []
                                tpages.append('')
                                npage = len(soup.find_all('table')[4].find_all('a'))
                                if npage:
                                    for i in range(npage):
                                        tpages.append(":".join(soup.find_all('table')[4].find_all('a')[i]['href'].split("'")[1].split("$")))
                                starin = 0
                                for tpage in tpages:
                                    if tpage:
                                        starin = 1
                                        payloadi['__EVENTTARGET'] = tpage
                                        r = s.post(url, headers=headers, data=payloadi)
                                        soup = BeautifulSoup(r.text, 'lxml')
                                        payloadi[soup.find_all('input')[2]['name']] = soup.find_all('input')[2]['value']
                                    tnum = (len(soup.find_all('table')[4].find_all('td')) - 1)//8
                                    for l in range(starin, tnum):
                                        dataline = []
                                        for j in range(8):
                                            color = soup.find_all('table')[4].find_all('td')[l * 8 + j].font['color'].strip()
                                            word = soup.find_all('table')[4].find_all('td')[l * 8 + j].text.strip()
                                            if word:
                                                if color in colorneedch:
                                                    if '<' in word:word = word.replace('<','&lt;')
                                                    dataline.append(tempchcolor.format(color, word))
                                                elif j == 1:
                                                    dataline.append(tempchsize.format(word))
                                                else:
                                                    dataline.append(word)
                                            else:
                                                dataline.append(word)
                                        datalines.append(dataline)

                                for dataline in datalines:
                                    if drname in ourVS:
                                        if dataline[0] == '檢驗項目名稱':
                                            repCount[0] += 1
                                            self.ui.nmorep.append(reptitle.format(repkind, repdate, drname))
                                        else:
                                            self.numPrinter('nmo', dataline)
                                    else:
                                        if dataline[0] == '檢驗項目名稱':
                                            repCount[5] += 1
                                            self.ui.othersrep.append(reptitle.format(repkind, repdate, drname))
                                        else:
                                            self.numPrinter('oth', dataline)
                                if drname in ourVS:
                                    self.ui.nmorep.append('------------END------------------\r\n')
                                    self.nmonums[repkind] = datalines
                                else:
                                    self.ui.othersrep.append('------------END------------------\r\n')
                            else:
                                self.statusBar().showMessage("Unknow form of report !!!!!!")
                            prog = prog + progperrep
                            self.ui.progressBar.setValue(prog)
                self.ui.progressBar.setValue(100)
                self.ui.pID.clear()
                for index in range(len(repTabText)):
                    self.ui.tabEReport.setTabText(index, repTabText[index].format(str(repCount[index])))
            else:
                self.statusBar().showMessage("Worng ID or no report in recent one month !!!!!!")
        else:
            self.statusBar().showMessage("No ID input nor txt file !!!!!!")
        return

    def testF(self):
        if self.nmonums:
            repForm = creptemp[1]
            Text = self.nmonums['核醫']
            Temp = []
            for sent in Text.splitlines():
                if sent:
                    Temp.append(sent.strip())
            repsentlist = []

            Bend = 0
            if 'FINDINGS :' in Text:
                Rinit = Temp.index('FINDINGS :') + 1
            else:
                Rinit = 0
            if 'Whole Body:' in Temp:
                Binit = Temp.index('Whole Body:')
            elif 'Whole Body: Normal physiologic' in Temp:
                Binit = Temp.index('Whole Body: Normal physiologic')
            else:
                Binit = Rinit

            if Rinit > Binit:
                Brain = ' '.join(Temp[Rinit:Binit - 1]).replace('Brains:', '').strip()
                repsentlist.append(Brain)

            sentTemp = ''
            for sent in Temp[Binit + 1:]:
                if 'CONCLUSIONS :' in sent:
                    sent = ''
                elif 'Reported By' in sent:
                    sent = ''
                elif '核專醫字' in sent:
                    sent = ''

                if re.match('\d[.]\s', sent):
                    if sentTemp:
                        repsentlist.append(sentTemp)
                        sentTemp = sent
                    else:
                        sentTemp = sent
                else:
                    sentTemp = sentTemp + ' ' + sent
            repsentlist.append(sentTemp)
        Text = linesep.join(repsentlist)
        for key in eckeypair.keys():
            Text = Text.replace(key, eckeypair[key])

        clipboard.setText(Text)
        return


if __name__ == '__main__':

    #stylesheet = """
    #    QTabBar::tab:selected {background: gray;}
    #    QTabWidget>QWidget>QWidget{background: gray;}
    #    """

    global textc
    textc = QtGui.QColor(0, 0, 0)
    global backc
    backc = QtGui.QColor(255, 255, 255)
    global url
    url = 'http://10.1.150.73/RQS/webRQS.aspx'
    global headers
    headers = {'User-Agent': 'Mozilla/5.0'}
    global payloadi
    payloadi = {}
    global nmonums
    global matrix
    matrix = {}
    #numrepname = ['name','value','unit','refmin','refmax','value_status','prevalue','predate']
    txtASTR = ''
    dpDate = '一月內'
    dpKind = '所有檢查單'
    btnQuery= '查  詢'
    ourVS = ['陳遠光','沈業有','葉加祿','陳世緯']
    ourR = ['陳世緯','林聖哲','蘇奕鴒','周慧姍']

    reptemp = '''
----{} at {} by {}----\n
{}\n
------------END------------------\n
'''
    reptitle = '----{} at {} by {}----\n'
    tempchcolor = " <span style=\"font-weight:800; color:{}\"> {} </span> "
    tempchsize = " <span style=\"font-weight:800\"> {} </span> "
    colorneedch = ['Red','Blue','DarkRed']

    repTabText = ['NM開單 {}','NM {}','病理 {}','放射 {}', '內視鏡 {}' ,'Others {}']

    keycatlist = ['phymenu','infmenu','mesmenu','echomenu','malgmenu','ctmenu','fumenu']
    keydict = {}

    for list in keycatlist:
        try:
            f = open(list + ".txt", 'r', encoding='utf-8-sig')
        except UnicodeDecodeError:
            f = open(list + ".txt", 'r', encoding='cp950')
        temp = {}
        while True:
            t = f.readline()
            if t == '': break
            if ':' in t:
                keypair = t.strip().split(':')
                temp[keypair[0]] = keypair[1]
        keydict[list] = temp
        f.close()

    try:
        f = open('repTemp.txt', 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open('repTemp.txt', 'r', encoding='cp950')
    creptemp = f.read().split(';')
    f.close()

    makerTemp = {}
    try:
        f = open('makerTemp.txt', 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open('makerTemp.txt', 'r', encoding='cp950')
    while True:
        t = f.readline()
        if t == '': break
        if ':' in t:
            keypair = t.strip().split(':')
            makerTemp[keypair[0]] = keypair[1]

    hotkeystr = {}
    try:
        f = open('ketstrpair.txt', 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open('ketstrpair.txt', 'r', encoding='cp950')
    while True:
        t = f.readline()
        if t == '': break
        if '|' in t:
            keypair = t.strip().split('|')
            hotkeystr[keypair[0]] = keypair[1]

    eckeypair = {}
    try:
        f = open('eckeypair.txt', 'r', encoding='utf-8-sig')
    except UnicodeDecodeError:
        f = open('eckeypair.txt', 'r', encoding='cp950')
    while True:
        t = f.readline()
        if t == '': break
        if ':' in t:
            keypair = t.strip().split(':')
            eckeypair[keypair[0]] = keypair[1]

    app = QtWidgets.QApplication(sys.argv)
    clipboard = QtWidgets.QApplication.clipboard()
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
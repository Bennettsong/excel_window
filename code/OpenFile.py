# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import pandas as pd
import shutil
import os


class OpenFile(QDialog):
    def __init__(self, parent=None):
        super(OpenFile, self).__init__(parent)
        self.setWindowTitle('Open File')
        self.filepath = ""
        self.selectSheet = ''

        self.resize(330, 150)
        self.center()
        # 垂直布局按照从上到下的顺序进行添加按钮部件。
        vlayout = QVBoxLayout()

        self.btn1 = QPushButton("打开Excel文件")
        self.btn1.clicked.connect(self.getContent)
        self.fileName = QLabel("没有打开excel文件")
        self.le = QLabel("选择sheet")
        self.cb = QComboBox()
        # self.cb.addItem("请选择")
        # self.cb.currentIndexChanged.connect(self.selectionchange)

        vlayout.addWidget(self.btn1)
        vlayout.addWidget(self.fileName)
        vlayout.addWidget(self.le)
        vlayout.addWidget(self.cb)

        # 使用两个button(ok和cancel)分别连接accept()和reject()槽函数
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accepts)
        buttons.rejected.connect(self.rejects)

        vlayout.addWidget(buttons)

        self.setLayout(vlayout)

    def getContent(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        if dlg.exec_():
            filePath = dlg.selectedFiles()
            print(filePath)
            self.fileName.setText("打开的文件为:" + filePath[0])

            filename = os.path.basename(filePath[0])
            dirname = os.path.dirname(filePath[0]) + '/'
            filename1 = 'new_' + filename
            path1 = os.path.join(dirname, filename1)
            shutil.copy(filePath[0], path1)
            print(path1)

            sheetNames = pd.ExcelFile(path1).sheet_names
            print(sheetNames)
            self.cb.addItems(sheetNames)
            self.filepath = path1

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def getData(self):
        return self.filepath, self.selectSheet

    # def selectionchange(self, i):
    #     if i == 0:
    #         self.selectSheet = self.cb.itemText(1)
    #     else:
    #         self.selectSheet = self.cb.currentText()
    def accepts(self):
        self.selectSheet = self.cb.currentText()
        self.accept()

    def rejects(self):
        self.filepath = ""
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = OpenFile()
    form.show()
    sys.exit(app.exec_())

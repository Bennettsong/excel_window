# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class SetUp(QDialog):
    def __init__(self, fields, parent=None):
        super(SetUp, self).__init__(parent)
        self.setWindowTitle('设置相关值')

        self.search = ""
        self.display = []
        self.display_id = [0 for _ in range(len(fields))]
        self.information = ""
        self.confirm_value = ""

        self.resize(650, 650)
        self.center()
        self.fields = fields
        self.search_field = QLabel('查找的字段')
        self.confirm_field = QLabel('确定按钮默认值')
        self.display_field = QLabel('显示的字段')
        self.top_field = QLabel('顶端显示内容')

        self.search_edit = QComboBox()
        self.search_edit.addItems(fields)
        # self.search_edit.currentIndexChanged.connect(self.selectionchange)

        self.confirm_edit = QLineEdit()
        self.confirm_edit.setText("已注册")
        groupBox = QGroupBox("Checkboxes")
        groupBox.setFlat(False)

        layout = QHBoxLayout()
        for id_, txt in enumerate(fields):
            checkBox = QCheckBox(txt, self)
            checkBox.id_ = id_
            checkBox.stateChanged.connect(self.checkLanguage)  # 1
            layout.addWidget(checkBox)
        groupBox.setLayout(layout)

        self.top_edit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.search_field, 1, 0)
        grid.addWidget(self.search_edit, 1, 1)

        grid.addWidget(self.confirm_field, 2, 0)
        grid.addWidget(self.confirm_edit, 2, 1)

        grid.addWidget(self.display_field, 3, 0)
        grid.addWidget(groupBox, 3, 1)

        grid.addWidget(self.top_field, 4, 0)
        grid.addWidget(self.top_edit, 4, 1, 5, 1)


        # 使用两个button(ok和cancel)分别连接accept()和reject()槽函数
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        # buttons.accepted.connect(self.accept)
        buttons.accepted.connect(self.accepts)
        buttons.rejected.connect(self.reject)

        grid.addWidget(buttons, 10, 0, 1, 2)

        self.setLayout(grid)

    def checkLanguage(self, state):
        checkBox = self.sender()
        if state == Qt.Unchecked:
            self.display_id[checkBox.id_] = 0
        elif state == Qt.Checked:
            self.display_id[checkBox.id_] = 1

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def selectionchange(self, i):
        self.search = self.search_edit.currentText()

    def accepts(self):
        self.search = self.search_edit.currentText()
        for i in range(len(self.fields)):
            if self.display_id[i]:
                self.display.append(self.fields[i])
        self.information = self.top_edit.toPlainText()
        self.confirm_value = self.confirm_edit.text()
        self.accept()

    def rejects(self):
        self.reject()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    fields = ['用户名', '密码', '身高', '体重', '性别', '居住地']
    form = SetUp(fields)
    form.show()
    sys.exit(app.exec_())

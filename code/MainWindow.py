from PyQt5.QtWidgets import *
import sys
from OpenFile import OpenFile
from SetUp import SetUp
from dataStore import dataStore
import pandas as pd
import os



class MainWindow(QWidget):
    # data的格式应为[[],[],[]]
    def __init__(self, datastore):
        super().__init__()
        self.setWindowTitle('电子签到')
        self.resize(700, 700)
        self.center()

        self.datastore = datastore

        # 全局部件（注意参数 self），用于"承载"全局布局
        wwg = QWidget(self)

        # 全局布局（注意参数 wwg）
        wl = QVBoxLayout(wwg)

        vlayout = QVBoxLayout()
        self.information = QLabel('提示')
        # self.top_edit = QTextEdit()
        self.top_edit = QLabel(datastore.information)
        vlayout.addWidget(self.information)
        vlayout.addWidget(self.top_edit)

        hlayout = QHBoxLayout()
        self.search = QPushButton('查找')
        self.search.clicked.connect(self.search_btn)
        self.search_value = QLineEdit()
        self.confirm = QPushButton('确定')
        self.confirm.clicked.connect(self.confirm_btn)
        self.confirm_value = QLineEdit()
        hlayout.addWidget(self.search)
        hlayout.addWidget(self.search_value)
        hlayout.addWidget(self.confirm)
        hlayout.addWidget(self.confirm_value)

        conLayout = QHBoxLayout()
        self.tableWidget = QTableWidget()

        if not self.datastore.selectData.empty:
            self.tableWidget.setRowCount(len(self.datastore.selectData))
            self.tableWidget.setColumnCount(len(self.datastore.selectData[0]))
            for i in range(len(self.datastore.selectData)):
                for j in range(len(self.datastore.selectData[0])):
                    newItem = QTableWidgetItem(self.datastore.selectData[i][j])
                    self.tableWidget.setItem(i, j, newItem)
            # 设置列名
            self.tableWidget.setHorizontalHeaderLabels(self.datastore.display_field)
        conLayout.addWidget(self.tableWidget)
        # 将表格变为禁止编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 将行和列的大小设为与内容相匹配
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        # 设置有网格线
        self.tableWidget.setShowGrid(True)

        hlayout1 = QHBoxLayout()
        self.openFile = QPushButton('打开文件')
        self.openFile.clicked.connect(self.openfileButtonClick)
        self.setUp = QPushButton('设置')
        self.setUp.clicked.connect(self.setupButtonClick)
        # self.setUp.clicked.connect(lambda: self.setupButtonClick(self.datastore.columns))

        hlayout1.addWidget(self.openFile)
        hlayout1.addWidget(self.setUp)

        # 最下方显示打开的文件名
        vlayout1 = QVBoxLayout()
        self.openfile_information = QLabel('')
        vlayout1.addWidget(self.openfile_information)

        # 这里向局部布局内添加部件,将他加到全局布局
        wl.addLayout(vlayout)
        wl.addLayout(hlayout)
        wl.addLayout(conLayout)
        wl.addLayout(hlayout1)
        wl.addLayout(vlayout1)

    # 将窗口移到中央
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    # 点击打开文件按钮
    def openfileButtonClick(self):
        ofile = OpenFile(self)

        # 点击ok,result为1，cancel为0
        result = ofile.exec_()
        self.datastore.path, self.datastore.selectSheet = ofile.getData()
        print(self.datastore.path)
        print(self.datastore.selectSheet)
        print(result)
        ofile.destroy()
        # 显示打开的文件
        self.openfile_information.setText("打开的文件为：" + os.path.basename(self.datastore.path))

        self.open_file(self.datastore.path, self.datastore.selectSheet)

    def setupButtonClick(self):
        print(self.datastore.columns)
        setup = SetUp(self.datastore.columns)
        # 点击ok,result为1，cancel为0
        result = setup.exec_()
        self.datastore.search_field = setup.search
        self.datastore.display_field = setup.display[:]
        self.datastore.information = setup.information
        self.datastore.confirm_value = setup.confirm_value
        print(result)
        print(self.datastore.search_field)
        print(self.datastore.display_field)
        print(self.datastore.information)
        print(self.datastore.confirm_value)
        self.updateInformation()
        self.datastore.selectData = pd.DataFrame()
        # self.search_value.setText('')
        self.search_value.clear()
        self.updateTable()
        setup.destroy()

    # 设置表格数据内容
    def updateTable(self):
        if not self.datastore.selectData.empty:
            self.tableWidget.setRowCount(len(self.datastore.selectData))
            self.tableWidget.setColumnCount(len(self.datastore.selectData.iloc[0]))
            for i in range(len(self.datastore.selectData)):
                for j in range(len(self.datastore.selectData.iloc[0])):
                    newItem = QTableWidgetItem(self.datastore.selectData.iloc[i, j])
                    self.tableWidget.setItem(i, j, newItem)
            # 设置列名
            self.tableWidget.setHorizontalHeaderLabels(self.datastore.display_field)
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
            # 设置列名
            self.tableWidget.setHorizontalHeaderLabels(self.datastore.display_field)

    # 设置提示信息内容
    def updateInformation(self):
        self.top_edit.setText(self.datastore.information)

    # 打开文件,excel读进来就变成了一个DataFrame,并且新增一列到最后(默认将所有列的数据类型赋值为str类型)
    def open_file(self, path, sheet_name=0):
        # converters = {'ID': str, 'Age': str}  # 把from列和to列都转换为str类型
        try:
            # file = pd.read_excel(path, sheet_name=sheet_name, keep_default_na=False, converters=converters)
            print('进入到打开文件')
            print(path)
            print(sheet_name)
            self.datastore.data = pd.read_excel(path, sheet_name=sheet_name, keep_default_na=False, dtype=str)
            self.datastore.columns = list(self.datastore.data.columns)
            self.datastore.data['确认'] = ""
        except:
            print('导入失败')

    # 查找数据
    def filter_data(self, search, show_fileds):
        if show_fileds:
            data = self.datastore.data[self.datastore.data[search[0]] == search[1]][show_fileds]
        else:
            data = self.datastore.data[self.datastore.data[search[0]] == search[1]]
        # datas = np.array(data).tolist()
        return data

    # 查找按钮
    def search_btn(self):
        print("查询按钮的值为：" + self.search_value.text())
        # 清空确定框里面内容
        self.confirm_value.clear()
        self.datastore.selectData = pd.DataFrame()
        self.updateTable()
        if self.search_value.text():
            if self.datastore.search_field:
                search = [self.datastore.search_field, self.search_value.text()]
                show_fileds = self.datastore.display_field
                self.datastore.selectData = self.filter_data(search, show_fileds).copy(deep=True)
                if not self.datastore.selectData.empty:
                    self.updateTable()
                else:
                    QMessageBox.about(self, "提示", "没有查询到内容")


            else:
                QMessageBox.about(self, "警告", "请在设置中输入查询的字段")
        else:
            QMessageBox.about(self, "警告", "请输入查询的内容")

    # 修改值，默认最后一列，indexs为该条记录的索引，values为最后一列的值
    def update_data(self, indexs, values='已注册'):
        # flag表示是否修改，0表示修改
        flag = 0
        try:
            self.datastore.data.loc[indexs, '确认'] = values
        except:
            flag = 1
        return flag

    # 保存excel，flag为1表示成功，为0表示失败
    def save_file(self, path):
        flag = 1
        try:
            self.datastore.data.to_excel(path, index=None)
        except:
            flag = 0
        return flag

    def confirm_btn(self):
        if not self.datastore.selectData.empty:
            confirmValue = ""
            if self.confirm_value.text():
                confirmValue = self.confirm_value.text()
            else:
                if self.datastore.confirm_value:
                    confirmValue = self.datastore.confirm_value
                else:
                    confirmValue = "已注册"
            flag = self.update_data(self.datastore.selectData.index.values[0], confirmValue)
            if flag:
                QMessageBox.about(self, "提示", "数据确认失败")
            else:
                flag = self.save_file(self.datastore.path)
                if flag:
                    QMessageBox.about(self, "警告", "数据保存成功")
                else:
                    QMessageBox.about(self, "警告", "数据保存失败")
        else:
            QMessageBox.about(self, "警告", "没有数据可以确认，请选择数据")
        self.clear_data()

    def clear_data(self):
        self.search_value.clear()
        self.confirm_value.clear()
        self.datastore.selectData = pd.DataFrame()
        self.updateTable()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    datastore = dataStore()
    win = MainWindow(datastore)
    win.show()
    sys.exit(app.exec_())

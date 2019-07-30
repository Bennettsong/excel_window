import pandas as pd
class dataStore():
    def __init__(self):
        self.path = ""
        self.columns = []
        self.search_field = ""
        self.display_field = []
        self.confirm_value = "已注册"
        self.information = ""
        self.data = ""
        self.selectSheet = ""
        # 格式为[[],[],[]]
        self.selectData = pd.DataFrame()

    def setPath(self, path):
        self.path = path

    def getPath(self):
        return self.path

    def setColumns(self, columns):
        self.columns = columns

    def getColumns(self):
        return self.columns

    def setSearch_field(self, search_field):
        self.search_field = search_field

    def getSearch_field(self):
        return self.search_field

    def setDisplay_field(self, display_field):
        self.display_field = display_field

    def getDisplay_field(self):
        return self.display_field

    def setConfirm_value(self, confirm_value):
        self.confirm_value = confirm_value

    def getConfirm_value(self):
        return self.confirm_value

    def setInformation(self, information):
        self.information = information

    def getInformation(self):
        return self.information

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def setSelectData(self, selectData):
        self.selectData = selectData

    def getSelectData(self):
        return self.selectData

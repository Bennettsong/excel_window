import pandas as pd

path = r'file/test.xlsx'
# df = pd.read_excel(path).sheet_names()
df = pd.ExcelFile(path).sheet_names
print(df)

# 获取文件名和路径
import os
path1 = r'E:/CODE/python/pyqt/file/test.xlsx'
filename = os.path.basename(path1)
# test.xlsx
dirname = os.path.dirname(path1)
# E:/CODE/python/pyqt/file
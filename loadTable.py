import xlrd

fileLocation = "table.xlsx"
workbook = xlrd.open_workbook(fileLocation)
sheet = workbook.sheet_by_index(0)
sheet.call_value(0,0)
print(sheet.nrows)
print(sheet.ncols)
"""
for col in range(sheet.ncols):
	sheet.cell_value(1, col)#Login
	sheet.cell_value(2, col)#Heslo"""
for row in range(sheet.nrows):
	sheet.cell_value(row, 1)#Login
	sheet.cell_value(row, 2)#Heslo

data = [[sheet.cell_value(r,c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]


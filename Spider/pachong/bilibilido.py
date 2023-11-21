import xlrd

book=xlrd.open_workbook('bilibili2.xls')
table=book.sheets()[0]
print(table.cell(2,1))
import xlwt

workbook=xlwt.Workbook(encoding="utf-8") #创建workbook对象
worksheet=workbook.add_sheet('sheet1')
worksheet.write(0,0,'hello')
workbook.save('student.xls')


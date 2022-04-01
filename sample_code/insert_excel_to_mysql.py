import xlrd
import mysql
import mysql.connector

mysql_connection = mysql.connector.connect(user = 'root', password = 'Laijiachong1', host = 'localhost',database = 'crawler' )
cursor = mysql_connection.cursor()
sql_insert = "INSERT INTO project_chn \
   (省份, 城市, 公告类型, 信息标题, 项目名称,\
       招标编号, 招标预算_万元, 发布时间, 原文地址, 招标代理机构,\
           开标时间, 招标单位, 招标单位联系人, 招标单位联系方式, 招标单位地址,\
               中标单位, 中标金额_万元, 中标日期) \
                  VALUES (%s, %s, %s, %s, %s,\
                     %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s, %s,\
                           %s, %s, %s)"
sql_insert_simplified = "INSERT INTO project_chn_simplified \
   (省份, 城市, 公告类型, 项目名称,\
      招标预算_万元, 发布时间, 原文地址, 开标时间,\
         招标单位, 中标单位, 中标金额_万元, 中标日期) \
                  VALUES (%s, %s, %s, %s,\
                     %s, %s, %s, %s,\
                        %s, %s, %s, %s)"
#打开数据所在的工作簿，以及选择存有数据的工作表
book = xlrd.open_workbook("/Users/michael/Desktop/福清市公安局“城市交通大脑”监管及交通信号灯控制优化服务结果公告(包2).xls")
sheet = book.sheet_by_name("导出数据信息")
# 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题行
for r in range(1, sheet.nrows):
      a = sheet.cell(r, 0).value
      b = sheet.cell(r, 1).value
      c = sheet.cell(r, 2).value
      d = sheet.cell(r, 3).value
      e = sheet.cell(r, 4).value
      f = sheet.cell(r, 5).value
      g = sheet.cell(r, 6).value
      h = sheet.cell(r, 7).value
      i = sheet.cell(r, 8).value
      j = sheet.cell(r, 9).value
      k = sheet.cell(r, 10).value
      l = sheet.cell(r, 11).value
      m = sheet.cell(r, 12).value
      n = sheet.cell(r, 13).value
      o = sheet.cell(r, 14).value
      p = sheet.cell(r, 15).value
      q = sheet.cell(r, 16).value
      r = sheet.cell(r, 17).value
      #s = sheet.cell(r, int(19)).value

      values = (a, b, c, d, e,\
         f, g, h, i, j,\
            k, l, m, n, o,\
               p, q, r)
      vaules_simplified = (a, b, c, e,\
         g, h, i, k,\
            l, p, q, r)
      #print(vaules_simplified)
      try:   
         cursor.execute(sql_insert, values)
         mysql_connection.commit()
      except:
         continue
      
      cursor.execute(sql_insert_simplified, vaules_simplified)
      mysql_connection.commit()

#columns = str(sheet.ncols)
rows = str(sheet.nrows)
print ("导入 " + " 列 " + rows + " 行数据到MySQL数据库!")
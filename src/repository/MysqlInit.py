import pymysql
 
db_connection = pymysql.connect(host='localhost', user='root', password='123456',
                             database='NumberGuessGame', port=3306, charset='utf8mb4')


#获取游标
cursor = db_connection.cursor()
# 用完记得close掉
cursor.close()
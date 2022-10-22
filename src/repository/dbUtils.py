import pymysql
 
# db_connection  是一个对象，用来创建游标
db_connection = pymysql.connect(host='localhost', user='root', password='123456',
                             database='NumberGuessGame', port=3306, charset='utf8mb4')


#获取游标
cursor = db_connection.cursor()
# 用完记得close掉
cursor.close()


def execute_sql(sql: str)->None:
    cursor = db_connection.cursor()
    cursor.execute(sql)
    # cursor.execute("SELECT LAST_INSERT_ID()")
    # res = cursor.fetchall()
    res = cursor.lastrowid
    print("res:", res)
    # 提交后才会生效
    db_connection.commit()

    cursor.close()
    
def select_sql(sql: str)->tuple:
    cursor = db_connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    # print("-----cursor.fetchall()-----")
    # print(res)
    # print("-----cursor.fetchall()-----")
    cursor.close()
    return res
from typing import Tuple, List
import pymysql
from loguru import logger


# db_connection  是一个对象，用来创建游标
db_connection = pymysql.connect(host='localhost', user='root', password='123456',
                             database='NumberGuessGame', port=3306, charset='utf8mb4')


#获取游标
cursor = db_connection.cursor()
# 用完记得close掉
cursor.close()


def execute_sql(sql: str)->Tuple:
    try:
        cursor = db_connection.cursor()
        cursor.execute(sql)
        # cursor.execute("SELECT LAST_INSERT_ID()")
        res = cursor.fetchall()
        # 提交后才会生效
        db_connection.commit()
    except Exception as e:
        logger.debug(f"sql:{sql}")
        db_connection.rollback()
        raise
    finally:
        cursor.close()
    
    return res

# 以事务的方式执行若干sql语句。并依次返回结果集
def execute_sqls_in_transaction(sqls: List[str])->List[Tuple]:
    try:
        cursor = db_connection.cursor()
        res = []
        for sql in sqls:
            cursor.execute(sql)
            res.append(cursor.fetchall())
        # 提交后才会生效
        db_connection.commit()
        
    except Exception as e:
        print(f"出错！e={e}")
        db_connection.rollback()
        raise RuntimeError(e)
    finally:
        cursor.close()
    
    return res
    
def select_sql(sql: str)->tuple:
    try:
        cursor = db_connection.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
    except Exception as e:
        db_connection.rollback()
        raise    
    finally:
        cursor.close()
    
    return res
    

if __name__ == '__main__':
    # sql = "select * from player where id = 218"
    # res = execute_sql(sql) # ((218, "t'est", '20', 0, 'qwe', ''),)
    # print(res[0][1])
    # print(repr(print(res[0][1])))
    sql = f"select status from userstatus where user_id = 1"
    # logger.info("[Player::selectUserStatus]:sql="+sql)
    res = execute_sql(sql)
    print(res)
    db_connection.close()
    
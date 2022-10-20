import RoomPO
from BasePO import BasePO
from RoomPO import RoomPO
from typing import List, Tuple
from MysqlInit import db_connection # 是一个对象，用来创建游标
class BasesCRUD:
    
    select_by_id_pattern = "select * from {} where id = {}"
    insert_pattern = "insert into "
    
    def __init__(self) -> None:
        self.tableName = ""
        
        
    def insert(self, obj: BasePO):
        pass
    
    def delete(self, obj: BasePO):
        pass
    
    def update(self, obj: BasePO):
        pass
    
    # 通过一个ID访问，得到一个PO对象
    def selectById(self, id: int)->Tuple:
        cursor = db_connection.cursor()
        sql = self.select_by_id_pattern.format(self.tableName, id)
        cursor.execute(sql)
        res = cursor.fetchall()
        print("-----cursor.fetchall()-----")
        print(res)
        print("-----cursor.fetchall()-----")
        cursor.close()
        return res


class RoomCRUD(BasesCRUD):
    
    def __init__(self) -> None:
        super().__init__()
        self.tableName = "room"
    
    #重写方法
    def selectById(self, id: int)->Tuple:
        res = super().selectById(id)
        return RoomPO.db2po(res)
    
    
        
        
if __name__ == '__main__':
    roomCRUD = RoomCRUD()
    
    roomCRUD.selectById(1)
    
    
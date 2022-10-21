import RoomPO
from BasePO import BasePO
from RoomPO import RoomPO
from typing import List, Tuple
from MysqlInit import execute_sql, select_sql
from loguru import logger
import traceback
class BasesCRUD:
    
    
    
    def __init__(self) -> None:
        self.tableName = ""
        self.select_by_id_pattern = "select * from {} where id = {}"
        self.base_insert_pattern = "insert into {}{} values {}"
        
    def insert(self, obj: BasePO):
        pass
    
    def delete(self, obj: BasePO):
        pass
    
    def update(self, obj: BasePO):
        pass
    
    # 通过一个ID访问，得到一个PO对象
    def selectById(self, id: int)->Tuple:
        sql = self.select_by_id_pattern.format(self.tableName, id)
        res = select_sql(sql)
        return res


class RoomCRUD(BasesCRUD):
    
    def __init__(self) -> None:
        super().__init__()
        self.tableName = "room"
        self.columns = "(id,name,type,player_ids,history_game_ids)"
        self.insert_pattern = "insert into {}{} values {}".format(self.tableName,self.columns,"{}")
    
    #重写方法
    def selectById(self, id: int)->Tuple:
        res = super().selectById(id)[0] # 因为只有一个id
        return RoomPO.db2po(res)

    def insert(self, po: RoomPO)->bool:
        try:
            sql = self.insert_pattern.format(RoomPO.po2db_str(po))
            logger.info("[RoomCRUD::insert]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::insert] error={}".format(err))
    
        
        
if __name__ == '__main__':
    roomCRUD = RoomCRUD()
    
    roomCRUD.selectById(1)
    print("开始insert")
    roomCRUD.insert(RoomPO("namename",3,30,"[]","[]"))
    print("结束insert")
    
from BasePO import BasePO
from RoomPO import RoomPO
from PlayerPO import PlayerPO
from typing import List, Tuple
from dbUtils import execute_sql, execute_sqls_in_transaction, select_sql
from loguru import logger
import traceback
import json_serializer
class BaseCRUD:
    """任何一个表的crud都需要继承此类，并且重写__init__中的几个方法
    """
    
    _base_insert_pattern = "insert into {}{} values {};"
    _base_update_pattern = "update {} SET {} where {};"
    def __init__(self) -> None:
        """__init__里的都需要在子类中重写
        """
        self._tableName = ""
        self._select_by_id_pattern = "select * from {} where id = {};"
        self._select_max_id_pattern = "select max(id) from {};"
        
    def insert(self, obj: BasePO):
        pass
    
    # def delete(self, obj: BasePO):
    #     pass
    
    def update(self, obj: BasePO):
        pass
    
    # 通过一个ID访问，得到一个PO对象
    def selectById(self, id: int)->Tuple:
        sql = self._select_by_id_pattern.format(self._tableName, id)
        res = select_sql(sql)
        return res
    def selectMaxId(self)->int:
        sql = self._select_max_id_pattern.format(self._tableName)
        res = select_sql(sql)
        return res[0][0]


class _RoomCRUD(BaseCRUD):
    
    def __init__(self) -> None:
        super().__init__()
        self._tableName = "room"
        self._columns = RoomPO.columns_str
        self._insert_pattern = self._base_insert_pattern.format(self._tableName,self._columns,"{}")
        self._update_pattern = self._base_update_pattern.format(self._tableName, "{}", "id={}")
    
    #重写方法
    def selectById(self, id: int)->RoomPO:
        res = super().selectById(id)[0] # 因为只有一个id
        return RoomPO.db2po(res)

    def insert(self, po: RoomPO)->int:
        try:
            sql1 = self._insert_pattern.format(RoomPO.po2db_str(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[RoomCRUD::insert]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::insert] error={}".format(err))
    
    def update(self, po: RoomPO)->bool:
        try:
            sql = self._update_pattern.format(RoomPO.po2kv_str(po), po.id)
            logger.info("[RoomCRUD::update]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::update] error={}".format(err))        
            
      
        
class _PlayerCRUD(BaseCRUD):
    
    def __init__(self)->None:
        super().__init__()
        self._tableName = "player"
        self._columns = PlayerPO.columns_str
        self._insert_pattern = self._base_insert_pattern.format(self._tableName,self._columns,"{}")
        self._update_pattern = self._base_update_pattern.format(self._tableName, "{}", "id={}")
    
    def selectById(self, id: int)->PlayerPO:
        res = super().selectById(id)[0] # 因为只有一个id
        return PlayerPO.db2po(res)

    def insert(self, po: PlayerPO)->bool:
        try:
            sql = self._insert_pattern.format(PlayerPO.po2db_str(po))
            logger.info("[Player::insert]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[Player::insert] error={}".format(err))
        
    def _update(self, po: PlayerPO, kv: str)->bool:
        try:
            sql = self._update_pattern.format(kv, po.id)
            logger.info("[Player::update]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[Player::update] error={}".format(err))      
    
    def update(self, po: PlayerPO)->bool:
        self._update(po, PlayerPO.po2kv_str(po))
    def updateScore(self, po: PlayerPO)->bool:
        self._update(po, f'name={repr(po.score)}') 



roomCRUD = _RoomCRUD()
playerCRUD = _PlayerCRUD()
 
if __name__ == '__main__':
    
    
    # roomCRUD.selectById(1)
    print("开始insert")
    roomCRUD.insert(RoomPO(102,"namename",30,"[]","[]"))
    print("结束insert")
    
    # print("开始update")
    # roomCRUD.update(RoomPO(3,"namename",30,"[1,2]","[]"))
    # print("结束update")
    
    
    # po = playerCRUD.selectById(200)
    # poo = playerCRUD.selectById(201)
    # s = json_serializer.dump_to_json(po, outpu_encoding='utf8')
    # print(s)
    # print(json_serializer.dump_to_json(poo, outpu_encoding='utf8'))
    # poo = json_serializer.load_from_json(poo,s, input_encoding='utf8')
    # print(json_serializer.dump_to_json(poo, outpu_encoding='utf8'))
    
    # print("开始insert")
    # playerCRUD.insert(PlayerPO(208, "testname", 20, 0, "qqsdq+zsd+"))
    # print("结束insert")
    
    # print("开始update")
    # playerCRUD.update(PlayerPO(203, "testname203",20,0,"aawe+sdf"))
    # print("结束update")
    
    
    print("开始select最大id")
    print(roomCRUD.selectMaxId())
    print("结束select最大id")
    
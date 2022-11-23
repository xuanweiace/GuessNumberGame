from BasePO import BasePO
from RoomPO import RoomPO
from PlayerPO import PlayerPO
from GamePO import GamePO
from typing import List, Tuple, Union
from dbUtils import execute_sql, execute_sqls_in_transaction, select_sql
from loguru import logger
import traceback
import json_serializer
import sys
sys.path.insert(0,"../")
import constant
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
        self._select_by_name_pattern = "select * from {} where name = {};"
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
        self._columns_without_id = RoomPO.columns_str_without_id
        self._insert_pattern = self._base_insert_pattern.format(self._tableName,self._columns_without_id,"{}")
        self._update_pattern = self._base_update_pattern.format(self._tableName, "{}", "id={}")
    
    #重写方法
    def selectById(self, id: int)->RoomPO:
        res = super().selectById(id) # 因为只有一个id
        if len(res) == 0:
            return None
        return RoomPO.db2po(res[0])

    def insert(self, po: RoomPO)->int:
        try:
            sql1 = self._insert_pattern.format(RoomPO.po2db_str(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[RoomCRUD::insert]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            if len(res)>1:
                return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::insert] error={}".format(err))
            
    def insert_without_id(self, po: RoomPO)->int: # 返回id
        try:
            sql1 = self._insert_pattern.format(RoomPO.po2db_str_without_id(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[RoomCRUD::insert_without_id]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            if len(res)>1:
                return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::insert_without_id] error={}".format(err))
    
    def update(self, po: RoomPO)->bool:
        try:
            sql = self._update_pattern.format(RoomPO.po2kv_str(po), po.id)
            logger.info("[RoomCRUD::update]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::update] error={}".format(err))        
            
    def selectListByStatus(self, status: Union[int, list, tuple]) -> List[RoomPO]:
        try:
            if type(status) == int:
                sql = f"select * from {self._tableName} where status = {status}"
            else:
                sql = f"select * from {self._tableName} where status in {tuple(status)}"
            logger.info("[RoomCRUD::selectListByStatus]:sql="+sql)
            res = execute_sql(sql)
            return [RoomPO.db2po(x) for x in res]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[RoomCRUD::selectListByStatus] error={}".format(err))       
        
class _PlayerCRUD(BaseCRUD):
    
    def __init__(self)->None:
        super().__init__()
        self._tableName = "player"
        self._columns = PlayerPO.columns_str
        self._columns_without_id = PlayerPO.columns_str_without_id
        self._insert_pattern = self._base_insert_pattern.format(self._tableName,self._columns_without_id,"{}")
        self._update_pattern = self._base_update_pattern.format(self._tableName, "{}", "id={}")
        self._select_by_name_pattern = self._select_by_name_pattern.format(self._tableName, "{}")
        
    def selectById(self, id: int)->PlayerPO:
        res = super().selectById(id) # 因为只有一个id，所以要么是()，要么是形如((200, 'zxz', '20', 0, None, None),)
        if len(res) == 0:
            return None
        return PlayerPO.db2po(res[0])
    
    def selectByName(self, name: str)->PlayerPO:
        sql = self._select_by_name_pattern.format("'" + name + "'")
        res = execute_sql(sql)
        if len(res) == 0:
            return None
        return PlayerPO.db2po(res[0])

    def insert(self, po: PlayerPO)->int:
        try:
            sql1 = self._insert_pattern.format(PlayerPO.po2db_str_without_id(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[PlayerPO::insert]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            if len(res)>1:
                return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[Player::insert] error={}".format(err))
            raise
            
    def insert_without_id(self, po: PlayerPO)->int:
        try:
            sql1 = self._insert_pattern.format(PlayerPO.po2db_str_without_id(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[PlayerPO::insert_without_id]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            if len(res)>1:
                return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[Player::insert_without_id] error={}".format(err))
            raise
        
    def _update(self, po: PlayerPO, kv: str)->bool:
        try:
            sql = self._update_pattern.format(kv, po.id)
            logger.info("[Player::update]:sql="+sql)
            execute_sql(sql)
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[Player::update] error={}".format(err))      
            raise
    
    def update(self, po: PlayerPO)->bool:
        self._update(po, PlayerPO.po2kv_str(po))
    def updateScore(self, po: PlayerPO)->bool:
        self._update(po, f'name={repr(po.score)}') 
        
        
    def updateUserStatus(self, userId: int, status:int):
        try:
            sql = f'update userstatus set status = {status} where user_id = {userId}'
            logger.info("[Player::updateUserStatus]:sql="+sql)
            res = execute_sql(sql)       
        except:
            err = traceback.format_exc()
            logger.error("[Player::updateUserStatus] error={}".format(err))   
            raise           
        return  
    
    def insertUserStatus(self, userId: int, status: int):
        try:
            sql = f'insert into userstatus (`user_id`, `status`) VALUES ({userId}, {status})'
            logger.info("[Player::insertUserStatus]:sql="+sql)
            res = execute_sql(sql)       
        except:
            err = traceback.format_exc()
            logger.error("[Player::insertUserStatus] error={}".format(err))   
            raise           
        return  
    
    def selectUserStatus(self, userId: int)->int:
        """如果用户不存在（或者没有登录过），则返回None

        Args:
            userId (int): 用户id
        """
        try:
            sql = f"select status from userstatus where user_id = {userId}"
            logger.info("[Player::selectUserStatus]:sql="+sql)
            res = execute_sql(sql)
            if len(res) == 0: # ()
                return None
            return res[0][0]
        except:
            err = traceback.format_exc()
            logger.error("[Player::selectUserStatus] error={}".format(err))   
            raise


class _GameCRUD(BaseCRUD):
    
    def __init__(self)->None:
        super().__init__()
        self._tableName = "game"
        self._columns = GamePO.columns_str
        self._columns_without_id = GamePO.columns_str_without_id
        self._insert_pattern = self._base_insert_pattern.format(self._tableName,self._columns_without_id,"{}")
        self._update_pattern = self._base_update_pattern.format(self._tableName, "{}", "id={}")
        
    def selectById(self, id: int)->PlayerPO:
        res = super().selectById(id) # 因为只有一个id，所以要么是()，要么是形如((200, 'zxz', '20', 0, None, None),)
        if len(res) == 0:
            return None
        return GamePO.db2po(res[0]) 
    
    def insert_without_id(self, po: GamePO)->int:
        try:
            sql1 = self._insert_pattern.format(GamePO.po2db_str_without_id(po))
            sql2 = self._select_max_id_pattern.format(self._tableName)
            logger.info("[GamePO::insert_without_id]:sql1="+sql1+"\nsql2="+sql2)
            res = execute_sqls_in_transaction([sql1, sql2])
            if len(res)>1:
                return res[1][0][0]
        except Exception as e:
            err = traceback.format_exc()
            logger.error("[GamePO::insert_without_id] error={}".format(err))
            raise


roomCRUD = _RoomCRUD()
playerCRUD = _PlayerCRUD()
gameCRUD = _GameCRUD()

if __name__ == '__main__':
    
    
    # roomCRUD.selectById(1)
    # print("开始insert")
    # roomCRUD.insert(RoomPO(103,"namename",30,"[]","[]"))
    # print("结束insert")
    
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
    
    po = playerCRUD.selectById(218)
    print(po.name)
    
    
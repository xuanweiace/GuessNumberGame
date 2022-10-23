import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from BaseObject import Room, Player
from constant import ObjectType, Color
from typing import List, Dict, Tuple
from BasePO import BasePO

# 除了BO的信息之外，还存了这个房间都进行了哪些游戏
# PO 类信息还要承载，和db交互和数据格式转换的功能。
# PO和BO的转换可以在BO中实现。
class RoomPO(BasePO):
    
    columns_str = "(id,name,type,player_ids,history_game_ids)"
    
    def __init__(self, roomId: int, name:str, roomType: ObjectType, playerIds: str, historyGameIds:str) -> None:
        """注意playerid存的是字符串！！！不是列表！！转化成BO的时候再eval一下即可。
            
        """
        super().__init__(roomId, name, roomType)

        self.playerIds = playerIds # str 存的是List[int]
        self.historyGameIds = historyGameIds # str 存的是List[int]
    
    @staticmethod
    def db2po(t:Tuple)->"RoomPO":
        """将数据库的元组转换成PO对象

        Args:
            t (Tuple): eg：(1, 'room_test', 40, '[]', '[]')
        """
        roomId = t[0]
        name = t[1]
        roomType = t[2]
        players = t[3]
        historyGameIds = t[4]
        return RoomPO(name, roomId, roomType, players, historyGameIds)
    
    @staticmethod
    def po2db(po: "RoomPO")->Tuple:
        """将数据库信息转化成db里要的格式（tuple）

        Args:
            po (RoomPO): RoomPO类型的po对象
        """
        
        return (po.id,po.name, po.type, str(po.playerIds), str(po.historyGameIds))
        
        
    @staticmethod
    def po2db_str(po: "RoomPO")->str:
        # # todo 可以这样吗？ 对象调用静态方法
        return repr(po.po2db(po))
    
    @staticmethod
    def po2kv_str(po: "RoomPO")->str:
        return f"id={po.id},name={repr(po.name)},type={po.type},player_ids={repr(po.playerIds)},history_game_ids={repr(po.historyGameIds)}"
    
    @staticmethod
    def bo2po(bo: "Room")->"RoomPO":
        # todo RoomPO.historyGameIds这个字段弃用了
        return RoomPO(bo.id, bo.name, bo.type, repr([x.id for x in bo.players]), '[]')
    
       
    
    
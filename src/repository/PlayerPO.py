import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from BaseObject import Room, Player
from constant import ObjectType, Color
from typing import List, Dict, Tuple
from BasePO import BasePO

class PlayerPO(BasePO):
    
    columns_str = "(id,name,type,score,portrait)"
    columns_str_without_id = "(name,type,score,portrait)"
    def __init__(self, id:str, name: str, playerType: ObjectType, score: int, portrait: str) -> None:
        super().__init__(id, name, playerType)
        self.score=score
        self.portrait=portrait
        
    def self2bo(self):
        return Player(self.id, self.name, self.type, self.score, self.portrait)
        
    @staticmethod
    def db2po(t:Tuple)->"PlayerPO":
        """将数据库的元组转换成PO对象

        Args:
            t (Tuple): eg：(201, 'zzz', 20, 0, '+Xz4asdzxczxcxz'
        """
        id = t[0]
        name = t[1]
        playerType = t[2]
        score = t[3]
        portrait = t[4]
        return PlayerPO(id, name, playerType, score, portrait)
    
    
    @staticmethod
    def po2db(po: "PlayerPO")->Tuple:
        """将数据库信息转化成db里要的格式（tuple）

        Args:
            po (PlayerPO): PlayerPO类型的po对象
        """
        
        return (po.id,po.name, po.type, po.score, po.portrait)
    
    
    @staticmethod
    def po2db_str(po: "PlayerPO")->str:
        return repr(po.po2db(po))
    
    @staticmethod
    def po2db_str_without_id(po: "PlayerPO")->str:
        return repr(po.po2db(po)[1:])
    
    @staticmethod
    def po2kv_str(po: "PlayerPO")->str:
        return f"id={po.id},name={repr(po.name)},type={po.type},score={po.score},portrait={repr(po.portrait)}"
    
    @staticmethod
    def po2kv_str_without_id(po: "PlayerPO")->str:
        return f"name={repr(po.name)},type={po.type},score={po.score},portrait={repr(po.portrait)}"   
    
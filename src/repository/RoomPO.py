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
class RoomPO(Room, BasePO):
    
    def __init__(self, name:str, roomId: int, roomType: ObjectType, players: List[Player], historyGameIds:List[int]) -> None:
        super().__init__(name, roomId, roomType, players)
        self.historyGameIds = historyGameIds
    
    @staticmethod
    def db2po(t:Tuple):
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
    def hello(self, q):
        pass
    
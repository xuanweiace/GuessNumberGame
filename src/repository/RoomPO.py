from ..BaseObject import Room, Player
from constant import ObjectType, Color
from typing import List, Dict
from BasePO import BasePO

# 除了BO的信息之外，还存了这个房间都进行了哪些游戏
class RoomPO(Room, BasePO):
    
    def __init__(self, name, roomId: int, roomType: ObjectType, players: List[Player], historyGameIds:List[int]) -> None:
        super().__init__(name, roomId, roomType, players)
        self.historyGameIds = historyGameIds
        
    
    
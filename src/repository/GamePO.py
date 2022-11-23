import os
import sys
import json

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from BaseObject import Room, Player
from constant import ObjectType, Color
from typing import List, Dict, Tuple
from BasePO import BasePO
from BaseObject import Game, Board
import json_serializer
class GamePO(BasePO):
    columns_str = "(id,name,type,playerBoards,publicBoard,status)"
    columns_str_without_id = "(name,type,playerBoards,publicBoard,status)"
    
    def __init__(self, id, name, type, playerBoards: str, publicBoard: str, status:int) -> None:
        super().__init__(id, name, type)
        self.playerBoards = playerBoards # dict[Board]
        self.publicBoard = publicBoard # Board
        self.status = status
    
    def asBO(self):
        d = json.loads(self.playerBoards)
        for k in d:
            d[k] = json_serializer.load_from_json(Board(), d[k])
        pubBoard = json_serializer.load_from_json(self.publicBoard)
        return Game(self.id, self.name, self.type, d, pubBoard, self.status)
    
    def bo2po(bo: Game)->"GamePO":
        d = {}
        for k in bo.playerBoards:
            d[k] = json_serializer.dump_to_json(d[k])
        plaBoard = json.dumps(d)
        pubBoard = json_serializer.dump_to_json(bo.publicBoard)
        return GamePO(bo.id, bo.name, bo.type, plaBoard, pubBoard, bo.status)
    
    @staticmethod
    def po2db(po: "GamePO")->Tuple:
        return (po.id,po.name, po.type, str(po.playerBoards), str(po.publicBoard), po.status)
        
    @staticmethod
    def po2db_str(po: "GamePO")->str:
        return "'" + repr(po.po2db(po))[1:-1]+"'" # 用repr是为了让字符串边界转换成单引号 用到了repr的地方都要小心！
    
    @staticmethod
    def po2db_str_without_id(po: "GamePO")->str:
        return repr(po.po2db(po)[1:]).replace('"',"'")
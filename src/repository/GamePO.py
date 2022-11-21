import os
import sys


current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from BaseObject import Room, Player
from constant import ObjectType, Color
from typing import List, Dict, Tuple
from BasePO import BasePO
from BaseObject import Game, Board
class GamePO(BasePO):
    columns_str = "(id,name,type,score,portrait)"
    columns_str_without_id = "(name,type,score,portrait)"
    
    def __init__(self, id, name, type, playerBoards: dict[Board], publicBoard:Board, status:int) -> None:
        super().__init__(id, name, type)
        self.playerBoards = playerBoards
        self.publicBoard = publicBoard
        self.status = status
    
    def asBO(self):
        return Game(self.id, self.name, self.type, self.playerBoards, self.publicBoard, self.status)
    
    
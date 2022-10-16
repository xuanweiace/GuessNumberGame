from constant import ObjectType, Color
from typing import List, Dict
class BaseObject:
    def __init__(self, name: str, type: ObjectType) -> None:
        self.name = name
        self.type = type

# 注意value是str不是int
class Card(BaseObject):
    def __init__(self, name: str, cardType: ObjectType, color: Color, value:str) -> None:
        super().__init__(name, cardType)
        self.color = color
        self.value = value
    
# score为该玩家得分，从数据库中读取。
# todo 待确定。 portrait为该玩家设置的头像，暂定base64编码保存到数据库中。
class Player(BaseObject):
    def __init__(self, name: str, playerType: ObjectType, score: int, portrait:str) -> None:
        super().__init__(name, playerType)
        self.score = score
        self.portrait = portrait   
        
class Board(BaseObject):
    def __init__(self, name, boardType, cards: List[Card], player: Player) -> None:
        super().__init__(name, boardType)
        self.cards = cards;
        self.player = player
    
class Game(BaseObject):
    def __init__(self, name, gameType: ObjectType, playerBoards: List[Board], publicBoard: Board) -> None:
        super().__init__(name, gameType)
        self.playerBoards = playerBoards
        self.publicBoard = publicBoard



if __name__ == '__main__':
    baseObject = BaseObject("名字","普通类型")
    print(baseObject.name)
    
    
    c = Card("蓝1", ObjectType.NORMAL_CARD, Color.BLUE, "K")
    print(c.color)
    print(c.type)
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


class Room(BaseObject):
    """
    目前限制一个Room里最多有两个玩家
    为了避免过多的依赖关系，Room只记录有那几个玩家，不记录当前游戏号等信息。如需要请去repository层取。

    Args:
        BaseObject (_type_): _description_
    """
    
    def __init__(self, name, roomId:int, roomType: ObjectType, players: List[Player]) -> None:
        """初始化一个room，玩家信息是需要的，不能只存游戏，然后去游戏里找玩家。
            因为建好房间后可以只进入一个玩家，或者两个玩家都准备了但是没有开始游戏

        Args:
            name (str): room的名字，暂时没有作用
            roomId (int): roomid，是一个1开头的10位整数
            roomType (ObjectType): 房间类型，目前只有NORMAL_ROOM
            players (List[Player]): 玩家信息
        """
        super().__init__(name, roomType)
        self.id = roomId
        self.players = players
        
    def addPlayer(self, player: Player)->bool:
        if len(self.players) >= 2:
            return False
        self.players.append(player)
        return True
        

if __name__ == '__main__':
    baseObject = BaseObject("名字","普通类型")
    print(baseObject.name)
    
    
    c = Card("蓝1", ObjectType.NORMAL_CARD, Color.BLUE, "K")
    print(c.color)
    print(c.type)
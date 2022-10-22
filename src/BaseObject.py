from constant import ObjectType, Color
from typing import List, Dict

"""
BO层的子对象必须要存实体了，不能只存id了（比如room里的player），因为要涉及到和客户端交互了。
"""
class BaseObject:
    def __init__(self, id: int, name: str, type: ObjectType) -> None:
        self.id = id
        self.name = name
        self.type = type

# 注意value是str不是int
class Card(BaseObject):
    def __init__(self, cardId: int, name: str, cardType: ObjectType, color: Color, value:str) -> None:
        super().__init__(cardId, name, cardType)
        self.color = color
        self.value = value
    
# score为该玩家得分，从数据库中读取。
# todo 待确定。 portrait为该玩家设置的头像，暂定base64编码保存到数据库中。
class Player(BaseObject):
    def __init__(self, playerId,  name: str, playerType: ObjectType, score: int, portrait:str) -> None:
        super().__init__(playerId, name, playerType)
        self.score = score
        self.portrait = portrait
        
class Board(BaseObject):
    def __init__(self, boardId, name, boardType, cards: List[Card], player: Player) -> None:
        super().__init__(boardId, name, boardType)
        self.cards = cards
        self.player = player
    
class Game(BaseObject):
    def __init__(self, gameId, name, gameType: ObjectType, playerBoards: List[Board], publicBoard: Board) -> None:
        super().__init__(gameId, name, gameType)
        self.playerBoards = playerBoards
        self.publicBoard = publicBoard
        self.gameState = "ready" # [ready running over]


class Room(BaseObject):
    """
    目前限制一个Room里最多有两个玩家
    本来打算：为了避免过多的依赖关系，Room只记录有那几个玩家，不记录当前游戏号等信息。如需要请去repository层取。
    现在打算：Room里还是要存Game信息的，同时需要冗余存player信息。因为可能有player没有game。
    """
    
    def __init__(self, roomId:int, name, roomType: ObjectType, players: List[Player]) -> None:
        """初始化一个room，玩家信息是需要的，不能只存游戏，然后去游戏里找玩家。
            因为建好房间后可以只进入一个玩家，或者两个玩家都准备了但是没有开始游戏

        Args:
            name (str): room的名字，暂时没有作用
            roomId (int): roomid，是一个1开头的10位整数
            roomType (ObjectType): 房间类型，目前只有NORMAL_ROOM
            players (List[Player]): 玩家信息
        """
        super().__init__(roomId, name, roomType)
        self.players = players
        self.game = None
    
    def newGame(self):
        assert len(self.players) == 2
        # if len(self.players) != 2:
        #     raise RuntimeError("创建游戏错误，玩家个数为:"+str(len(self.players)))
        
    
    def addPlayer(self, player: Player)->bool:
        if len(self.players) >= 2:
            return False
        self.players.append(player)
        return True
        

if __name__ == '__main__':
    baseObject = BaseObject(1, "名字","普通类型")
    print(baseObject.name)
    
    
    c = Card("蓝1", ObjectType.NORMAL_CARD, Color.BLUE, "K")
    print(c.color)
    print(c.type)
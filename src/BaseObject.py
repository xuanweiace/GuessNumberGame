from constant import ObjectType, Color
from typing import List, Dict
from json_serializer import *
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
    def __init__(self, cardId: int=0, name: str="", cardType: ObjectType=ObjectType.NORMAL_CARD, color: Color=Color.BLUE, value:str="value") -> None:
        super().__init__(cardId, name, cardType)
        self.color = color
        self.value = value
    
# score为该玩家得分，从数据库中读取。
# todo 待确定。 portrait为该玩家设置的头像，暂定base64编码保存到数据库中。
class Player(BaseObject):
    def __init__(self, playerId=0,  name: str="", playerType: ObjectType=ObjectType.NORMAL_PLAYER, score: int=0, portrait:str="") -> None:
        super().__init__(playerId, name, playerType)
        self.score = score
        self.portrait = portrait
        
class Board(BaseObject):
    def __init__(self, boardId=0, name="", boardType=ObjectType.PUBLIC_BOARD, cards: List[Card]=FixedTypeList(Card,[]), player: Player=Player()) -> None:
        super().__init__(boardId, name, boardType)
        self.cards = cards
        self.player = player
    
class Game(BaseObject):
    def __init__(self, gameId=0, name="", gameType: ObjectType=ObjectType.ONLINE_GAME, playerBoards: List[Board]=FixedTypeList(Board, []), publicBoard: Board=Board()) -> None:
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
    def __init__(self, roomId:int =0, name:str ="123", roomType: ObjectType =ObjectType.NORMAL_ROOM, players: List[Player] =FixedTypeList(Player, []), status:int=0) -> None:
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
        self.status = status
    
    def newGame(self):
        assert len(self.players) == 2
        self.game = Game()
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
    
    c = Card(1, "blue1", ObjectType.NORMAL_CARD, Color.BLUE, "K")
    print(c.color)
    print(c.type)
    
    player = Player(100, "player100", ObjectType.NORMAL_PLAYER, 13, "")
    from json_serializer import dump_to_json, load_from_json
    
    board = Board(1, "board1", ObjectType.PLAYER_BOARD, [c], player)
    game = Game(300, "game300", ObjectType.ONLINE_GAME, FixedTypeList(Board, [board]), board)
    
    print(dump_to_json(game))
    
    s_str = dump_to_json(game)
    
    g_obj = Game(0, "")
    g_obj = load_from_json(g_obj, s_str)
    
    print(g_obj.publicBoard.cards[0].name)
    
    c2 = Card(2, "blue2", ObjectType.NORMAL_CARD, Color.BLUE, "K2")

    cards = [c, c2]
    print("-----"*10)
    print(cards)
    ss = dump_to_json(cards)
    print(ss)
    cs = FixedTypeList(Card, [])
    print(load_from_json(cs,ss))
    print("-----"*10)
    print(cs)
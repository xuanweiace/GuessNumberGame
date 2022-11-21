from enum import Enum
# 用枚举的好处，在静态类型推断的时候，可以方便的找到定位
class Color:
    YELLOW = 1
    BLUE = 2

# 初步决定把所有ObjectType放到一起
class ObjectType:
    NORMAL_CARD = 10
    UNDERLINE_CARD = 11
    
    NORMAL_PLAYER = 20
    
    PLAYER_BOARD = 30
    PUBLIC_BOARD = 31
    
    NORMAL_ROOM = 40
    
    ONLINE_GAME = 90
    OFFLINE_GAME = 91
    
class UserStatus:
    ONLINE = 1
    OFFLINE = 2
    
class GameStatus:
    RUN = 1
    OVER = 2

class RoomStatus: 
    IDLE = 0 # 空闲
    BUSY = 1 # 繁忙（游戏中）
    DESTROYED = 2 # 销毁
    
if __name__ == '__main__':
    print(UserStatus.ONLINE == UserStatus(1))
    
    print(UserStatus.ONLINE.__class__(2))
    print(str(UserStatus.ONLINE))
    
    d = {"userstatus": UserStatus.ONLINE}
    import json
    
    print(json.dumps(d))
    
    

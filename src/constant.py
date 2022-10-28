from enum import Enum

class Color(Enum):
    YELLOW = 1
    BLUE = 2

# 初步决定把所有ObjectType放到一起
class ObjectType(Enum):
    NORMAL_CARD = 10
    UNDERLINE_CARD = 11
    
    NORMAL_PLAYER = 20
    
    PLAYER_BOARD = 30
    PUBLIC_BOARD = 31
    
    NORMAL_ROOM = 40
    
    ONLINE_GAME = 90
    OFFLINE_GAME = 91
    
class UserStatus(Enum):
    ONLINE = 1
    OFFLINE = 2
    
    
    
if __name__ == '__main__':
    print(UserStatus.ONLINE == UserStatus(1))
    
    print(UserStatus.ONLINE.__class__(2))
    print(str(UserStatus.ONLINE))
    
    d = {"userstatus": UserStatus.ONLINE}
    import json
    
    print(json.dumps(d))
    
    

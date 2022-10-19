from BaseObject import Room
import time
import constant
class RoomGenerator:
    """生成一个人RoomBO
    """
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def generateRoom()->Room:
        """房间id为生成一个1开头的十位数
            eg. 1666197514
        Returns:
            Room: _description_
        """
        # todo 生成方式
        roomId = int(time.time())
        return Room("normal room", roomId, constant.ObjectType.NORMAL_ROOM, [])
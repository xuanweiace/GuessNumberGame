from BaseObject import Room
import time
import constant
from repository.crud import roomCRUD
class RoomGenerator:
    """生成一个RoomBO
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
        roomId = roomCRUD.selectMaxId() + 1
        return Room(roomId, "房间"+str(roomId), constant.ObjectType.NORMAL_ROOM, [], [])
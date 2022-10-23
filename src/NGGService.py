from repository.RoomPO import RoomPO
from repository.crud import roomCRUD, playerCRUD
from Generator import RoomGenerator



class NGGService:
    def __init__(self) -> None:
        
        pass
    
    def createRoom(userId:int)->int:
        """
        用户userId想要创建房间，我们只需要分配一个房间号roomId返回即可，同时把roomid和userid绑定关系存一下。
        这是向外提供的接口，所以：
            1、userID需要做校验
            2、只需要userID就行了，不需要完整player信息
        """
        # todo 需要解决并发问题
        room = RoomGenerator.generateRoom()
        roomid = roomCRUD.insert(RoomPO.bo2po())
        return roomid
        
    def createGame():
        # todo
        pass
        
        
        
        
        
nggService = NGGService()   
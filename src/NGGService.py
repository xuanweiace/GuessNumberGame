from CODE import pack_err_dict, pack_success_dict
from repository.RoomPO import RoomPO
from repository.crud import roomCRUD, playerCRUD
from Generator import RoomGenerator
from BaseObject import Room, Player
import constant
import err
import json_serializer

class NGGService:
    def __init__(self) -> None:
        
        pass
    
    def createRoom(self, data: dict)->dict:
        """
        用户userId想要创建房间，我们只需要分配一个房间号roomId返回即可，同时把roomid和userid绑定关系存一下。
        这是向外提供的接口，所以：
            1、userID需要做校验
            2、只需要userID就行了，不需要完整player信息
        """
        # todo 需要解决并发问题
        username:int = data["username"]
        roomname:str = data["roomname"]
        player = playerCRUD.selectByName(username)
        if player == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户名不存在")
        playerBO = player.self2bo()
        room = Room(-1, roomname, constant.ObjectType.NORMAL_ROOM, [playerBO])
        roomid = roomCRUD.insert_without_id(RoomPO.bo2po(room))
        return pack_success_dict({"roomid":roomid, "roomname":roomname})
    
    def listOpenRoom(self, data: dict)->dict:
        """房间状态 0等待中 1已开始 2已销毁
            入参dict没有用
        """
        roomPOs = roomCRUD.selectListByStatus([0,1])
        rooms = [x.self2bo() for x in roomPOs]        
        
        return pack_success_dict(json_serializer.dump_to_json(rooms))
        
    def createGame():
        # todo
        pass
        
    
    def getHandler(self, api: str):
        if api == 'create_room':
            return self.createRoom
        elif api == 'list_open_room':
            return self.listOpenRoom
        
        else:
            return None
        
        
nggService = NGGService()   
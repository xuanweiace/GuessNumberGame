from CODE import pack_err_dict, pack_success_dict, pack_notify_dict
from repository.RoomPO import RoomPO
from repository.GamePO import GamePO
from repository.crud import roomCRUD, playerCRUD, gameCRUD
from Generator import RoomGenerator
from BaseObject import Room, Player, Game
import constant
import err
import json_serializer
import NGGContext
from loguru import logger

class NGGService:
    def __init__(self) -> None:
        pass
    
    async def createRoom(self, data: dict)->dict:
        """
        用户username想要创建房间，我们只需要分配一个房间号roomId返回即可，同时把roomid和userid绑定关系存一下。
        这是向外提供的接口，所以：
            1、username需要做校验
            2、只需要username就行了，不需要完整player信息
        """
        # todo 需要解决并发问题
        username:int = data["username"]
        roomname:str = data["roomname"]
        player = playerCRUD.selectByName(username)
        if player == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户名不存在")
        playerBO = player.self2bo()
        patchy_room = Room(-1, roomname, constant.ObjectType.NORMAL_ROOM, [playerBO])
        roomid = roomCRUD.insert_without_id(RoomPO.bo2po(patchy_roomroom))
        patchy_room.setId(roomid) # 为了规范 set一下，不过没有用
        return pack_success_dict({"roomid":roomid, "roomname":roomname})
    
    async def listOpenRoom(self, data: dict)->dict:
        """房间状态 0等待中 1已开始 2已销毁
            入参dict没有用
        """
        roomPOs = roomCRUD.selectListByStatus([0,1])
        rooms = [x.self2bo() for x in roomPOs]        
        
        return pack_success_dict(json_serializer.dump_to_json_obj(rooms))
    
    async def enterRoom(self, data: dict)->dict:
        """一个user进入房间 
        1.根据username拿到userid 根据roomId拿到room信息 
        2.判断是否可以进入房间
        3.落库
        4.通知另一玩家(如有)
        Args:
            data (dict): 需要包含username,roomid

        Returns:
            dict: 包含整个的房间信息
        """
        username:int = data["username"]
        roomid: int =  data["roomid"]
        
        playerPO = playerCRUD.selectByName(username)
        roomPO = roomCRUD.selectById(roomid)
        if playerPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户信息不存在")
        if roomPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "房间信息不存在")
        player = playerPO.self2bo()
        room = roomPO.self2bo()
        
        # 判断是否已经在房间里
        if room.containPlayer(player):
            return pack_err_dict(err.ER.ALREADY_IN_ROOM, f"玩家{player.name}已经在房间{room.id}里")
        # 判断房间状态是否不是【等待中】
        if room.status != constant.RoomStatus.IDLE:
            return pack_err_dict(err.ER.ROOM_STATUS_NOT_WAITING, f"房间已开始或销毁 room status:{room.status}")
        # 判断房间人数已满
        if len(room.players) >= 2:
            return pack_err_dict(err.ER.ROOM_IS_FULL, f"房间已满无法加入len(room.players)={len(room.players)}")
        
        # 把player加入房间 并落库
        room.addPlayer(player)
        roomCRUD.update(RoomPO.bo2po(room))
        # 推送到其他player那里
        if len(room.players) == 2:
            tar_userid = room.players[0]
            try:
                await NGGContext.push_to_user(username, pack_notify_dict("room_refresh", json_serializer.dump_to_json_obj(room)))
            except Exception as e:
                logger.warning(f"[NGGService enetrRoom] 发送到user={tar_userid}失败,原因是{e}")
        return pack_success_dict(json_serializer.dump_to_json_obj(room))
        
    async def leaveRoom(self, data: dict)->dict:
        """一个user退出房间 
        1.根据username拿到userid 根据roomId拿到room信息 
        2.判断是否可以退出房间
        3.落库
        4.通知另一玩家(如有)
        Args:
            data (dict): 需要包含username,roomid

        Returns:
            dict: 包含整个的房间信息
        """
        username:int = data["username"]
        roomid: int =  data["roomid"]
        
        playerPO = playerCRUD.selectByName(username)
        roomPO = roomCRUD.selectById(roomid)
        if playerPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户信息不存在")
        if roomPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "房间信息不存在")
        player = playerPO.self2bo()
        room = roomPO.self2bo()
        # 判断房间状态是否不是【等待中】
        if room.status != constant.RoomStatus.IDLE:
            return pack_err_dict(err.ER.ROOM_STATUS_NOT_WAITING, f"房间已开始或销毁 room status:{room.status}")
        # 判断玩家是否在房间内
        if not room.containPlayer(player):
            return pack_err_dict(err.ER.ROOM_IS_FULL, f"玩家{player.name}不在房间号{roomid}里")
        
        # 把player加入房间 并落库
        room.removePlayer(player)
        roomCRUD.update(roomPO.bo2po(room))
        # 推送到其他player那里
        if len(room.players) == 1:
            tar_userid = room.players[0]
            try:
                await NGGContext.push_to_user(username, pack_notify_dict("room_refresh", json_serializer.dump_to_json_obj(room)))
            except Exception as e:
                logger.warning(f"[NGGService enetrRoom] 发送到user={tar_userid}失败,原因是{e}")       
                
        return pack_success_dict(json_serializer.dump_to_json_obj(room))
    
    async def createGame(self, data:dict)->dict:
        """创建新游戏 现在是房间内的任意玩家都可以创建游戏
        1.根据username拿到userid 根据roomId拿到room信息 
        2.判断是否可以开始游戏(房间内需要两名玩家)
        3.初始化一个Game并落库 room修改为busy状态
        4.通知另一玩家
        Args:
            data (dict): 需要包含username,roomid

        Returns:
            dict: 包含整个的房间信息
        """
        username:int = data["username"]
        roomid: int =  data["roomid"]    
        
        playerPO = playerCRUD.selectByName(username)
        roomPO = roomCRUD.selectById(roomid)
        if playerPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户信息不存在")
        if roomPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "房间信息不存在")
        player = playerPO.self2bo()
        room = roomPO.self2bo()    
        
        if len(room.players) != 2:
            return pack_err_dict(err.ER.ROOM_IS_NOT_FULL, f"房间未满，玩家数量为{len(room.players)}")

        # 判断房间状态是否不是【等待中】
        if room.status != constant.RoomStatus.IDLE:
            return pack_err_dict(err.ER.ROOM_STATUS_NOT_WAITING, f"房间已开始或销毁 room status:{room.status}")
        
        patchy_game = Game(-1, "api_create_game")
        gameId = gameCRUD.insert_without_id(GamePO.bo2po(patchy_game))
        
        game = patchy_game
        game.setId(gameId)
        room.setGame(game)
        room.setStatus(constant.RoomStatus.BUSY)
        # 落库
        roomCRUD.update(RoomPO.bo2po(room))
        gameCRUD.update(GamePO.bo2po(game))
        
        
    def _terminateGame(self, game: Game):
        game.status = constant.GameStatus.OVER
        
            
    def getHandler(self, api: str):
        if api == 'create_room':
            return self.createRoom
        elif api == 'list_open_room':
            return self.listOpenRoom
        elif api == "create_game":
            return self.createGame
        elif api == "enter_room":
            return self.enterRoom
        elif api == "leave_room":
            return self.leaveRoom
        else:
            return None
        
        
nggService = NGGService()   
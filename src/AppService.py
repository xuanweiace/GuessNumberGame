from CODE import pack_err_dict, pack_success_dict
from repository.PlayerPO import PlayerPO
from repository.crud import playerCRUD
from constant import ObjectType, Color, UserStatus
import err
class AppService:
    """要求所有的方法的入参都是dict形式的data
    """
    def __init__(self) -> None:
        
        pass
    
    def getHandler(self, api:str): # 返回一个函数
        if api == 'register':
            return self.register
        elif api == 'login':
            return self.login
        else:
            return None
    # def doHandle(self, data: dict):
    #     self.getHandler(data['api'])
        
            
    def register(self, data: dict):
        """进行一个player的注册
        Args:
            data (dict): 其中key必须包含：username，password,portraitd这几项（其中password暂时不加密）
                            密码功能暂时不启用
        """
        username = data["username"]
        password = data["password"]
        portrait = data["portrait"]
        playerPO = playerCRUD.selectByName(username)
        if playerPO != None:
            return pack_err_dict(err.ER.RECORD_ALREADY_EXIST, "记录已经存在")
        print("ObjectType.NORMAL_PLAYER:", ObjectType.NORMAL_PLAYER)
        print(type(ObjectType.NORMAL_PLAYER))
        new_playerPO = PlayerPO(0,username, ObjectType.NORMAL_PLAYER.value
                                , 0, portrait)
        new_playerId = playerCRUD.insert_without_id(new_playerPO)
        return pack_success_dict({"userid":new_playerId})

    def login(self, data):
        """一个用户的登录

        Args:
            data (dict): 必须包含，username
        Returns:
            可能返回的错误码：RECORD_NOT_EXIST，USER_ALREADY_ONLINE
        """
        username = data["username"]
        playerPO = playerCRUD.selectByName(username)
        if playerPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户不存在")
        status = playerCRUD.selectUserStatus(playerPO.id)
        if status == UserStatus.ONLINE:
            return pack_err_dict(err.ER.USER_ALREADY_ONLINE, "登录失败，用户已online")
        elif status == None:
            playerCRUD.insertUserStatus(playerPO.id, UserStatus.ONLINE)    
        else:
            playerCRUD.updateUserStatus(playerPO.id, UserStatus.ONLINE)
        
        return pack_success_dict({"userid": playerPO.id, "userstatus": UserStatus.ONLINE.name})

    def logout(self, data):
        """用户登出
        Args:
            data (dict): 要求必须要有username字段
        Returns:
            可能返回的错误码：RECORD_NOT_EXIST，USER_ALREADY_OFFLINE
        """
        username = data["username"]
        playerPO = playerCRUD.selectByName(username)
        if playerPO == None:
            return pack_err_dict(err.ER.RECORD_NOT_EXIST, "用户不存在")
        status = playerCRUD.selectUserStatus(playerPO.id)
        if status == UserStatus.OFFLINE:
            return pack_err_dict(err.ER.USER_ALREADY_OFFLINE, "注销失败，用户已offline")
        elif status == None:
            pass
        else:
            playerCRUD.updateUserStatus(playerPO.id, UserStatus.OFFLINE)
        
        return pack_success_dict({"userid": playerPO.id, "userstatus": UserStatus.OFFLINE.name})
        

appService = AppService()
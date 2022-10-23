
class AppService:
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
        
            
    def register(self, data):
        pass

    def login(self, data):
        pass

appService = AppService()
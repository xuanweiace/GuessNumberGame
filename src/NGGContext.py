

ngg_session = dict()

client_session_map = dict()

# 目前仅支持一个ip向服务端建立一个连接
# 暂时不支持 在客户端上切换用户，除非你关闭重开
class ClientContext:
    def __init__(self, address, userId):
        self.address = address
        self.userId = userId


class NGGContext:
    
    def __init__(self):
        self.client_address = [] # NGGContext改变后，向列表内的所有client发信号
        
        self.room = None
            
    
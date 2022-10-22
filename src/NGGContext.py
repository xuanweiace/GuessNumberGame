

ngg_session = dict()

# 目前仅支持一个ip向服务端建立一个连接
class NGGContext:
    
    def __init__(self):
        self.client_address = [] # NGGContext改变后，向列表内的所有client发信号
        
        self.room = None
            
    
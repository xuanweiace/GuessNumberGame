from AppService import appService
from BaseObject import *
client_ngg_map = dict() # 一或多个session对应一个ngg

client_session_map = dict() # 一个client对应一个session

# 目前仅支持一个ip向服务端建立一个连接
# 暂时不支持 在客户端上切换用户，除非你关闭重开
class ClientContext:
    def __init__(self, address, ws_connection, username):
        self.address = address
        self.conn = ws_connection
        self.username = username


class NGGContext:
    
    def __init__(self, cli_host, cli_port):
        self.client_address = [(cli_host, cli_port)] # NGGContext改变后，向列表内的所有client发信号
        
        self.room = None
        
    def add_client(self, cli_host, cli_port):
        self.client_address.append((cli_host, cli_port))
        
    def remove_client(self, cli_host, cli_port):
        # 客户端不在context里
        if (cli_host, cli_port) not in self.client_address:
            return False
        self.client_address.remove((cli_host, cli_port))
        # 如果已经没有客户端连接了，则可以释放这个ngg_context对象
        if len(self.client_address) == 0:
            del self
            
    def set_room(self, room:Room):
        self.room = room
        
        
        
def find_context_by_roomId(roomId: int):
    for ngg in client_ngg_map:
        if roomId == ngg.room.id:
            return ngg
    return None

def can_welcome_client(cli_host, cli_port)->bool:
    if cli_host in client_session_map:
        return False
    return True
    
# 只会在这里new ClientContext
def new_client_welcome(conn, cli_host, cli_port):
    client_session_map[cli_host] = ClientContext((cli_host, cli_port), conn, None)
    

def client_login(cli_host):
    if client_session_map[cli_host].username == None:
        return False
    return True

# todo 这里要抛出异常还是直接返回None
def get_client_username(cli_host):
    if client_login(cli_host) == False:
        return None
    return client_session_map[cli_host].username

def deal_client_leave(cli_host, cli_port):
    # 先检查是否已经登出
    if cli_host not in client_session_map:
        return
    
    
    # 接下来进行客户端清理逻辑
    
    # 先判断是否登录，如是，则登出。
    if client_login(cli_host):
        appService.logout({"username":get_client_username(cli_host)})
    
    # 销毁对应session
    cli_session = client_session_map.pop(cli_host)
    addr = cli_session.address
    
    # 将client移除对应ngg
    ngg :NGGContext = client_ngg_map[cli_host]
    
    ngg.remove_client(addr[0], addr[1])
    
    
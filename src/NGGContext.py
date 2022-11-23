from AppService import appService
from BaseObject import *
import json
from websockets.legacy.protocol import WebSocketCommonProtocol
"""
   ngg的上下文信息 维护在内存里而不是落库 
"""


import atexit

def clear_client_hook():
    for k,v in client_session_map:
        print(f"正在清理客户端:{v.address}")
        deal_client_leave(v.address[0], v.address[1])
print("注册清理客户端的hook")        
atexit.register(clear_client_hook)


# 目前仅支持一个ip向服务端建立一个连接
# 暂时不支持 在客户端上切换用户，除非你关闭重开

client_session_map = dict() # 一个client对应一个session  {"host":ClientContext()}的格式
class ClientContext:
    def __init__(self, address, ws_connection, username):
        self.address = address
        self.conn = ws_connection
        self.username = username

def find_conn_by_username(username: str):
    for k in client_session_map:
        if client_session_map[k].username == username:
            return client_session_map[k].conn

    return None
client_ngg_map = dict() # 一或多个session对应一个ngg
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
    client_ngg_map[cli_host] = NGGContext(cli_host, cli_port)
    

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
    
    print(f"对{cli_host}进行清理")
    # 接下来进行客户端清理逻辑
    
    # todo  看用户是否在房间内，如果是则退出。
    
    # 判断是否登录，如是，则登出。
    if client_login(cli_host):
        print(f"登出{cli_host}")
        appService.logout({"username":get_client_username(cli_host)})
    
    # 销毁对应session
    cli_session = client_session_map.pop(cli_host)
    addr = cli_session.address
    
    # 将client移除对应ngg
    ngg :NGGContext = client_ngg_map[cli_host]
    
    ngg.remove_client(addr[0], addr[1])
    
    
async def push_to_user(username: str, data: dict):
    conn:WebSocketCommonProtocol = find_conn_by_username(username)
    if conn:
        send_msg = json.dumps(data)
        # 主动send但是不需要等待recv
        await conn.send(send_msg)
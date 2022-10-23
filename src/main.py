import asyncio
import add_path
import json
import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
from loguru import logger
from NGGContext import ngg_session, NGGContext
from NGGService import nggService
from AppService import appService

# 该函数维护了一个websocket长连接

async def route_ngg(conn: WebSocketCommonProtocol):
    pass


async def route_http(conn: WebSocketCommonProtocol):
    try:
        async for message in conn:
            data_d = json.loads(message)
            
            handler = appService.getHandler(data_d['api'])
            res = {'api':data_d['api'], 'code': 40002, "msg": "服务端没有该请求的处理函数", "data": None}
            print("res:", res)
            print("json.dumps(res)",json.dumps(res))
            if handler != None:
                res = handler(data_d)
            
            return res
        
    except Exception as e:
        logger.error(f"[main.route_http] remote_address{conn.remote_address} err={e}")
    finally:
        #todo
        pass
                

async def echo(conn: WebSocketCommonProtocol, path):
    if path == '/ngg': # 需要维护状态
        route_ngg(conn)
    elif path == '/http': # 无状态协议
        route_http(conn)
    else:
        
        
    logger.debug("conn:{}".format(conn))
    logger.debug("path:{}".format(path))
    print("remote_address:", conn.remote_address)
    print("path:", path)
    # 如果已有ip再次过来，就拒绝连接。
    cli_host, cli_port = conn.remote_address
    if cli_host in ngg_session:
        await conn.send(f"{'code':40001,msg:'该ip已被占用{cli_host}'}")
        return
    ngg_session[cli_host] = NGGContext()
    
    try: 
        async for message in conn:
            logger.info("got a message:{}".format(message))
            if path == '/create_room':
                print(f"进来了，path={path}")
                newRoomId = nggService.createRoom(103)
                await conn.send("create room success")
                
    except Exception as e:
        logger.error(f"[main.route_ngg] remote_address{conn.remote_address} err={e}")
    finally:
    # 释放连接
        ngg_session.pop(cli_host)

async def main():
    # start a websocket server
    async with websockets.serve(echo, "0.0.0.0", 8765):
        logger.info("GuessNumberGame Server Start Successfully.")
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    logger.add("../log/runtime_{time}.log", retention="5 days")
    
    asyncio.run(main())
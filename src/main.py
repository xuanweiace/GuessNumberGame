import asyncio
import add_path
import json
import websockets
import traceback
from websockets.legacy.protocol import WebSocketCommonProtocol
from loguru import logger
from NGGContext import can_welcome_client, new_client_welcome, deal_client_leave
from NGGService import nggService
from AppService import appService
from CODE import pack_err_dict
import err

"""
注意route_ngg和route_http的异常捕获逻辑不能抽取到一起，
因为异常处理逻辑不一样，route_ngg是有状态的，需要释放连接
"""

# 该函数维护了一个websocket长连接

async def route_ngg(conn: WebSocketCommonProtocol):
    logger.debug("conn.remote_address:{}".format(conn.remote_address))
    # 如果已有ip再次过来，就拒绝连接。
    cli_host, cli_port = conn.remote_address
    if can_welcome_client(cli_host, cli_port) == False:
        await conn.send(f"{{'code':{err.ER.CLIENT_ALREADY_CONNECTED},'msg':'该ip已被占用,ip={cli_host}'}}")
        return
    
    try: 
        new_client_welcome(conn, cli_host, cli_port)
        async for message in conn:
            logger.info("got a message:{}".format(message))
            data_d = json.loads(message)
            handler = nggService.getHandler(data_d['api'])
            if handler != None:
                res = handler(data_d["data"])
            else:
                res = pack_err_dict(err.ER.NO_REQUEST_HANDLER, "服务端没有该api请求的处理函数")
            send_msg = json.dumps(res)
            await conn.send(send_msg)                
    except Exception as e:
        erro = traceback.format_exc()
        logger.error(f"[main.route_ngg] remote_address{conn.remote_address} errpr={erro}")
    finally:
        # 释放连接， 但是不需要关闭conn（退出上面for的时候就退出了）
        deal_client_leave(cli_host, cli_port)


# 只进行一次通信的短连接，类似http，无状态
async def route_http(conn: WebSocketCommonProtocol):
    try:
        async for message in conn:
            data_d = json.loads(message)
            logger.info(f"[main.route_http] request:{data_d}")
            handler = appService.getHandler(data_d['api'])
            res = pack_err_dict(err.ER.NO_REQUEST_HANDLER, "服务端没有该api请求的处理函数")
            if handler != None:
                res = handler(data_d["data"])
            else:
                res = pack_err_dict(err.ER.NO_REQUEST_HANDLER, "服务端没有该api请求的处理函数")
            send_msg = json.dumps(res)
            await conn.send(send_msg)
            return
        
    except Exception as e:
        send_msg = json.dumps(pack_err_dict(err.ER.SERVER_ERROR, str(e)))
        await conn.send(send_msg)
        erro = traceback.format_exc()
        logger.error(f"[main.route_http] remote_address{conn.remote_address} error={erro}")
    finally:
        #todo
        pass
                

async def echo(conn: WebSocketCommonProtocol, path):    
    if path == '/ngg': # 需要维护状态
        await route_ngg(conn)
    elif path == '/http': # 无状态协议
        await route_http(conn)
    else:
        logger.warning(f"[main.echo] ws路径不支持: path={path}")
        await conn.send("error")
        await conn.close()
        
        


async def main():
    # start a websocket server
    async with websockets.serve(echo, "0.0.0.0", 8765):
        logger.info("GuessNumberGame Server Start Successfully.")
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    logger.add("../log/runtime_{time}.log", retention="5 days")
    
    asyncio.run(main())
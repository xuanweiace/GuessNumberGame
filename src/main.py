import asyncio
import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
from loguru import logger
from NGGContext import ngg_session
from NGGService import nggService

# 该函数维护了一个websocket长连接
async def echo(conn: WebSocketCommonProtocol, path):
    
    logger.debug("conn:{}".format(conn))
    logger.debug("path:{}".format(path))
    print("remote_address:", conn.remote_address)
    print("local_address:", conn.local_address)
    print("host:", conn.host)
    print("port:", conn.port)
    print("path:", path)
    
    # 如果已有ip再次过来，就拒绝连接。
    if conn.remote_address[0] in ngg_session:
        await conn.send(f"{'code':40001,msg:'该ip已被占用{conn.remote_address[0]}'}")
        return
    
    async for message in conn:
        logger.info("got a message:{}".format(message))
        if path == '/create_room':
            nggService.createRoom(200)
            await conn.send("create room success")
        
    # 释放连接
    ngg_session.pop(conn.remote_address[0])

async def main():
    # start a websocket server
    async with websockets.serve(echo, "0.0.0.0", 8765):
        logger.info("GuessNumberGame Server Start Successfully.")
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    logger.add("../log/runtime_{time}.log", retention="5 days")
    
    asyncio.run(main())
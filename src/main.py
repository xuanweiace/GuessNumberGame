import asyncio
import websockets
from websockets.legacy.protocol import WebSocketCommonProtocol
from loguru import logger

async def echo(conn: WebSocketCommonProtocol, path):
    logger.debug("conn:{}".format(conn))
    logger.debug("path:{}".format(path))
    print("remote_address:", conn.remote_address)
    print("local_address:", conn.local_address)
    print("host:", conn.host)
    print("port:", conn.port)
    async for message in conn:
        logger.info("got a message:{}".format(message))
        await conn.send(message)

async def main():
    # start a websocket server
    async with websockets.serve(echo, "0.0.0.0", 8765):
        logger.info("GuessNumberGame Server Start Successfully.")
        await asyncio.Future()  # run forever


if __name__ == '__main__':
    logger.add("../log/runtime_{time}.log", retention="5 days")
    
    asyncio.run(main())
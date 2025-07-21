import json
import socket
import logging
import asyncio
import setuplog
import websockets

from settings import *
from privateSettings import *

class HeyBoxClient:
    def __init__(self) -> None:
        self.log = logging.getLogger("黑盒语音")
        self.log.info(f'正在初始化黑盒语音连接')
        self.log.info(f'正在连接到诺瓦核心')
        self.client = socket.socket()
        self.client.connect(('127.0.0.1', 2353))
        self.client.send(json.dumps({
                                        'name': '黑盒语音',
                                        'isProactive': True 
                                    }).encode())
        recv = self.client.recv(1024).decode()
        self.log.info(f'已连接到诺瓦核心, 服务器返回消息：{recv}')
    
    async def mainloop(self):
        self.log.info(f'正在连接到黑盒语音')
        async with websockets.connect(f'{HEYBOX_BASE_URL}?{HEYBOX_CONN_QUERY}', additional_headers={'token': HEYBOX_TOKEN}) as websocket:
            self.log.info(f'已连接到黑盒语音')
            self.log.info(f'初始化完成，开始运行')
            try:
                while True:
                    message = await websocket.recv()
                    self.log.info(f'收到服务器消息：{message}')
                    message = json.loads(message)['data']
                    
            except websockets.exceptions.ConnectionClosed:
                self.log.error("连接关闭")
                

if __name__ == '__main__':
    c = HeyBoxClient()
    asyncio.run(c.mainloop())
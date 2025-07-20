import json
import socket
import asyncio
import logging
import setuplog
import requests
import websockets

from settings import *
from privateSettings import *

log = logging.getLogger("HeyBox")
client = socket.socket()

client.connect(('127.0.0.1', 2353))
log.info(f'已连接到诺瓦核心')

async def mainloop():
    async with websockets.connect(f'{HEYBOX_BASE_URL}?{HEYBOX_CONN_QUERY}', additional_headers={'token': HEYBOX_TOKEN}) as websocket:
        log.info(f'已连接到黑盒语音')
        try:
            while True:
                message = await websocket.recv()
                log.info(f'收到服务器消息：{message}')
                message = json.loads(message)['data']
                
                # 生成信息并返回给服务器
                data = {
                    'message': '',
                    'platAccount': {
                        'platName': '黑盒语音',
                        'name': message['nickname'],
                        'id': message['user_id']
                    }
                }
                data = json.dumps(data).encode()
                client.send(data)
                rec = client.recv(1024)
                rec = json.loads(rec.decode())
                
                req = requests.post(f'{HEYBOX_SEND_URL}?{HEYBOX_CONN_QUERY}', headers={
                    "token": "ODQ4NzQ5MTA7MTc1Mjc0MjA0MzUwOTY2OTczNTsxMzI1OTYzMTU1OTM2MTEzMjA4",
                    "Content-Type": "application/json;charset=UTF-8",
                }, json={
                    'msg': '@{id:'+ str(message['user_id']) +'} ' + rec['message'],
                    'msg_type': 10,
                    "heychat_ack_id": "0",
                    "reply_id": "",
                    "room_id": str(message['room_id']),
                    "addition": "{\"img_files_info\":[]}",
                    "at_user_id": str(message['user_id']),
                    "at_role_id": "",
                    "mention_channel_id": "",
                    "channel_id": str(message['channel_id']),
                })
                log.debug(f'发送消息的返回值：{req.text}')


        except websockets.exceptions.ConnectionClosed:
            log.error("连接关闭")
    
asyncio.run(mainloop())

import json
import botpy
import random
import socket
import logging
import setuplog

from settings import *
from botpy.message import GroupMessage
from privateSettings import *

class Noir(botpy.Client):
    def __init__(self, intents, timeout = 5, is_sandbox=False, log_config = None, log_format = None, log_level = None, bot_log = True, ext_handlers = True):
        super().__init__(intents, timeout, is_sandbox, log_config, log_format, log_level, bot_log, ext_handlers)
        self.log = logging.getLogger()  # 日志记录器
        self.seq = 1  # 消息计数
        
        # --- 初始化客户端并和服务器通信发送信息 ---
        self.client = socket.socket()
        self.client.connect(('127.0.0.1', 2353))
        data = {
            'name': 'QQ',
            'isProactive': False
        }
        self.log.info(f'正在向服务器发送数据')
        self.client.send(json.dumps(data).encode())
        recv = self.client.recv(1024).decode()
        self.log.info(f'服务器的回复：{recv}')

    async def send_message(self, data: dict, message: GroupMessage):
        # 发送信息
        self.log.info(f'实际发送的信息：{data['message']}, {'|'.join(data['picture'])}')

        # 图片
        if len(data['picture']) > 0:
            for picpath in data['picture']:
                picpath: str
                if picpath.startswith('http'):  # URL
                    pass
                else:  # 本地文件
                    await message.reply(file_image=picpath)
                    self.api.post_group_file
        
        for line in data['message']:
            await message._api.post_group_message(
                group_openid=message.group_openid, # type: ignore
                msg_id=message.id,
                content=QQ_MESSAGE_PREFIX + line,
                msg_type=0,
                msg_seq=self.seq,
            )
            self.seq += 1

    async def on_group_at_message_create(self, message: GroupMessage): # @ 消息
        # 重置 seq
        self.seq = QQ_SEQ_START
        
        # 去掉消息头尾的空格（**的空格）
        message.content = message.content.strip(' ')
        self.log.debug(f'收到消息 {message.content}')         
        
        # 与服务器通信获取回复
        data = {
            "message": message.content,
            "platAccount": {
                'platName': 'QQ',
                'name': '',
                'id': message.author.member_openid
            },
            "spread": False,
            "mustReply": True
        }
        data = json.dumps(data).encode()
        self.client.send(data)
        rec = self.client.recv(1024)
        try:
            rec = json.loads(rec.decode())
        except json.decoder.JSONDecodeError:
            self.log.error(f'发生编码错误，收到的内容：{rec}')
            self.log.exception(rec)
        
        await self.send_message(rec, message)

# 移除 QQBot 自带的 handler
for handle in logging.root.handlers:
    if '\x1b' in handle.formatter._fmt: # type: ignore
        logging.root.removeHandler(handle)

intents = botpy.Intents()
intents.public_messages = True
intents.direct_message = True

client = Noir(intents=intents)
client.run(appid=QQ_APPID, secret=QQ_APPSECRET) 
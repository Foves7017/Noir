import re
import json
import socket
import logging
import setuplog
import threading

from tools import ToolRunner
from openai import OpenAI
from command import process_command
from settings import *
from jsonDataBase import DataBase
from privateSettings import *

class Noir:
    def __init__(self):
        """ 诺瓦的核心组件
        """
        self.history = [{'role': 'system', 'content': NOIR_PROCESS_PROMPT}]
        self.log = logging.getLogger("Noir IV")
        self.log.info('Noir IV 开始初始化。。。')
        
        self.server = socket.socket()
        self.server.bind(('127.0.0.1', NOIR_PORT))
        self.server.listen(5)
        
        self.clients = {}
        
        self.log.info(f'Noir IV 服务正在端口 {NOIR_PORT} 上运行')
    
    def mainloop(self):
        while True:
            client, addr = self.server.accept()
            self.log.info(f'来自 {addr} 的连接')
            clientData: dict = json.loads(client.recv(1024).decode())
            self.clients[clientData['name']] = Serve(client, self, clientData['name'], clientData['isProactive'])
            client.send(b'200')

class Serve:
    def __init__(self, 
                 client: socket.socket, 
                 noir: Noir,
                 clientName: str,
                 isProactive: bool, 
                 ):
        """ 用于响应建立客户端
        
        Args:
            client (socket.socket): 相应的客户端
            clientName (str): 服务端的名称
            isProactive (bool): 是否可以主动发送消息
        """
        
        self.log = logging.getLogger('Client: ' + clientName)
        self.log.info(f'正在初始化线程')
        self.noir = noir
        self.client = client
        self.clientName = clientName
        self.isProactive = isProactive
        self.toolRunner = ToolRunner()
        self.openai_client = OpenAI(api_key=NOIR_DS_API_KEY, base_url=NOIR_DS_BASE_URL)
        
        self.thread = threading.Thread(target=self.main_thread)
        self.thread.start()
    
    def main_thread(self):
        self.log.info(f'线程进入循环')
        while True:
            try:
                # 接受消息并解析
                message = self.client.recv(1024)
                message = json.loads(message.decode())
                message = self.process(message)
                message = json.dumps(message).encode()
                self.client.send(message)
            except Exception as e:
                self.log.exception(f'发生异常 {e}, 已退出线程')
                break
    
    def translate(self, old_message: str) -> str:
        self.log.info('正在进行翻译')
        res = self.openai_client.chat.completions.create(
            messages=[{'role': 'system', 'content': NOIR_WORDOUT_PROMPT},{'role': 'user', 'content': old_message}],
            model=NOIR_DS_CHAT_MODEL
        )
        self.log.info(f'翻译结果：{str(res.choices[0].message.content)}')
        return str(res.choices[0].message.content)
    
    def process(self, message: dict) -> dict:
        self.log.debug(f'消息原文：{message}')
        self.log.info(f'收到消息：{message['message']}')
        # --- 拆分解析用户信息 ---
        # 分离消息正文
        content_soure: str = message['message'] 
        # 查询用户信息
        with DataBase() as data:
            userdata: dict = data.query_by_platID(message['platAccount']['platName'], message['platAccount']['id'])
            if not userdata:
                self.log.warning('正在创建新用户')
                userdata = data.add_new_user(message['platAccount'])
        self.log.debug(f'查询到的用户信息：{userdata}')
        
        # --- 判断信息结构并处理 ---
        if content_soure.startswith('%'):
            self.log.info(f'开始处理命令：{message['message']}')
            # 处理命令
            content_processed: str = process_command(message['message'], userdata['unid'], message['platAccount']['platName'])
            self.log.info(f'命令处理结果：{content_processed}')
        else:
            # 处理自然对话
            picture = []  # 图片列表
            prompt = f'''<UserInfo>
                <name>{userdata["accounts"][message['platAccount']['platName']]['name']}</name>
                <unid>{userdata["unid"]}</unid>
                <plat>{message["platAccount"]['platName']}</plat>
                <history>{userdata['history']}</history>
                <allplat>{str(userdata['accounts'].keys())}</allplat>
            </UserInfo>
            <Message>
                <content>{message["message"]}</content>
            </Message>
            '''.replace('        ', '')
            self.log.info(f'使用的提示词：\n{content_soure}')
            self.noir.history.append({'role': 'user', 'content': prompt, 'name': userdata['unid']})
            
            # 附加了工具调用后的调用
            finish_reason = ''
            back = ''
            while not finish_reason == 'stop':
                res = self.openai_client.chat.completions.create(
                    messages=self.noir.history, # type: ignore
                    model=NOIR_DS_CHAT_MODEL,
                    tools=self.toolRunner.toollist,  # type: ignore
                )
                content_model = res.choices[0].message 
                finish_reason = res.choices[0].finish_reason
                toolcalls = content_model.tool_calls 
                back += content_model.content  # type: ignore
                self.noir.history.append(content_model)  # type: ignore

                if finish_reason == 'tool_calls':
                    for toolcall in toolcalls: # type: ignore 
                        self.log.info(f'正在调用工具 {toolcall.function.name}, 参数为：{toolcall.function.arguments}')
                        toolback = self.toolRunner.run_tool(toolcall.function.name, toolcall.function.arguments)
                        self.log.info(f'工具输出：{toolback}')
                        if '<image>' in toolback:
                            imageFind: list[str] = re.findall('<image>.*?</image>', toolback)
                            for img in imageFind:
                                img.replace('<image>', '').replace('</image>', '')
                                self.log.info(f'检测到图片：{img}')
                                picture.append(img)
                        self.noir.history.append({'role': 'tool', 'content': toolback, 'tool_call_id': toolcall.id})
            
            content_processed = back
            self.log.info(f'主模型输出：\n{content_processed}')
        
        # --- 翻译 ---
        if not '<NoTranslate>' in content_processed:
            notrans = []
            if '<Output>' in content_processed:
                notrans = re.findall('<Output>.*?</Output>', content_processed)
                for notran in notrans:
                    content_processed = content_processed.replace(notran, '')
            content_translated = self.translate(content_processed)
            for i in notrans:
                content_translated += i.replace('<Output>', '').replace('</Output>', '')
        else:
            content_translated = content_processed.replace('<NoTranslate>', '')
        self.log.info(f'消息中包含的图片：{picture}')
        return {'message': content_translated, 'picture': picture}

if __name__ == '__main__':
    noir: Noir = Noir()
    noir.mainloop()
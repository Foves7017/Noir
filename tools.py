import os
import time
import json
import imgkit
import datetime
import markdown2

class ToolRunner:
    def __init__(self) -> None:
        os.makedirs('image', exist_ok=True)
        self.toollist = [
            {
                "type": "function",
                "function": {
                    "name": "get_time",
                    "description": "获取当前时间",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "markdown_render",
                    "description": "渲染markdown，当你需要在回答中提供数学公式或代码时，使用markdown格式并调用这个工具",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "要渲染的markdown字符串",
                            },
                        },
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "charactor_query",
                    "description": "根据人物的名字查询人物的信息，可以查询游戏、动漫角色或现实中存在的人物。",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "要查询人物的名字",
                            },
                        },
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "dict_query",
                    "description": "查询某个物品或概念的解释，当未找到时，你可以判断应该询问用户还是依靠自己的知识解释",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "要查询的物品或概念",
                            },
                        },
                    }
                }
            },
        ]
    
    def dict_query(self, name: str) -> str:
        """ 查询物品或概念

        Args:
            name (str): 要查询的物品
        """
        # 特殊的
        spec = {
            '面包人': '由面包构成的人，可以吃。有自己的意识。它们认为面包人的使命就是被吃掉，而面包人的最高荣耀是吃掉之后被说好吃。只要面包人的头部还在，那组成身体的面包就会逐渐复原。它们为世界提供了几乎无限的面包。同时，如果人类吃掉猫娘，那么那个人类就会变成面包人。',
            '猫娘': '生长着猫耳和猫尾的人类。行为举止有猫咪的风范，动作等也有猫咪的特征，甚至可以像猫咪一样从三层楼跳下来而不受伤。人类如果吃掉猫娘，那么那个人就会变成面包人。'
        }
        if name in spec:
            return spec[name]
        return f'没有找到 {name} 的信息'
    
    def charactor_query(self, name: str) -> str:
        # 查询人物
        # 特殊的人物：诺瓦（自己）
        if name == '诺瓦':
            return '诺瓦是你自己，是一个猫娘。有红色的眼睛和白色的长发与耳朵。'
        return f'没有找到人物 {name} 的信息'
 
    def run_tool(self, toolname: str, args: str) -> str:
        kwargs = json.loads(args)
        ret = self.__getattribute__(toolname)(**kwargs)
        return ret
    
    def markdown_render(self, content: str):
        html_content = markdown2.markdown(content)
        imgkit.from_string(html_content, f'img/markdown_render_temp.png', config=imgkit.config(wkhtmltoimage=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'))
        return '<image>img/markdown_render_temp.png</image>'
    
    def get_time(self):
        """ 时间查看工具的实现
        """
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
     
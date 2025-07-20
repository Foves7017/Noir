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
        ]
    
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
    
     
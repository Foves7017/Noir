import os
import datetime
import logging

from colorama import Fore, init

CONSOLE = True
COLORED = True

init(autoreset=True)  # 带颜色的设置
class ColoredFormatter(logging.Formatter):
    COLOR_MAP = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        msg = super().format(record)
        color = self.COLOR_MAP.get(record.levelno, Fore.WHITE)
        return f"{color}{msg}"


# 确认日志文件夹
os.makedirs('logs', exist_ok=True)
tm = datetime.datetime.now().strftime("%Y_%m_%d")
# 建立格式
formatter = logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s] %(message)s")
# 建立文件句柄
file_handle = logging.FileHandler(
    f'logs/{tm}.log',
    encoding='UTF8',

)
file_handle.setLevel(logging.DEBUG)
file_handle.setFormatter(formatter)
latest_handle = logging.FileHandler(
    f'logs/latest.log',
    mode='w',
    encoding='UTF8'
)
latest_handle.setLevel(logging.DEBUG) 
latest_handle.setFormatter(formatter)

if CONSOLE:
    # 建立终端句柄
    console_handle = logging.StreamHandler()
    console_handle.setLevel(logging.INFO)
    if COLORED:
        console_handle.setFormatter(ColoredFormatter('[%(asctime)s][%(levelname)s][%(name)s] %(message)s'))
    else:
        console_handle.setFormatter(formatter)
        

logger = logging.getLogger()
logger.addHandler(file_handle)
logger.addHandler(latest_handle)
if CONSOLE:
    logger.addHandler(console_handle)
logger.setLevel(logging.DEBUG)

# 列出所有handler
print('当前的所有handler：')
for handle in logging.root.handlers:    
    print(f'{handle = } {handle.formatter._fmt = }')
HEYBOX_BASE_URL: str = "wss://chat.xiaoheihe.cn/chatroom/ws/connect"
HEYBOX_SEND_URL: str = "https://chat.xiaoheihe.cn/chatroom/v2/channel_msg/send"
HEYBOX_CONN_QUERY: str = "client_type=heybox_chat&x_client_type=web&os_type=web&x_os_type=bot&x_app=heybox_chat&chat_os_type=bot&chat_version=1.30.0"

QQ_SEQ_START = 200
QQ_MESSAGE_PREFIX = '[开发版消息] '

JSONDATABASE_FILENAME = 'json/userdata.json'

NOIR_DS_CHAT_MODEL = 'deepseek-chat'
NOIR_PORT: int = 2353
with open('_WORDOUT_PROMPT.md', 'r', encoding='UTF8') as f:
    NOIR_WORDOUT_PROMPT = f.read()
with open('_PROCESS_PROMPT.md', 'r', encoding='UTF8') as f:
    NOIR_PROCESS_PROMPT = f.read()
import os
import json
import random

from settings import *

class DataBase:
    def __enter__(self):
        os.makedirs('json', exist_ok=True)
        try:
            with open(JSONDATABASE_FILENAME, 'r', encoding='UTF8') as f:
                self.file = json.load(f)
        except FileNotFoundError:
            self.file = {}
            
        return self

    def create_unid(self) -> str:
        while True:
            nunid = ''
            for _ in range(8):
                nunid += chr(random.randint(48, 90))
            if not nunid in self.file:
                return nunid
    
    def query_by_unid(self, unID: str) -> dict:
        try:
            return self.file[unID]
        except KeyError:
            raise KeyError(f'unID错误：没有 unID 为 {unID} 的用户')
    
    def query_by_platID(self, platName: str, platID: str) -> dict:
        """ 通过平台账号查找用户，通过平台的ID查询，未找到会返回空字典

        Args:
            platName (str): 平台名称
            platID (str): 平台 ID

        Returns:
            dict: 查找到的用户信息
        """
        for unid in self.file:
            if platName in self.file[unid]['accounts']:
                if self.file[unid]['accounts'][platName]['id'] == platID:
                    return self.query_by_unid(unid)
        return {}

    def modify_info(self, unid: str, platName: str, key: str, value: str) -> dict:
        """ 修改某一项的值

        Args:
            unid (str): 用户unid
            platname (str): 目标平台名
            key (str): 要修改的项目
            value (str): 新的值

        Returns:
            dict: 返回修改后的用户信息
        """
        self.file[unid]['accounts'][platName][key] = value
        return self.query_by_unid(unid)

    def add_new_user(self, account: dict) -> dict:
        """ 创建新用户，会返回新建的用户信息

        Args:
            account (dict): 用户信息，需要符合文档中的说明，（传入列表项）

        Returns:
            dict: 新建的用户信息
        """
        newunid = self.create_unid()
        self.file[newunid] = {
            'unid': newunid,
            'history': '无',
            'accounts': {
                account['platName']: account
            }
        }
        return self.query_by_unid(newunid)

    def append_history(self, unid: str, content: str) -> dict:
        """ 向某个用户的历史记录中添加新行

        Args:
            unid (str): unid
            content (str): 要添加的新行

        Returns:
            dict: 添加后的用户信息
        """
        if self.file[unid]['history'] == '无':
            self.file[unid]['history'] = content
        else:
            self.file[unid]['history'] += '\n' + content
        return self.query_by_unid(unid)
    
    def __exit__(self, *args):
        with open(JSONDATABASE_FILENAME, 'w', encoding='UTF8') as f:
            json.dump(self.file ,f)
            
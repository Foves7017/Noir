from jsonDataBase import DataBase

def process_command(command: str, unid: str, platName: str) -> str:
    command_list: list[str] = command.lstrip('%').split(' ')
    if command_list[0] == 'setname':
        if platName == 'QQ':
            try:
                newName = command_list[1]
                with DataBase() as data:
                    result = data.modify_info(unid, 'QQ', 'name', newName)
                if not result == 'OK':
                    return f'<Info>发生错误：{result}</Info>'
                return f'<Chat>修改成功</Chat>'
            except IndexError:  
                return f'<Info>命令格式为%setname [NewName]</Info><Chat>告诉用户命令格式错误</Chat>'
    elif command_list[0] == 'gethistory':
        with DataBase() as data:
            result = data.query_by_unid(unid)
            return f'<NoTranslate>历史：\n{result['history']}'
    elif command_list[0] == 'clear':
        return f'<Clear>'
    return f'<Chat>告诉用户输入了未知的命令</Chat>'
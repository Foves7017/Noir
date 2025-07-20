使用 JSON 格式存储用户信息的接口

# 存储的数据结构
```JSON
{
	"unid": {	
		"unid": "unID, 和上面那个键一样.",
		"history": "回忆历史",
		"accounts":{
			"平台名称": {
				"platName": "平台名称",
				"name": "在那个平台的昵称",
				"id": "在那个平台的账号或识别码"
			},
			...
		}
	}
}
```
# 方法
#### `__enter__(self)` 和 `__exit__(self)`
在进出上下文时自动加载/保存文件
#### `create_unid(self) -> str`
 - `return`： 生成的 `unid`
生成一个新的`unid`，`unid`是由 8 个 ASCII 在 $[48,90]$ 内的字符组成的字符串。
#### `query_by_unid(self, unID: str) -> dict`
 - `unID`：目标用户的 `unID`
 根据 `unid` 查询用户数据，会返回查询到的用户数据（见上）
#### `query_by_platID(self, platName: str, platID: str) -> dict`
 - `unID`：目标用户的 `unID`
 - `platname`：平台名，[[命名规范#平台名称|目前支持的平台]]
 - `platinfo`：要添加的信息，需要符合上面的格式
向一个用户的信息添加平台，如果平台名已经存在覆盖。返回新的用户信息
#### `modify_info(self, unid: str, platName: str, key: str, value: str) -> dict`
 - `unid`：用户`unid`
 - `platName`：对应平台名
 - `key`：要修改的键
 - `value`：新的值
返回修改后的用户信息。
#### `add_new_user(self, account: dict) -> dict`
 - `account`：初始平台，格式见下
传入的格式（实际上就是接收到消息的 `platAccount` 字段：
```JSON
{
	"platName": "平台名称",
	"name": "在那个平台的昵称",
	"id": "在那个平台的账号或识别码"
}
```
返回新建的用户信息
#### `append_history(self, unid: str, content: str) -> dict`
 - `unid`：目标用户的 id
 - `content`：要添加的新行
 向某个用户的历史记录中添加新行。返回新的用户信息。
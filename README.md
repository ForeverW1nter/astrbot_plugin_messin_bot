# Messin Bot - AstrBot 插件

Messin Bot 是一个功能丰富的 AstrBot 插件，提供了完整的机器人功能，包括基础命令、AI对话、经济系统、管理功能、娱乐功能和工具功能。

## 功能特性

### 基础命令
- `mes help`：显示帮助信息
- `mes repeat <内容>`：重复你说的话
- `mes status`：查看机器人状态
- `mes cal <表达式>`：计算数学表达式
- `mes fool`：随机讲一个笑话

### AI对话
- `mes ai <内容>`：智能对话，使用 DeepSeek API

### 经济系统
- `mes create_account`：创建经济账号
- `mes sign_in`：每日签到
- `mes balance`：查看余额
- `mes lottery`：抽奖
- `mes transfer <金额> <目标用户ID>`：转账
- `mes leaderboard`：查看排行榜
- `mes shop`：查看商店
- `mes transactions`：查看交易记录

### 管理功能
- `mes add_whitelist <群ID>`：添加白名单
- `mes remove_whitelist <群ID>`：移除白名单
- `mes add_admin <用户ID>`：添加管理员
- `mes remove_admin <用户ID>`：移除管理员
- `mes view_whitelist`：查看白名单
- `mes view_admins`：查看管理员

### 娱乐功能
- `mes loli`：获取随机图片
- `mes reaction`：随机反应

### 工具功能
- `mes bilibili <链接>`：解析Bilibili链接

## 全局功能

### 全局黑白名单
- 可以配置是否可以调用 AI 接口（被禁用 AI 接口的群聊或个人其他功能还是正常使用的，只是不能使用 AI）
- 可以配置是否禁用所有功能

### 过长消息处理
- 单消息 3 图片以上或 100 字符以上或 10 行以上的消息会被识别为过长消息
- 过长消息会自动放入聊天记录再发送

## 安装方法

1. **通过插件市场安装**：
   - 打开 AstrBot 管理面板
   - 进入插件市场
   - 搜索 "Messin Bot"
   - 点击安装按钮

2. **手动安装**：
   - 下载插件压缩包
   - 解压到 `~/.astrbot/data/plugins/` 目录
   - 重启 AstrBot

## 配置方法

1. 打开 AstrBot 管理面板
2. 进入插件管理
3. 找到 "Messin Bot" 插件
4. 点击 "配置" 按钮
5. 根据需要修改配置项

### 主要配置项

- **API配置**：
  - DeepSeek API 密钥
  - Lolicon API 密钥

- **经济系统配置**：
  - 新用户初始金币
  - 每日签到基础奖励
  - 连续签到额外奖励
  - 抽奖花费
  - 抽奖奖励配置

- **商店配置**：
  - 商店物品列表

- **管理系统配置**：
  - 初始管理员列表
  - 初始白名单群列表

- **娱乐系统配置**：
  - 图片功能启用状态
  - 反应功能启用状态
  - 反应表情列表

- **工具系统配置**：
  - Bilibili 解析功能启用状态

- **消息配置**：
  - 命令前缀
  - 帮助消息

- **全局配置**：
  - 白名单模式（白名单或黑名单）
  - AI 接口白名单/黑名单
  - 所有功能白名单/黑名单
  - 过长消息处理启用状态
  - 最大图片数量
  - 最大字符数
  - 最大行数

## 依赖项

- `aiohttp`：用于异步网络请求

## 开发指南

### 项目结构

```
astrbot_plugin_messin_bot/
├── commands/          # 命令处理模块
│   ├── __init__.py
│   ├── base.py        # 基础命令
│   ├── ai.py          # AI命令
│   ├── economy.py     # 经济系统命令
│   ├── admin.py       # 管理命令
│   ├── entertainment.py # 娱乐命令
│   └── tool.py        # 工具命令
├── utils/             # 工具类和数据管理
│   ├── __init__.py
│   ├── data_manager.py # 数据管理器
│   ├── tools.py       # 工具函数
│   └── global_manager.py # 全局管理器
├── api/               # API调用相关
│   ├── __init__.py
│   └── api_client.py  # API客户端
├── data/              # 数据文件
├── __init__.py        # 包文件
├── main.py            # 主文件
├── metadata.yaml      # 元数据
├── requirements.txt   # 依赖项
├── _conf_schema.json  # 配置模式
├── logo.png           # 插件logo
└── README.md          # 说明文档
```

### 开发流程

1. 克隆仓库
2. 安装依赖：`pip install -r requirements.txt`
3. 修改代码
4. 测试插件
5. 提交代码

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT

## 联系方式

- 作者：Forewall
- GitHub：https://github.com/ForeverW1nter/astrbot_plugin_messin_bot

import os
from collections.abc import AsyncGenerator
from astrbot.api.star import Star, Context, register
from astrbot.api.event import AstrMessageEvent
from astrbot.api.event.filter import command
from astrbot.api import logger

from .utils.data_manager import DataManager
from .commands import BaseCommands, AICommands, EconomyCommands, AdminCommands, EntertainmentCommands, ToolCommands

@register("astrbot_plugin_messin_bot", "Forewall", "提供完整的机器人功能，包括基础命令、AI对话、经济系统、管理功能、娱乐功能和工具功能", "1.0.0", "https://github.com/ForeverW1nter/astrbot_plugin_messin_bot")
class MessinBotPlugin(Star):
    """MessinBot插件 - 提供完整的机器人功能"""

    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)
        self.config = config or {}
        
        # 初始化数据管理器
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_manager = DataManager(plugin_dir)
        
        # 初始化API密钥
        self.deepseek_api_key = self.config.get("deepseek_api_key", "")
        self.lolicon_api_key = self.config.get("lolicon_api_key", "")
        
        # 初始化命令处理器
        self.base_commands = BaseCommands()
        self.ai_commands = AICommands(self.deepseek_api_key)
        self.economy_commands = EconomyCommands(self.data_manager)
        self.admin_commands = AdminCommands(self.data_manager)
        self.entertainment_commands = EntertainmentCommands(self.lolicon_api_key)
        self.tool_commands = ToolCommands()
        
        # 初始化存储
        self._init_data()
        
        logger.info("MessinBot插件初始化完成")

    def _init_data(self):
        """初始化数据"""
        # 初始化经济系统数据
        economy_data = self.data_manager.get_economy_data()
        if not economy_data["users"]:
            self.data_manager.save_economy_data({
                "users": {},
                "shop": [
                    {"id": 1, "name": "幸运符", "price": 100, "description": "增加抽奖中奖概率"},
                    {"id": 2, "name": "经验丹", "price": 200, "description": "增加经验值"},
                    {"id": 3, "name": "金币袋", "price": 500, "description": "获得1000金币"}
                ]
            })
        
        # 初始化管理系统数据
        admin_data = self.data_manager.get_admin_data()
        if not admin_data["admins"]:
            self.data_manager.save_admin_data({
                "admins": [],
                "whitelist_groups": []
            })

    # 主命令处理
    @command("mes", help="显示帮助信息")
    async def handle_mes(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理mes命令"""
        raw_msg: str = event.message_str.strip()
        
        # 去掉开头的指令名，提取子命令和参数
        parts = raw_msg.split(None, 1)
        if len(parts) < 2:
            yield event.plain_result("请输入命令，例如：mes help")
            return
        
        sub_command = parts[1].split(None, 1)[0] if len(parts[1].split(None, 1)) > 0 else ""
        params = parts[1].split(None, 1)[1].strip() if len(parts[1].split(None, 1)) > 1 else ""
        
        # 处理不同的子命令
        # 基础命令
        if sub_command == "help":
            async for msg in self.base_commands.handle_help(event):
                yield msg
        elif sub_command == "repeat":
            async for msg in self.base_commands.handle_repeat(event, params):
                yield msg
        elif sub_command == "status":
            async for msg in self.base_commands.handle_status(event):
                yield msg
        elif sub_command == "cal":
            async for msg in self.base_commands.handle_cal(event, params):
                yield msg
        elif sub_command == "fool":
            async for msg in self.base_commands.handle_fool(event):
                yield msg
        # AI命令
        elif sub_command == "ai":
            async for msg in self.ai_commands.handle_ai(event, params):
                yield msg
        # 经济系统命令
        elif sub_command == "create_account":
            async for msg in self.economy_commands.handle_create_account(event):
                yield msg
        elif sub_command == "sign_in":
            async for msg in self.economy_commands.handle_sign_in(event):
                yield msg
        elif sub_command == "lottery":
            async for msg in self.economy_commands.handle_lottery(event):
                yield msg
        elif sub_command == "balance":
            async for msg in self.economy_commands.handle_balance(event):
                yield msg
        elif sub_command == "transfer":
            async for msg in self.economy_commands.handle_transfer(event, params):
                yield msg
        elif sub_command == "leaderboard":
            async for msg in self.economy_commands.handle_leaderboard(event):
                yield msg
        elif sub_command == "shop":
            async for msg in self.economy_commands.handle_shop(event):
                yield msg
        elif sub_command == "transactions":
            async for msg in self.economy_commands.handle_transactions(event):
                yield msg
        # 管理命令
        elif sub_command == "add_whitelist":
            async for msg in self.admin_commands.handle_add_whitelist(event, params):
                yield msg
        elif sub_command == "remove_whitelist":
            async for msg in self.admin_commands.handle_remove_whitelist(event, params):
                yield msg
        elif sub_command == "add_admin":
            async for msg in self.admin_commands.handle_add_admin(event, params):
                yield msg
        elif sub_command == "remove_admin":
            async for msg in self.admin_commands.handle_remove_admin(event, params):
                yield msg
        elif sub_command == "view_whitelist":
            async for msg in self.admin_commands.handle_view_whitelist(event):
                yield msg
        elif sub_command == "view_admins":
            async for msg in self.admin_commands.handle_view_admins(event):
                yield msg
        # 娱乐命令
        elif sub_command == "loli":
            async for msg in self.entertainment_commands.handle_loli(event):
                yield msg
        elif sub_command == "reaction":
            async for msg in self.entertainment_commands.handle_reaction(event):
                yield msg
        # 工具命令
        elif sub_command == "bilibili":
            async for msg in self.tool_commands.handle_bilibili_parse(event, params):
                yield msg
        else:
            yield event.plain_result(f"未知命令：{sub_command}，请使用 mes help 查看可用命令")

    async def terminate(self):
        """插件卸载时调用"""
        logger.info("MessinBot插件正在卸载")
        # 这里可以添加清理资源的代码
        logger.info("MessinBot插件卸载完成")

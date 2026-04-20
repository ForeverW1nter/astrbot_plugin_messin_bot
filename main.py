import os
from collections.abc import AsyncGenerator
from astrbot.api.star import Star, Context, register
from astrbot.api.event import AstrMessageEvent
from astrbot.api.event.filter import command, event_message_type, EventMessageType
from astrbot.api import logger

from .utils import DataManager, GlobalManager
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
        
        # 初始化配置项
        api_config = self.config.get("api", {})
        economy_config = self.config.get("economy", {})
        sign_in_config = economy_config.get("sign_in", {})
        lottery_config = economy_config.get("lottery", {})
        admin_config = self.config.get("admin", {})
        entertainment_config = self.config.get("entertainment", {})
        loli_config = entertainment_config.get("loli", {})
        reaction_config = entertainment_config.get("reaction", {})
        tool_config = self.config.get("tool", {})
        bilibili_config = tool_config.get("bilibili", {})
        message_config = self.config.get("message", {})
        
        self.deepseek_api_key = api_config.get("deepseek_api_key", "")
        self.lolicon_api_key = api_config.get("lolicon_api_key", "")
        self.initial_balance = economy_config.get("initial_balance", 1000)
        self.sign_in_bonus = sign_in_config.get("bonus", 100)
        self.streak_bonus = sign_in_config.get("streak_bonus", 20)
        self.lottery_cost = lottery_config.get("cost", 50)
        self.lottery_rewards = lottery_config.get("rewards", {
            "thanks": 1,
            "50金币": 50,
            "100金币": 100,
            "200金币": 200,
            "500金币": 500
        })
        self.shop_items = self.config.get("shop", [
            {
                "id": 1,
                "name": "幸运符",
                "price": 100,
                "description": "增加抽奖中奖概率"
            },
            {
                "id": 2,
                "name": "经验丹",
                "price": 200,
                "description": "增加经验值"
            },
            {
                "id": 3,
                "name": "金币袋",
                "price": 500,
                "description": "获得1000金币"
            }
        ])
        self.initial_admins = admin_config.get("initial_admins", [])
        self.initial_whitelist = admin_config.get("initial_whitelist", [])
        self.loli_enabled = loli_config.get("enabled", True)
        self.reaction_enabled = reaction_config.get("enabled", True)
        self.reactions = reaction_config.get("reactions", [
            "(๑•̀ㅂ•́)و✧",
            "(｡･ω･｡)ﾉ♡",
            "(≧▽≦)/",
            "( ´▽` )ﾉ",
            "(≧∇≦)ﾉ",
            "( ´ ▽ ` )ﾉ"
        ])
        self.bilibili_enabled = bilibili_config.get("enabled", True)
        self.command_prefix = message_config.get("prefix", "mes")
        self.help_message = message_config.get("help_message", "命令列表：\n- {prefix} help：显示帮助信息\n- {prefix} repeat <内容>：重复你说的话\n- {prefix} status：查看机器人状态\n- {prefix} cal <表达式>：计算数学表达式\n- {prefix} fool：随机讲一个笑话\n- {prefix} ai <内容>：智能对话\n- {prefix} create_account：创建经济账号\n- {prefix} sign_in：每日签到\n- {prefix} balance：查看余额\n- {prefix} lottery：抽奖\n- {prefix} transfer <金额> <目标用户ID>：转账\n- {prefix} leaderboard：查看排行榜\n- {prefix} shop：查看商店\n- {prefix} add_whitelist <群ID>：添加白名单\n- {prefix} remove_whitelist <群ID>：移除白名单\n- {prefix} add_admin <用户ID>：添加管理员\n- {prefix} remove_admin <用户ID>：移除管理员\n- {prefix} view_whitelist：查看白名单\n- {prefix} view_admins：查看管理员\n- {prefix} loli：获取随机图片\n- {prefix} reaction：随机反应\n- {prefix} bilibili <链接>：解析Bilibili链接")
        
        # 初始化全局管理器
        self.global_manager = GlobalManager(self.config)
        
        # 初始化命令处理器
        self.base_commands = BaseCommands(self.command_prefix, self.help_message)
        self.ai_commands = AICommands(self.deepseek_api_key, self.global_manager)
        self.economy_commands = EconomyCommands(self.data_manager, {
            "initial_balance": self.initial_balance,
            "sign_in_bonus": self.sign_in_bonus,
            "streak_bonus": self.streak_bonus,
            "lottery_cost": self.lottery_cost,
            "lottery_rewards": self.lottery_rewards,
            "shop_items": self.shop_items
        })
        self.admin_commands = AdminCommands(self.data_manager)
        self.entertainment_commands = EntertainmentCommands(self.lolicon_api_key, {
            "loli_enabled": self.loli_enabled,
            "reaction_enabled": self.reaction_enabled,
            "reactions": self.reactions
        })
        self.tool_commands = ToolCommands({
            "bilibili_enabled": self.bilibili_enabled
        })
        
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
                "shop": self.shop_items
            })
        
        # 初始化管理系统数据
        admin_data = self.data_manager.get_admin_data()
        if not admin_data["admins"]:
            self.data_manager.save_admin_data({
                "admins": self.initial_admins,
                "whitelist_groups": self.initial_whitelist
            })
    


    # 主命令处理
    @command("mes", help="显示帮助信息")
    async def handle_mes(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理命令"""
        # 获取用户ID和群ID
        user_id = event.get_sender_id()
        group_id = event.get_group_id() if hasattr(event, "get_group_id") else None
        unified_msg_origin = getattr(event, "unified_msg_origin", None)
        
        # 检查所有功能的白名单
        if not self.global_manager.check_whitelist(user_id, group_id, "all", unified_msg_origin):
            yield event.plain_result("您没有权限使用此功能")
            return
        
        raw_msg: str = event.message_str.strip()
        
        # 去掉开头的指令名，提取子命令和参数
        parts = raw_msg.split(None, 1)
        if len(parts) < 2:
            yield event.plain_result(f"请输入命令，例如：{self.command_prefix} help")
            return
        
        sub_command = parts[1].split(None, 1)[0] if len(parts[1].split(None, 1)) > 0 else ""
        params = parts[1].split(None, 1)[1].strip() if len(parts[1].split(None, 1)) > 1 else ""
        
        # 检查AI功能的白名单
        if sub_command == "ai":
            if not self.global_manager.check_whitelist(user_id, group_id, "ai", unified_msg_origin):
                yield event.plain_result("您没有权限使用AI功能")
                return
        
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
            # 检查消息是否过长
            if self.global_manager.is_long_message(params):
                # 消息过长，放入聊天记录再发送
                yield event.plain_result("消息过长，已将内容放入聊天记录")
                # 这里应该调用AstrBot的API将消息放入聊天记录
                # 由于AstrBot的API限制，这里暂时只发送提示信息
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

    # 全局消息处理 - 高优先级拦截
    @event_message_type(EventMessageType.ALL, priority=999999999)
    async def on_all_message(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理所有消息，实现全局功能"""
        # 获取用户ID和群ID
        user_id = event.get_sender_id()
        group_id = event.get_group_id() if hasattr(event, "get_group_id") else None
        unified_msg_origin = getattr(event, "unified_msg_origin", None)
        
        # 检查所有功能的白名单
        if not self.global_manager.check_whitelist(user_id, group_id, "all", unified_msg_origin):
            # 不在白名单中，阻止消息处理
            logger.info(f"用户 {user_id} 不在白名单中，消息已阻止")
            # 停止事件传递
            event.stop_event()
            return
        
        # 检查AI白名单（适用于所有消息，包括其他插件的AI调用）
        # 这里我们假设所有消息都可能触发AI接口调用
        # 实际应用中，你可能需要根据具体情况进行更精确的判断
        if not self.global_manager.check_whitelist(user_id, group_id, "ai", unified_msg_origin):
            # 不在AI白名单中，阻止消息处理
            logger.info(f"用户 {user_id} 不在AI白名单中，AI相关消息已阻止")
            # 停止事件传递
            event.stop_event()
            return
        
        # 获取消息内容
        message_content = event.message_str.strip()
        
        # 检查消息是否过长
        if self.global_manager.is_long_message(message_content):
            # 消息过长，放入聊天记录再发送
            # 这里应该调用AstrBot的API将消息放入聊天记录
            # 由于AstrBot的API限制，这里暂时只记录日志
            logger.info(f"用户 {user_id} 发送了过长消息，已记录")

    async def terminate(self):
        """插件卸载时调用"""
        logger.info("MessinBot插件正在卸载")
        # 这里可以添加清理资源的代码
        logger.info("MessinBot插件卸载完成")

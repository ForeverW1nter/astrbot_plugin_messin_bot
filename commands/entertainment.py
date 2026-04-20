import random
from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent
from ..api.api_client import APIClient

class EntertainmentCommands:
    """娱乐命令处理类"""

    def __init__(self, lolicon_api_key, config=None):
        """初始化娱乐命令处理器
        
        Args:
            lolicon_api_key: Lolicon API密钥
            config: 配置参数
        """
        self.lolicon_api_key = lolicon_api_key
        self.config = config or {
            "loli_enabled": True,
            "reaction_enabled": True,
            "reactions": [
                "(๑•̀ㅂ•́)و✧",
                "(｡･ω･｡)ﾉ♡",
                "(≧▽≦)/",
                "( ´▽` )ﾉ",
                "(≧∇≦)ﾉ",
                "( ´ ▽ ` )ﾉ"
            ]
        }
        self.loli_enabled = self.config.get("loli_enabled", True)
        self.reaction_enabled = self.config.get("reaction_enabled", True)
        self.reactions = self.config.get("reactions", [
            "(๑•̀ㅂ•́)و✧",
            "(｡･ω･｡)ﾉ♡",
            "(≧▽≦)/",
            "( ´▽` )ﾉ",
            "(≧∇≦)ﾉ",
            "( ´ ▽ ` )ﾉ"
        ])

    async def handle_loli(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理图片命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        if not self.loli_enabled:
            yield event.plain_result("图片功能已禁用")
            return
            
        if not self.lolicon_api_key:
            yield event.plain_result("请先在配置中设置Lolicon API Key")
            return
        
        try:
            # 调用Lolicon API
            response = await APIClient.call_lolicon_api(self.lolicon_api_key)
            if response:
                yield event.plain_result(response)
            else:
                yield event.plain_result("获取图片失败")
        except Exception as e:
            yield event.plain_result(f"获取图片失败：{e}")

    async def handle_reaction(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理反应命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        if not self.reaction_enabled:
            yield event.plain_result("反应功能已禁用")
            return
            
        if not self.reactions:
            yield event.plain_result("没有配置反应表情")
            return
            
        reaction = random.choice(self.reactions)
        yield event.plain_result(reaction)

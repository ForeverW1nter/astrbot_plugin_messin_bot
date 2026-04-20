import random
from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent
from ..api.api_client import APIClient

class EntertainmentCommands:
    """娱乐命令处理类"""

    def __init__(self, lolicon_api_key):
        """初始化娱乐命令处理器
        
        Args:
            lolicon_api_key: Lolicon API密钥
        """
        self.lolicon_api_key = lolicon_api_key

    async def handle_loli(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理图片命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
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
        reactions = [
            "(๑•̀ㅂ•́)و✧",
            "(｡･ω･｡)ﾉ♡",
            "(≧▽≦)/",
            "( ´▽` )ﾉ",
            "(๑•̀ㅂ•́)و✧",
            "(≧∇≦)ﾉ",
            "( ´ ▽ ` )ﾉ",
            "(๑•̀ㅂ•́)و✧",
            "(｡･ω･｡)ﾉ♡",
            "(≧▽≦)/"
        ]
        reaction = random.choice(reactions)
        yield event.plain_result(reaction)

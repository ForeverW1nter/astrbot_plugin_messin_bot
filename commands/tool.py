from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent
from ..utils.tools import Tools

class ToolCommands:
    """工具命令处理类"""

    async def handle_bilibili_parse(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理Bilibili解析命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        url = params.strip()
        if url:
            try:
                # 解析Bilibili链接
                result = Tools.parse_bilibili(url)
                if result:
                    yield event.plain_result(result)
                else:
                    yield event.plain_result("解析失败")
            except Exception as e:
                yield event.plain_result(f"解析失败：{e}")
        else:
            yield event.plain_result("请输入Bilibili链接")

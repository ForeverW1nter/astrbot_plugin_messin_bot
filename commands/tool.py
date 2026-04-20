from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent
from ..utils.tools import Tools

class ToolCommands:
    """工具命令处理类"""

    def __init__(self, config=None):
        """初始化工具命令处理器
        
        Args:
            config: 配置参数
        """
        self.config = config or {
            "bilibili_enabled": True
        }
        self.bilibili_enabled = self.config.get("bilibili_enabled", True)

    async def handle_bilibili_parse(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理Bilibili解析命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        if not self.bilibili_enabled:
            yield event.plain_result("Bilibili解析功能已禁用")
            return
            
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

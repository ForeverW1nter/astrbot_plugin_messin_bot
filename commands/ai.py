from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent
from ..api.api_client import APIClient

class AICommands:
    """AI命令处理类"""

    def __init__(self, deepseek_api_key, global_manager=None):
        """初始化AI命令处理器
        
        Args:
            deepseek_api_key: DeepSeek API密钥
            global_manager: 全局管理器，用于白名单检查
        """
        self.deepseek_api_key = deepseek_api_key
        self.global_manager = global_manager

    async def handle_ai(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理AI对话命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        # 获取用户ID和群ID
        user_id = event.get_sender_id()
        group_id = event.get_group_id() if hasattr(event, "get_group_id") else None
        unified_msg_origin = getattr(event, "unified_msg_origin", None)
        
        # 检查AI白名单
        if self.global_manager and not self.global_manager.check_whitelist(user_id, group_id, "ai", unified_msg_origin):
            yield event.plain_result("您没有权限使用AI功能")
            return
        
        prompt = params.strip()
        if prompt:
            if not self.deepseek_api_key:
                yield event.plain_result("请先在配置中设置DeepSeek API Key")
                return
            
            try:
                # 调用DeepSeek API
                response = await APIClient.call_deepseek_api(self.deepseek_api_key, prompt)
                yield event.plain_result(f"【AI回复】{response}")
            except Exception as e:
                yield event.plain_result(f"AI调用失败：{e}")
        else:
            yield event.plain_result("请输入对话内容")

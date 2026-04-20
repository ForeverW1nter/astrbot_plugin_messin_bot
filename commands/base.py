import random
from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent

class BaseCommands:
    """基础命令处理类"""

    async def handle_help(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理帮助命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        help_text = "命令列表：\n"
        help_text += "- mes help：显示帮助信息\n"
        help_text += "- mes repeat <内容>：重复你说的话\n"
        help_text += "- mes status：查看机器人状态\n"
        help_text += "- mes cal <表达式>：计算数学表达式\n"
        help_text += "- mes fool：随机讲一个笑话\n"
        help_text += "- mes ai <内容>：智能对话\n"
        help_text += "- mes create_account：创建经济账号\n"
        help_text += "- mes sign_in：每日签到\n"
        help_text += "- mes balance：查看余额\n"
        help_text += "- mes lottery：抽奖\n"
        help_text += "- mes transfer <金额> <目标用户ID>：转账\n"
        help_text += "- mes leaderboard：查看排行榜\n"
        help_text += "- mes shop：查看商店\n"
        help_text += "- mes add_whitelist <群ID>：添加白名单\n"
        help_text += "- mes remove_whitelist <群ID>：移除白名单\n"
        help_text += "- mes add_admin <用户ID>：添加管理员\n"
        help_text += "- mes remove_admin <用户ID>：移除管理员\n"
        help_text += "- mes view_whitelist：查看白名单\n"
        help_text += "- mes view_admins：查看管理员\n"
        help_text += "- mes loli：获取随机图片\n"
        help_text += "- mes reaction：随机反应\n"
        help_text += "- mes bilibili <链接>：解析Bilibili链接\n"
        yield event.plain_result(help_text)

    async def handle_repeat(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理重复命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        if params:
            yield event.plain_result(params)
        else:
            yield event.plain_result("请输入要重复的内容")

    async def handle_status(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理状态命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        status_text = "机器人状态：\n"
        status_text += "- 运行中\n"
        status_text += "- 已连接到AstrBot\n"
        status_text += "- 插件系统正常\n"
        yield event.plain_result(status_text)

    async def handle_cal(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理计算命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        if params:
            try:
                result = eval(params)
                yield event.plain_result(f"计算结果：{result}")
            except Exception as e:
                yield event.plain_result(f"计算错误：{e}")
        else:
            yield event.plain_result("请输入数学表达式")

    async def handle_fool(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理笑话命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        jokes = [
            "为什么程序员喜欢用黑底白字？因为他们是夜间生物。",
            "程序员的女朋友问他：你为什么总是把我放在最后？程序员回答：因为在代码中，最后的才是最重要的。",
            "什么是程序员最害怕的？是需求的变化，就像刚写好的代码被要求重写一样。",
            "程序员的三个境界：初级：能写出能运行的代码；中级：能写出能维护的代码；高级：能写出别人能维护的代码。",
            "为什么程序员不喜欢大自然？因为它有太多的虫子。"
        ]
        joke = random.choice(jokes)
        yield event.plain_result(joke)

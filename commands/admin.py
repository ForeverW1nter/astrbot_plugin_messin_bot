from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent

class AdminCommands:
    """管理命令处理类"""

    def __init__(self, data_manager):
        """初始化管理命令处理器
        
        Args:
            data_manager: 数据管理器
        """
        self.data_manager = data_manager

    async def handle_add_whitelist(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理添加白名单命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        group_id = params.strip()
        if not group_id:
            yield event.plain_result("请输入群ID")
            return
        
        admin_data = self.data_manager.get_admin_data()
        if group_id not in admin_data["whitelist_groups"]:
            admin_data["whitelist_groups"].append(group_id)
            self.data_manager.save_admin_data(admin_data)
            yield event.plain_result(f"群{group_id}已添加到白名单")
        else:
            yield event.plain_result("群已在白名单中")

    async def handle_remove_whitelist(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理移除白名单命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        group_id = params.strip()
        if not group_id:
            yield event.plain_result("请输入群ID")
            return
        
        admin_data = self.data_manager.get_admin_data()
        if group_id in admin_data["whitelist_groups"]:
            admin_data["whitelist_groups"].remove(group_id)
            self.data_manager.save_admin_data(admin_data)
            yield event.plain_result(f"群{group_id}已从白名单移除")
        else:
            yield event.plain_result("群不在白名单中")

    async def handle_add_admin(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理添加管理员命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        user_id = params.strip()
        if not user_id:
            yield event.plain_result("请输入用户ID")
            return
        
        admin_data = self.data_manager.get_admin_data()
        if user_id not in admin_data["admins"]:
            admin_data["admins"].append(user_id)
            self.data_manager.save_admin_data(admin_data)
            yield event.plain_result(f"用户{user_id}已添加为管理员")
        else:
            yield event.plain_result("用户已是管理员")

    async def handle_remove_admin(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理移除管理员命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        user_id = params.strip()
        if not user_id:
            yield event.plain_result("请输入用户ID")
            return
        
        admin_data = self.data_manager.get_admin_data()
        if user_id in admin_data["admins"]:
            admin_data["admins"].remove(user_id)
            self.data_manager.save_admin_data(admin_data)
            yield event.plain_result(f"用户{user_id}已移除管理员权限")
        else:
            yield event.plain_result("用户不是管理员")

    async def handle_view_whitelist(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理查看白名单命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        admin_data = self.data_manager.get_admin_data()
        whitelist = admin_data["whitelist_groups"]
        
        if not whitelist:
            yield event.plain_result("白名单为空")
            return
        
        whitelist_info = "白名单群：\n"
        for group_id in whitelist:
            whitelist_info += f"- {group_id}\n"
        
        yield event.plain_result(whitelist_info)

    async def handle_view_admins(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理查看管理员命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        # 检查是否为管理员
        if not self.data_manager.is_admin(event.get_sender_id()):
            yield event.plain_result("权限不足")
            return
        
        admin_data = self.data_manager.get_admin_data()
        admins = admin_data["admins"]
        
        if not admins:
            yield event.plain_result("暂无管理员")
            return
        
        admins_info = "管理员：\n"
        for admin_id in admins:
            admins_info += f"- {admin_id}\n"
        
        yield event.plain_result(admins_info)

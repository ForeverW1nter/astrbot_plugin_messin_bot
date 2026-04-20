class GlobalManager:
    """全局管理器，处理全局功能"""

    def __init__(self, config=None):
        """初始化全局管理器
        
        Args:
            config: 配置参数
        """
        self.config = config or {}
        global_config = self.config.get("global", {})
        whitelist_config = global_config.get("whitelist", {})
        long_message_config = global_config.get("long_message", {})
        
        # 白名单配置
        self.whitelist_mode = whitelist_config.get("mode", "whitelist")
        self.ai_whitelist = whitelist_config.get("ai", [])
        self.all_whitelist = whitelist_config.get("all", [])
        
        # 过长消息处理配置
        self.long_message_enabled = long_message_config.get("enabled", True)
        self.max_images = long_message_config.get("max_images", 3)
        self.max_chars = long_message_config.get("max_chars", 100)
        self.max_lines = long_message_config.get("max_lines", 10)

    def check_whitelist(self, user_id, group_id=None, check_type="all", unified_msg_origin=None):
        """检查用户是否在白名单中
        
        Args:
            user_id: 用户ID
            group_id: 群ID（如果是群消息）
            check_type: 检查类型：all（所有功能）或 ai（AI功能）
            unified_msg_origin: 统一消息来源标识
            
        Returns:
            bool: 是否通过检查
        """
        # 确定检查的列表
        if check_type == "ai":
            check_list = self.ai_whitelist
        else:
            check_list = self.all_whitelist
        
        # 如果白名单为空，默认允许所有
        if not check_list:
            return True
        
        # 获取检查对象
        check_targets = []
        if group_id:
            check_targets.append(str(group_id))
        if user_id:
            check_targets.append(str(user_id))
        if unified_msg_origin:
            check_targets.append(unified_msg_origin)
        
        # 如果没有检查对象，默认允许所有
        if not check_targets:
            return True
        
        # 根据模式检查
        if self.whitelist_mode == "whitelist":
            # 白名单模式：只有在列表中的才允许
            for target in check_targets:
                if target in check_list:
                    return True
            return False
        else:
            # 黑名单模式：不在列表中的都允许
            for target in check_targets:
                if target in check_list:
                    return False
            return True

    def is_long_message(self, message):
        """检查消息是否过长
        
        Args:
            message: 消息内容
            
        Returns:
            bool: 是否是过长消息
        """
        if not self.long_message_enabled:
            return False
        
        # 检查字符数
        if len(message) > self.max_chars:
            return True
        
        # 检查行数
        if len(message.split('\n')) > self.max_lines:
            return True
        
        # 检查图片数量（这里简化处理，实际需要根据消息类型检查）
        # 由于AstrBot的消息结构，这里暂时只检查文本部分
        
        return False

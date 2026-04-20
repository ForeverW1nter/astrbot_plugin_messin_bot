import json
import os
from astrbot.api import logger

class DataManager:
    """数据管理类，用于处理经济系统和管理系统的数据"""

    def __init__(self, plugin_dir):
        """初始化数据管理器
        
        Args:
            plugin_dir: 插件目录路径
        """
        # 初始化经济系统数据
        self.economy_data_dir = os.path.join(plugin_dir, "data", "economy")
        os.makedirs(self.economy_data_dir, exist_ok=True)
        self.economy_data_file = os.path.join(self.economy_data_dir, "economy_data.json")
        # 初始化管理系统数据
        self.admin_data_dir = os.path.join(plugin_dir, "data", "admin")
        os.makedirs(self.admin_data_dir, exist_ok=True)
        self.admin_data_file = os.path.join(self.admin_data_dir, "admin_data.json")

    def _load_economy_data(self):
        """加载经济数据
        
        Returns:
            dict: 经济数据
        """
        try:
            if os.path.exists(self.economy_data_file):
                with open(self.economy_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载经济数据失败: {e}")
        return {"users": {}, "shop": []}

    def _save_economy_data(self, data):
        """保存经济数据
        
        Args:
            data: 经济数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.economy_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存经济数据失败: {e}")
            return False

    def _load_admin_data(self):
        """加载管理数据
        
        Returns:
            dict: 管理数据
        """
        try:
            if os.path.exists(self.admin_data_file):
                with open(self.admin_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"加载管理数据失败: {e}")
        return {"admins": [], "whitelist_groups": []}

    def _save_admin_data(self, data):
        """保存管理数据
        
        Args:
            data: 管理数据
            
        Returns:
            bool: 保存是否成功
        """
        try:
            with open(self.admin_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"保存管理数据失败: {e}")
            return False

    # 经济系统数据操作
    def get_economy_data(self):
        """获取经济数据
        
        Returns:
            dict: 经济数据
        """
        return self._load_economy_data()

    def save_economy_data(self, data):
        """保存经济数据
        
        Args:
            data: 经济数据
            
        Returns:
            bool: 保存是否成功
        """
        return self._save_economy_data(data)

    # 管理系统数据操作
    def get_admin_data(self):
        """获取管理数据
        
        Returns:
            dict: 管理数据
        """
        return self._load_admin_data()

    def save_admin_data(self, data):
        """保存管理数据
        
        Args:
            data: 管理数据
            
        Returns:
            bool: 保存是否成功
        """
        return self._save_admin_data(data)

    def is_admin(self, user_id):
        """检查用户是否为管理员
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否为管理员
        """
        admin_data = self._load_admin_data()
        return str(user_id) in admin_data.get("admins", [])

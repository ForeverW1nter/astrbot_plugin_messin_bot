import time
import random
from collections.abc import AsyncGenerator
from astrbot.api.event import AstrMessageEvent

class EconomyCommands:
    """经济系统命令处理类"""

    def __init__(self, data_manager):
        """初始化经济系统命令处理器
        
        Args:
            data_manager: 数据管理器
        """
        self.data_manager = data_manager

    async def handle_create_account(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理创建账号命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        user_id = str(event.get_sender_id())
        economy_data = self.data_manager.get_economy_data()
        
        if user_id in economy_data["users"]:
            yield event.plain_result("账号已存在")
            return
        
        # 创建新账号
        economy_data["users"][user_id] = {
            "balance": 1000,  # 初始金币
            "experience": 0,
            "level": 1,
            "last_sign_in": 0,
            "checkin_streak": 0,
            "inventory": []
        }
        self.data_manager.save_economy_data(economy_data)
        yield event.plain_result("账号创建成功，初始金币1000")

    async def handle_sign_in(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理签到命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        user_id = str(event.get_sender_id())
        economy_data = self.data_manager.get_economy_data()
        
        if user_id not in economy_data["users"]:
            yield event.plain_result("请先创建账号")
            return
        
        user_data = economy_data["users"][user_id]
        now = int(time.time())
        last_sign_in = user_data.get("last_sign_in", 0)
        
        # 检查是否已经签到
        if now - last_sign_in < 86400:  # 24小时
            yield event.plain_result("今日已签到")
            return
        
        # 计算连续签到奖励
        streak = user_data.get("checkin_streak", 0) + 1
        bonus = 100 + (streak - 1) * 20  # 连续签到奖励递增
        
        # 更新数据
        user_data["balance"] += bonus
        user_data["last_sign_in"] = now
        user_data["checkin_streak"] = streak
        user_data["experience"] += 10
        
        # 检查升级
        if user_data["experience"] >= user_data["level"] * 100:
            user_data["level"] += 1
            user_data["experience"] = 0
            yield event.plain_result(f"签到成功！获得{bonus}金币，经验+10，升级到{user_data['level']}级")
        else:
            yield event.plain_result(f"签到成功！获得{bonus}金币，经验+10，连续签到{streak}天")
        
        self.data_manager.save_economy_data(economy_data)

    async def handle_lottery(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理抽奖命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        user_id = str(event.get_sender_id())
        economy_data = self.data_manager.get_economy_data()
        
        if user_id not in economy_data["users"]:
            yield event.plain_result("请先创建账号")
            return
        
        user_data = economy_data["users"][user_id]
        if user_data["balance"] < 50:
            yield event.plain_result("金币不足，抽奖需要50金币")
            return
        
        # 扣除金币
        user_data["balance"] -= 50
        
        # 抽奖逻辑
        rewards = [
            (1, "谢谢参与", 0),
            (2, "50金币", 50),
            (3, "100金币", 100),
            (4, "200金币", 200),
            (5, "500金币", 500)
        ]
        
        # 计算概率
        total = sum([r[0] for r in rewards])
        rand = random.randint(1, total)
        
        current = 0
        for weight, name, amount in rewards:
            current += weight
            if rand <= current:
                if amount > 0:
                    user_data["balance"] += amount
                    yield event.plain_result(f"抽奖结果：{name}，获得{amount}金币")
                else:
                    yield event.plain_result(f"抽奖结果：{name}")
                break
        
        self.data_manager.save_economy_data(economy_data)

    async def handle_balance(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理余额命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        user_id = str(event.get_sender_id())
        economy_data = self.data_manager.get_economy_data()
        
        if user_id not in economy_data["users"]:
            yield event.plain_result("请先创建账号")
            return
        
        user_data = economy_data["users"][user_id]
        yield event.plain_result(f"余额：{user_data['balance']}金币，等级：{user_data['level']}，经验：{user_data['experience']}")

    async def handle_transfer(self, event: AstrMessageEvent, params: str) -> AsyncGenerator:
        """处理转账命令
        
        Args:
            event: 消息事件
            params: 命令参数
            
        Yields:
            消息事件结果
        """
        if not params:
            yield event.plain_result("请输入转账金额和目标用户")
            return
        
        try:
            amount_str, target_id = params.split()
            amount = int(amount_str)
        except:
            yield event.plain_result("格式错误，请输入：mes transfer <金额> <目标用户ID>")
            return
        
        user_id = str(event.get_sender_id())
        economy_data = self.data_manager.get_economy_data()
        
        if user_id not in economy_data["users"]:
            yield event.plain_result("请先创建账号")
            return
        
        if target_id not in economy_data["users"]:
            yield event.plain_result("目标用户不存在")
            return
        
        user_data = economy_data["users"][user_id]
        if user_data["balance"] < amount:
            yield event.plain_result("金币不足")
            return
        
        # 执行转账
        user_data["balance"] -= amount
        economy_data["users"][target_id]["balance"] += amount
        self.data_manager.save_economy_data(economy_data)
        yield event.plain_result(f"转账成功！向{target_id}转账{amount}金币")

    async def handle_leaderboard(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理排行榜命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        economy_data = self.data_manager.get_economy_data()
        users = economy_data["users"]
        
        if not users:
            yield event.plain_result("暂无数据")
            return
        
        # 按余额排序
        sorted_users = sorted(users.items(), key=lambda x: x[1]["balance"], reverse=True)[:10]
        
        leaderboard = "富豪排行榜：\n"
        for i, (user_id, user_data) in enumerate(sorted_users, 1):
            leaderboard += f"{i}. {user_id}：{user_data['balance']}金币\n"
        
        yield event.plain_result(leaderboard)

    async def handle_shop(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理商店命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        economy_data = self.data_manager.get_economy_data()
        shop = economy_data["shop"]
        
        if not shop:
            yield event.plain_result("商店暂无商品")
            return
        
        shop_info = "商店商品：\n"
        for item in shop:
            shop_info += f"{item['id']}. {item['name']} - {item['price']}金币：{item['description']}\n"
        
        yield event.plain_result(shop_info)

    async def handle_transactions(self, event: AstrMessageEvent) -> AsyncGenerator:
        """处理交易记录命令
        
        Args:
            event: 消息事件
            
        Yields:
            消息事件结果
        """
        yield event.plain_result("交易记录功能开发中")

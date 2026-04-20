import aiohttp
from astrbot.api import logger

class APIClient:
    """API客户端类，用于处理各种API调用"""

    @staticmethod
    async def call_deepseek_api(api_key, prompt):
        """调用DeepSeek API
        
        Args:
            api_key: DeepSeek API密钥
            prompt: 提示词
            
        Returns:
            str: API响应内容
        """
        url = "https://api.deepseek.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
            except Exception as e:
                logger.error(f"调用DeepSeek API失败: {e}")
                raise

    @staticmethod
    async def call_lolicon_api(api_key):
        """调用Lolicon API
        
        Args:
            api_key: Lolicon API密钥
            
        Returns:
            str: 图片URL
        """
        url = "https://api.lolicon.app/setu/v2"
        params = {
            "apikey": api_key,
            "r18": 0,
            "num": 1
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    result = await response.json()
                    if result["code"] == 0 and result["data"]:
                        data = result["data"][0]
                        return data["urls"]["original"]
                    return None
            except Exception as e:
                logger.error(f"调用Lolicon API失败: {e}")
                raise

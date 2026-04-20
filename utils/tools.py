import re

class Tools:
    """工具类，提供各种工具函数"""

    @staticmethod
    def parse_bilibili(url):
        """解析Bilibili链接
        
        Args:
            url: Bilibili链接
            
        Returns:
            str: 解析结果
        """
        # 提取BV号或AV号
        bv_match = re.search(r'(BV[a-zA-Z0-9]+)', url)
        av_match = re.search(r'(av\d+)', url)
        
        if bv_match:
            bv_id = bv_match.group(1)
            return f"Bilibili视频链接解析成功\nBV号: {bv_id}\n链接: https://www.bilibili.com/video/{bv_id}"
        elif av_match:
            av_id = av_match.group(1)
            return f"Bilibili视频链接解析成功\nAV号: {av_id}\n链接: https://www.bilibili.com/video/{av_id}"
        else:
            return "无法解析Bilibili链接"

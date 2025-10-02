##项目代码和视频由AI超元域频道原创，禁止盗搬
import os
import subprocess

from autogen import ConversableAgent
from dotenv import load_dotenv
load_dotenv()
# Define system messages for the agents
title_creator_sm = """你是一位专业的标题制作者。当给定新闻内容时：
1. 创建一个吸引眼球的中文标题，可以适度夸张但必须基于事实
2. 标题长度应在15-30个字符之间
3. 尽可能使用情感词汇和数字
4. 添加感叹号以增强效果
"""

eng_converter_sm = """你是一位专业的英文缩写专家。当给定一个中文标题时：
1. 使用关键字的首字母创建一个有意义的英文缩写
2. 解释每个字母的含义
3. 尽量控制在6个字母以内
"""
qwen_api_key = os.getenv("QWEN_API_KEY")

qwen = {
    "config_list": [
        {
            "model": "qwen-max",
            "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            "api_key": qwen_api_key,
        },
    ],
    "cache_seed": None,  # Disable caching.
}
# Create the agents
title_creator = ConversableAgent(
    name="TitleCreator",
    system_message=title_creator_sm,
    llm_config=qwen
)

eng_converter = ConversableAgent(
    name="EngConverter", 
    system_message=eng_converter_sm,
    llm_config=qwen
)

def process_news(news_content):
    # Get clickbait title from first agent
    content = news_content.replace("\n", "")
    title_chat = title_creator.initiate_chat(
        eng_converter,
        message=f"请为以下新闻内容创建一个吸引眼球的中文标题：{content}，请直接输出标题，不要输出任何解释！",
        max_turns=1  # 限制对话轮次为1
    )
    
    # Get English abbreviation from second agent
    title = title_chat.chat_history[1]["content"]
    abbr_chat = eng_converter.initiate_chat(
        title_creator,
        message=f"请为以下中文标题创建一个有意义的英文缩写,尽量控制在6个字母以内，连续字母，小写字母，不要任何符号和空格：{title}，请直接输出英文缩写，不要输出任何解释！",
        max_turns=1  # 限制对话轮次为1
    )
    title_en = abbr_chat.chat_history[1]["content"]
    # Get content from third agent
    return {
        "title": title,
        "title_en": title_en,
        "content": content
    }

if __name__ == "__main__":
    with open("news.txt", "r") as file:
        news_content = file.read()
        result = process_news(news_content)
        print(result)

import os

import requests
import uuid
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("ZHIPU_API_KEY")

def run_v4_sync():
    msg = [
        {
            "role": "user",
            "content":"deepseek使用技巧"

        }
    ]
    tool = "web-search-pro"
    url = "https://open.bigmodel.cn/api/paas/v4/tools"
    request_id = str(uuid.uuid4())
    data = {
        "request_id": request_id,
        "tool": tool,
        "stream": False,
        "messages": msg
    }

    resp = requests.post(
        url,
        json=data,
        headers={'Authorization': api_key},
        timeout=300
    )
    print(resp.content.decode())



if __name__ == '__main__':
    run_v4_sync()
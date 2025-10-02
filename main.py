import json
from step_01_create_title import process_news
from step_02_create_audio_short import create_audio


if __name__ == "__main__":
    with open("news.txt", "r") as file:
        news_content = file.read()
        result = process_news(news_content)
        print(result)
        result_json = json.dumps(result)
        with open("result.json", "w") as file:
            file.truncate(0)
            file.write(result_json.encode('utf-8').decode('unicode_escape'))
        print("result.json 已保存")
        with open("result.json", "r") as file:
            result = json.load(file)
            create_audio(result["title"], result["title_en"], result["content"])

import json
from autogen import ConversableAgent
import glob
import os
import subprocess
import shlex
from dotenv import load_dotenv
load_dotenv()
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
qwen_api_key = os.getenv("QWEN_API_KEY")
gpt_api_key = os.getenv("GPT_API_KEY")

def run_chattts(text, output_file, speaker_index):
    # 对文本进行转义和格式化
    escaped_text = shlex.quote(text)

    # 根据说话者的索引选择不同的声音参数
    if speaker_index % 2 == 0:
        voice_param = "-s 2"  # 女性声音
    else:
        voice_param = "-s 333"  # 男性声音
    # if speaker_index % 2 == 0:
    #     voice_param = "-s 54321"  # 女性声音
    # else:
    #     voice_param = "-s 12345"  # 男性声音

    command = f"chattts {voice_param} -o {output_file} {escaped_text}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")


def clear_gen_folder(dir_name):
    # 获取 gen 文件夹下的所有文件路径
    files = glob.glob(f"gen/{dir_name}/*")
    for file in files:
        try:
            os.remove(file)
            print(f"Deleted file: {file}")
        except Exception as e:
            print(f"Error deleting file {file}: {e}")



gpt4 = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "base_url": "https://api.openai.com/v1",
            "api_key": gpt_api_key,
        },
    ],
    "cache_seed": None,  # Disable caching.
}
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

deepseek_v3 = {
    "config_list": [
        {
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com/v1",
            "api_key": deepseek_api_key,
        },
    ],
    "cache_seed": None,  # Disable caching.
}



def create_audio(title, title_en, news):
    round_num=10
    role01 = "主持人"
    role02 = "张明远教授"
    sm01 = f"你是{role01},你是知识分子，你擅长哲学思辨，提问由浅入深，精准犀利，以{role01}的口吻和性格对{role02}的回答进行回应并进行进一步提问，请尽量口语化，请在每次开始说话的时候增加“嗯，”作为延时。你们需要围绕{news}进行由浅入深的讨论，请把提问保持在30字以内。一共有{str(round_num)}轮对话，请别忘记在第{str(round_num-1)}轮开始说结束语，不要提前说结束语！对话中请不要出现非对话内容。对话中禁止出现状语“地”字！如：深刻地、更好地"
    sm02 = f"你是{role02},你博学多识，尤其擅长哲学思考，回答精准。请根据{role01}的发言，以{role02}的口吻和性格进行回应，尽量口语化，请在每次开始说话的时候增加“嗯...”作为思考延时。你们需要围绕{news}进行讨论，请把回答保持在120字以内。"
    m = "您好，张教授，感谢您接受采访，跟大家打个招呼吧。"


    rl01 = ConversableAgent(
        "01",
        llm_config=qwen,
        system_message=sm01,
    )
    rl02 = ConversableAgent(
        "02",
        llm_config=qwen,
        system_message=sm02,
    )

    chat_result = rl01.initiate_chat(rl02, message=m, max_turns=round_num)

    clear_gen_folder(title_en)

    # 确保目标目录存在
    os.makedirs(f"gen/{title_en}", exist_ok=True)

    # 生成音频文件
    for i, message in enumerate(chat_result.chat_history):
        text = message["content"]
        text.replace('地', '的')
        output_file = f"gen/{title_en}/output_{i}.wav"
        output_file_for_concat = f"output_{i}.wav"
        run_chattts(text, output_file, i)
        with open(f"gen/{title_en}/concat.txt", 'a') as file:
            file.write(f'file \'{output_file_for_concat}\'\n')
        with open(f"gen/{title_en}/contents.txt", 'a') as file:
            file.write(role01+'：'+text+'\n'  if i%2==0  else role02 + '：' + text + '\n')

    c = f'ffmpeg -f concat -i gen/{title_en}/concat.txt -c copy "gen/{title_en}/{title}.wav"'
    try:
        subprocess.run(c, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")


if __name__ == "__main__":
    with open("result.json", "r") as file:
        result = json.load(file)
        create_audio(result["title"], result["title_en"], result["content"])

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
# 1. 连接本地 LM Studio 的 API
# 从环境变量中读取地址，没设置则默认走localhost
base_url = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
api_key = os.getenv("LM_STUDIO_API_KEY", "lm-studio")
# 模型名称也改成从环境变量读取
model_name = os.getenv("LM_STUDIO_MODEL", "qwen2.5-7b-instruct")

client = OpenAI(
    base_url=base_url,
    api_key=api_key,
)

print("=== 本地大模型 CLI 应用已启动 ===")
print("（输入 'exit' 退出程序）\n")

# 2. 记录对话历史（这样它能记住上下文）
messages = [
    {"role": "system", "content": "你是一个专业的AI助手，用通俗易懂的语言回答问题。"}
]

while True:
    user_input = input("你: ")
    if user_input.lower() == 'exit':
        print("再见！")
        break

    # 把用户的话加入历史
    messages.append({"role": "user", "content": user_input})

    try:
        # 3. 发送请求给本地模型
        response = client.chat.completions.create(
            # ⚠️ 这里必须和你 LM Studio 里的 API Identifier 完全一致
            model=model_name,
            messages=messages,
            temperature=0.7,
        )

        # 4. 提取回复并打印
        ai_reply = response.choices[0].message.content
        print(f"AI: {ai_reply}\n")

        # 把 AI 的回复也加入历史
        messages.append({"role": "assistant", "content": ai_reply})

    except Exception as e:
        print(f"请求失败: {e}\n")
from openai import OpenAI
import os
import json


TOGETHER_API_KEY = '6029667f7ff11510b9432d899196f9704d2e982a9a1fa2af35b621b4025514a5'
client = OpenAI(api_key=TOGETHER_API_KEY, base_url="https://api.together.xyz/v1")
response = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-V3",
    messages=[
        {"role": "system", "content": "Bạn là một người hiểu rất rõ về luật pháp của Việt Nam"},
        {"role": "user", "content": "vượt đèn đỏ bị phạt thế nào"},
    ],
    stream=False
)
print(response.choices[0].message.content)

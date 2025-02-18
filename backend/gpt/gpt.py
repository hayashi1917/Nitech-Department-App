import openai
import os

# 環境変数からAPIキーを取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_GPT_response(message: str):
    #GPTのレスポンスを取得
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "prompt is in English, but you output response in Japanese",
            },
            {
                "role": "user",
                "content": f"""
                    I take a test for getting a suitable department for university.
                    {message}
                    Please comment about my suitable department.
                """,
            },
        ],
    )

    return response.choices[0].message.content



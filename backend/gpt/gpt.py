import openai
import os
import logging

# 環境変数からAPIキーを取得
openai.api_key = os.environ.get("OPENAI_API_KEY")
logger = logging.getLogger(__name__)

def get_GPT_response(message: str):
    #GPTのレスポンスを取得
    try:
        response = openai.ChatCompletion.create(
            model="gpt-5.4-nano-2026-03-17",
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
    except openai.error.OpenAIError:
        logger.exception("OpenAI API request failed.")
        return "AIコメントの生成に失敗しました。診断結果は上記をご確認ください。"

    return response.choices[0].message.content


import openai
import os

# 環境変数からAPIキーを取得
openai.api_key = os.environ.get("OPENAI_API_KEY")

def get_GPT_response(EM: int, PE: int, LC: int, AC: int, CS: int):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "prompt is in English, but you output response in Japanese",
            },
            {
                "role": "user",
                "content": f"""
                    I take a test for getting a suitable department for university.
                    Please comment about my score.
                    My Score is below.
                    [
                        "EM": {EM},
                        "PE": {PE},
                        "LC": {LC},
                        "AC": {AC},
                        "CS": {CS},
                    ]
                    EM means Electronics.
                    PE means Physics.
                    LC means Life Sciences.
                    AC means Sociologies.
                    CS means Computer Sciences.

                    Each max score is 80.
                """,
            },
        ],
    )

    return response.choices[0].message.content

# 動作確認
# print(get_GPT_response(EM=56, PE=55, LC=35, AC=15, CS=69))

import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def generate(self, system: str, user: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            temperature=0,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )

        content = response.choices[0].message.content

        if not isinstance(content, str):
            raise ValueError("OpenAIClient: response content is not a string")

        return content
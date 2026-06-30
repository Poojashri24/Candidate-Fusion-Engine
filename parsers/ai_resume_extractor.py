import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY is not set.")

client = OpenAI()

class AIResumeExtractor:

    def extract(self, text):

        prompt = f"""
Extract candidate details.

Return ONLY JSON.

Fields:

full_name

emails

phones

headline

skills

experience

education

Resume:

{text}
"""

        response = client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[

                {
                    "role":"user",
                    "content":prompt
                }

            ]

        )

        return json.loads(
            response.choices[0].message.content
        )
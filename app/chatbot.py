import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_system_prompt():
    with open("app/prompts/system_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

def ask_chatbot(messages):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    return response.choices[0].message.content

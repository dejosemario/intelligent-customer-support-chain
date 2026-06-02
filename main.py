import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize the client (same as Colab)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY")
)

def call_llm(prompt_text, system_instructions="You are a helpful banking assistant"):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": prompt_text}
        ],
        model=os.environ.get("MODEL_NAME", "meta-llama/llama-3.2-3b-instruct:free"),
        max_tokens=300
    )
    return response.choices[0].message.content

from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat(query: str):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="gpt-4o"
    )
    return chat_completion.choices[0].message.content
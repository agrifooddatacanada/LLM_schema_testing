import os

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
base_url = os.getenv("ANTHROPIC_BASE_URL")
model = os.getenv("ANTHROPIC_MODEL")

print(f"API_KEY loaded: {api_key is not None}")
print(f"BASE_URL = {base_url!r}")
print(f"MODEL = {model!r}")


client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    base_url=os.getenv("ANTHROPIC_BASE_URL")
)

response = client.messages.create(
    model=os.getenv("ANTHROPIC_MODEL"),
    max_tokens=100,
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Connection successful"
        }
    ]
)

print(response.content[0].text)
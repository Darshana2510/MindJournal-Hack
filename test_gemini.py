from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API key loaded:", bool(api_key))

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY was not found in .env"
    )

client = genai.Client(
    api_key=api_key
)

response = client.models.generate_content(
    model=os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    ),
    contents="Say hello to MindJournal in one sentence."
)

print("\nGemini response:")
print(response.text)

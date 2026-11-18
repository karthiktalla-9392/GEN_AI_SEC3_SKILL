import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv(Path(__file__).with_name(".env"))

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or not api_key.strip():
    print("OPENAI_API_KEY is not set. Showing a local demo response (not from an AI API).")
    answer = (
        "Artificial Intelligence (AI) is technology that enables computers "
        "to perform tasks that usually require human intelligence, such as "
        "understanding language, recognizing images, and solving problems."
    )
else:
    client = OpenAI(api_key=api_key.strip())
    response = client.responses.create(
        model="gpt-5.5",
        input="What is Artificial Intelligence? Explain in simple words.",
    )
    answer = response.output_text

print("\nLLM Response:")
print(answer)

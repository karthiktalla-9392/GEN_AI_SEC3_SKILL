import os
from pathlib import Path

from llm_client import DemoProvider, GeminiProvider, LLMClient, OllamaProvider


env_file = Path(__file__).with_name(".env")
try:
    from dotenv import load_dotenv
except ModuleNotFoundError as error:
    if error.name != "dotenv":
        raise
    if env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                name, value = line.split("=", 1)
                value = value.strip().strip("\"'")
                if name.strip():
                    os.environ[name.strip()] = value
else:
    load_dotenv(env_file, override=True)

provider_name = input("Choose provider (demo/gemini/ollama) [demo]: ").strip().lower()
if not provider_name:
    provider_name = "demo"

if provider_name == "demo":
    provider = DemoProvider()
elif provider_name == "gemini":
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key":
        raise ValueError(
            "GEMINI_API_KEY is missing. Add your Gemini API key to the .env file."
        )
    provider = GeminiProvider(
        api_key=api_key,
        model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip(),
    )
elif provider_name == "ollama":
    provider = OllamaProvider(model=os.getenv("OLLAMA_MODEL", "llama3.2").strip())
else:
    raise ValueError("Invalid provider. Choose demo, gemini, or ollama.")

client = LLMClient(provider)
prompt = input("Enter your question: ").strip()
if not prompt:
    raise ValueError("The question cannot be empty.")

answer = client.generate(prompt)
if provider_name == "demo":
    print("\nDemo Response:")
else:
    print("\nLLM Response:")
print(answer)

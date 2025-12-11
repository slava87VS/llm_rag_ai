import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Инициализируем клиент для OpenRouter
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-site.com",  # Замените на ваш URL
        "X-Title": "My RAG Application",  # Замените на название вашего приложения
    }
)

# Делаем запрос
try:
    completion = client.chat.completions.create(
        model=os.getenv("OPENAI_API_MODEL", "openai/gpt-3.5-turbo"),
        messages=[
            {"role": "user", "content": "Привет. Что ты умеешь?"}
        ],
        temperature=0.5
    )
    print(completion.choices[0].message.content)
except Exception as e:
    print(f"Ошибка: {e}")
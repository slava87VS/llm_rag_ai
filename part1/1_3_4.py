import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openai import ChatOpenAI  # Или другой подходящий класс
from langchain_community.chat_models import ChatAnthropic, ChatCohere  # Примеры других провайдеров

load_dotenv()
MODEL_NAME = os.getenv("OPENAI_API_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Убедитесь, что есть ключ API

try:
    # Сначала пробуем как OpenAI-совместимую модель
    model = ChatOpenAI(
        model=MODEL_NAME,
        api_key=OPENAI_API_KEY,
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
except Exception as e:
    print(f"Ошибка инициализации модели: {e}")
    exit(1)

agent = create_agent(
    model=model,  # Передаем созданный объект модели, а не строку
    checkpointer=InMemorySaver(),
)

# Остальной код остается без изменений
conv_1 = {"configurable": {"thread_id": "conversation_001"}}

question1 = "Привет! Меня зовут Алиса"
response1 = agent.invoke(
    {"messages": [{"role": "user", "content": question1}]},
    conv_1
)
print("пользователь 1:", question1)
print("Бот:", response1["messages"][-1].content)

question2 = "Какое у меня имя?"
response2 = agent.invoke(
    {"messages": [{"role": "user", "content": question2}]},
    conv_1
)
print("пользователь 1:", question2)
print("Бот:", response2["messages"][-1].content)

# Новый пользователь с другим thread_id
conv_2 = {"configurable": {"thread_id": "conversation_002"}}

question3 = "Какое у меня имя?"
response3 = agent.invoke(
    {"messages": [{"role": "user", "content": question3}]},
    conv_2
)
print("пользователь 2:", question3)
print("Бот:", response3["messages"][-1].content)
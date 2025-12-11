import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence

MODEL = os.getenv("OPENAI_API_MODEL", "gpt-5")

template = "Отвечай как ассистент: Привет, {name}! Рад тебя видеть. Я могу помочь с вопросами по {topic}."
prompt = PromptTemplate(
    template=template,
    input_variables=["name", "topic"]
)

chain = RunnableSequence(prompt, ChatOpenAI(model=MODEL))

result = chain.invoke({"name": "Анна", "topic": "программированию"})
print(result)
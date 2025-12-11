from langchain_core.runnables import RunnableLambda, RunnablePassthrough
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

def uppercase(text):
    return text.upper()

load_dotenv()
MODEL = os.getenv("OPENAI_API_MODEL")

llm = ChatOpenAI(model=MODEL)
prompt = ChatPromptTemplate.from_template("Привет. Меня зовут {name}")
# Создать словарь из входных данных
chain = {"name": RunnablePassthrough()} | prompt | llm

result = chain.invoke("Ваня") # → {"name": "Ваня"} → prompt → llm
print(result)
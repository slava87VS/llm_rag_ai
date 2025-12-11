import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
MODEL = os.getenv("OPENAI_API_MODEL")

prompt = ChatPromptTemplate.from_template("Привет. Меня зовут {name}")
llm = ChatOpenAI(model=MODEL)

basic_chain = prompt | llm

result = basic_chain.invoke({"name": "Вася"})
print(result)
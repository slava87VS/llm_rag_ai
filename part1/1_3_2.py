from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence

import os
from dotenv import load_dotenv

load_dotenv()


prompt = ChatPromptTemplate.from_template("Переведи на английский: {question}")

model = ChatOpenAI(
    model_name=os.getenv("OPENAI_API_MODEL"),
    temperature=0
)

chain = RunnableSequence(first=prompt, last=model)

result = chain.invoke({"question": "доброе утро"})
print(result.content)
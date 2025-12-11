from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


chat = ChatOpenAI(
    model_name=os.getenv("OPENAI_API_MODEL"),
    temperature=0.7
)

response = chat.invoke("Как варить рожки")
print(response)


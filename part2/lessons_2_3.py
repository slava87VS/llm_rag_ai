import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers.json import JsonOutputParser

load_dotenv()
MODEL = os.getenv("OPENAI_API_MODEL", "gpt-5")

llm = ChatOpenAI(model=MODEL)

parser = JsonOutputParser()
format_instructions = parser.get_format_instructions()

prompt = PromptTemplate(
    template="Пожалуйста, верни данные в формате JSON.\n{format_instructions}\n{question}",
    input_variables=["question"],
    partial_variables={"format_instructions": format_instructions}
)

chain = prompt | llm | parser

result = chain.invoke({"question": "Что такое LangChain?"})
print(result)  # вывод: {'question': 'Что такое LangChain?', 'answer': 'LangChain — это ...'}
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()
MODEL = os.getenv("OPENAI_API_MODEL", "gpt-5")

llm = ChatOpenAI(model=MODEL)

# Определяем схему данных
class BookInfo(BaseModel):
    title: str = Field(..., description="Название книги")
    author: str = Field(..., description="Имя автора")
    tags: list[str] = Field(..., description="Список тегов или жанров")

# Создаём парсер
output_parser = PydanticOutputParser(pydantic_object=BookInfo)
format_instructions = output_parser.get_format_instructions()

# Шаблон промпта
prompt = PromptTemplate(
    template=(
        "Ответь на вопрос в требуемом формате.\n"
        "{format_instructions}\n"
        "Вопрос: {user_question}\nОтвет:"
    ),
    input_variables=["user_question"],
    partial_variables={"format_instructions": format_instructions},
)

# цепочка
chain = prompt | llm | output_parser

# Запуск
result = chain.invoke({"user_question": "Расскажи о книге '1984' Джорджа Оруэлла."})
print(type(result)) # <class '__main__.BookInfo'>
print(result) # title='1984', author='Джордж Оруэлл', tags=['антиутопия', 'классика']


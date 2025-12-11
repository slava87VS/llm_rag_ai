from langchain_core.prompts import PromptTemplate

from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

# Создаём шаблон чата с системным и пользовательским сообщением
chat_template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("Ты — опытный переводчик."),
    HumanMessagePromptTemplate.from_template("Переведи текст с английского на русский:\n\"{input_text}\"")
])

# Вариант 1 — format_messages (возвращает список сообщений/объектов для модели)
messages_list = chat_template.format_messages(input_text="Hello, world!")
print("format_messages result:", messages_list)

# Вариант 2 — invoke (возвращает объект ChatPromptValue со списком внутри него)
prompt_chatobj = chat_template.invoke({"input_text": "Hello, world!"})
print("invoke result:", prompt_chatobj)
print(type(prompt_chatobj))


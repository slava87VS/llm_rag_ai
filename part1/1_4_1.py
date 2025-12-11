import os
from re import split

from dotenv import load_dotenv

load_dotenv()

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# Создаём класс для CLI-бота
class CliBot():
    def __init__(self, model_name):
        # Создаём модель
        self.chat_model = ChatOpenAI(
            model_name=model_name,
            temperature=0
        )

        # Создаём Хранилище истории
        self.store = {}

        # Создаем шаблон промпта
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты полезный ассистент."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        # Создаём цепочку (тут используется синтаксис LCEL*)
        self.chain = self.prompt | self.chat_model

        # Создаём цепочку с историей
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,  # Цепочка с историей
            self.get_session_history,  # метод для получения истории
            input_messages_key="question",  # ключ для вопроса
            history_messages_key="history",  # ключ для истории
        )

    # Метод для получения истории по session_id
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def __call__(self, session_id):
        while True:
            try:
                user_text = input("Вы: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nБот: Завершение работы.")
                break
            if not user_text:
                continue

            msg = user_text.lower()
            if len(split(" ", msg)) > 200:
                print("Long message")


            if msg in ("выход", "стоп", "конец"):
                print("Бот: До свидания!")
                break
            if msg == "сброс":
                if session_id in self.store:
                    del self.store[session_id]
                print("Бот: Контекст диалога очищен.")
                continue

            responce = self.chain_with_history.invoke(
                {"question": user_text},
                {"configurable": {"session_id": session_id}}
            )
            print('Бот:', responce.content)


if __name__ == "__main__":
    bot = CliBot(os.getenv("OPENAI_API_MODEL", "gpt-5"))
    bot("user_123")
import json
import os
from datetime import datetime

import tiktoken
from dotenv import load_dotenv

load_dotenv()

import logging
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI


# Создаём класс для CLI-бота
class cli_bot():
    def __init__(self, model_name, system_prompt="Ты полезный ассистент."):
        # Загружаем FAQ и добавляем его в системный промпт
        faq_data = self.load_faq()
        faq_text = "\n".join([f"Вопрос: {item['q']}\nОтвет: {item['a']}" for item in faq_data])

        order_data = self.load_orders()
        order_list = []
        for order_id, details in order_data.items():
            status = details.get('status', 'неизвестно')
            if status == 'in_transit':
                info = f"в пути, доставка через {details.get('eta_days', '?')} дней, перевозчик: {details.get('carrier', 'не указан')}"
            elif status == 'delivered':
                info = f"доставлен {details.get('delivered_at', 'дата неизвестна')}"
            elif status == 'processing':
                info = f"в обработке: {details.get('note', 'нет дополнительной информации')}"
            else:
                info = f"статус: {status}"

            order_list.append(f"Заказ {order_id}: {info}")

        order_text = "\n".join(order_list)

        # Обновляем системный промпт с FAQ
        enhanced_system_prompt = f"""{system_prompt}

        Вот часто задаваемые вопросы и ответы (FAQ):
        {faq_text}

        Вот информация о заказах:
        {order_text}

        Если пользователь задает вопрос из FAQ, используй информацию из ответа. 
        Если пользователь спрашивает о статусе заказа, используй информацию о заказах выше.
        Если вопрос не из FAQ и не о заказах, ответь как обычно."""


        # Создаём модель
        self.chat_model = ChatOpenAI(
            model_name=model_name,
            temperature=0,
            request_timeout=15
        )

        # Создаём Хранилище истории
        self.store = {}

        # Создаем шаблон промпта с обновленным системным промптом
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", enhanced_system_prompt),  # Используем промпт с FAQ
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        # Создаём цепочку
        self.chain = self.prompt | self.chat_model

        # Создаём цепочку с историей
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain,  # Цепочка с историей
            self.get_session_history,  # метод для получения истории
            input_messages_key="question",  # ключ для вопроса
            history_messages_key="history",  # ключ для истории
        )

        # Настраиваем логирование в файл
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        logging.basicConfig(
            filename=f"logs/session_{timestamp}.jsonl", level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
            encoding="utf-8"
        )

    # Метод для загрузки orders
    def load_orders(self) -> json:
        """
        загружает файл orders
        :return: json
        """
        with open('C:\work\обучение\llm_rag\ecom-bot\data\orders.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_order_status(self, order_id):
        orders_data = self.load_orders()

        return orders_data[order_id]['status']


    # Метод для загрузки faq
    def load_faq(self)-> json:
        """
        загружает файл faq
        :return: json
        """
        with open('C:\\work\\обучение\\llm_rag\\ecom-bot\\data\\faq.json', 'r', encoding='utf-8') as f:
            return json.load(f)


    # Метод для получения истории по session_id
    def get_session_history(self, session_id: str):
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def __call__(self, session_id):
        print(
            "Чат-бот запущен! Можете задавать вопросы. \n - Для выхода введите 'выход'.\n - Для очистки контекста введите 'сброс'.\n")
        logging.info("=== New session ===")
        while True:
            try:
                user_text = input("Вы: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nБот: Завершение работы.")
                break
            if not user_text:
                continue

            logging.info(f"User: {user_text}")
            msg = user_text.lower()
            if msg in ("выход", "стоп", "конец"):
                print("Бот: До свидания!")
                logging.info("Пользователь завершил сессию. Сессия окончена.")
                break
            if msg == "сброс":
                if session_id in self.store:
                    del self.store[session_id]
                print("Бот: Контекст диалога очищен.")
                logging.info("Пользователь сбросил контекст.")
                continue

            if user_text.startswith("/order"):
                parts = user_text.split()
                if len(parts) == 2:
                    order_id = parts[1]
                    order_status = self.get_order_status(order_id)
                    response_text = order_status
                else:
                    response_text = "Пожалуйста, укажите номер заказа, например: /order 12345"

                print(f"Бот: {response_text}")
                logging.info(f"Bot: {response_text}")
                continue

            try:
                responce = self.chain_with_history.invoke(
                    {"question": user_text},
                    {"configurable": {"session_id": session_id}}
                )
            except Exception as e:
                # Логируем и выводим ошибку, продолжаем чат
                logging.error(f"[error] {e}")
                print(f"[Ошибка] {e}")
                continue

            # Форматируем и выводим ответ
            bot_reply = responce.content.strip()
            logging.info(f"Bot: {bot_reply}")
            print(f"Бот: {bot_reply}")


        # Логируем количество токенов
        usage = responce.usage_metadata
        if usage:
            usage.get('input_tokens')
            usage.get('output_tokens')
            usage.get('total_tokens')

            logging.info(f"Usage: {json.dumps(usage)}")
        else:
            print("Информация о токенах недоступна")

if __name__ == "__main__":
    model = os.getenv("OPENAI_API_MODEL", "gpt-5")


    bot = cli_bot(
        model_name=model
    )
    bot("user_123")
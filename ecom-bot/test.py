import json


def load_orders() -> json:
    """
    загружает файл orders
    :return: json
    """
    with open('C:\work\обучение\llm_rag\ecom-bot\data\orders.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def get_order_status(order_id):
    orders_data = load_orders()
    id = orders_data[order_id]['status']

    return id

print(get_order_status('12345'))
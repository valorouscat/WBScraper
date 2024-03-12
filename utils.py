import requests
from db import new_item
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

def get_info(item_id: str, user_id: str):
    url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={item_id}"
    response = requests.get(url)
    if response.status_code == 200:
        if response.json()['data']['products']:
            logger.info(f"Info successfully get for {item_id}")
            data = response.json()['data']['products'][0]
            item: dict = {}
            item['name'] = data['name']
            item['id'] = data['id']
            item['price'] = str(data['salePriceU'])[:-2]
            item['rating'] = data['rating']
            total_stocks = 0
            for i in data['sizes'][0]['stocks']:
                total_stocks += i['qty']
            item['stocks'] = total_stocks

            now = datetime.now().strftime("%H:%M:%S")
            new_item(user_id, now, item_id)
            
            return f"Название: {item['name']}\nАртикул: {item_id}\nЦена: {item['price']}\nРейтинг: {item['rating']}\nКоличество: {item['stocks']}"
    logger.warning(f"Failed to get info for {item_id}")
    return None
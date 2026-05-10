import sys
import asyncio
import logging
import re
import os

from funpaybotengine import Bot, Dispatcher
from funpaybotengine.types import OrderStatus

GOLDEN_KEY = ''

bot = Bot(golden_key=GOLDEN_KEY)
dp = Dispatcher()

def extract_account(order_title):
    match = re.search(r'Подарком,\s*(\S+)', order_title)
    if match:
        return match.group(1)
    
    parts = order_title.split(',')
    if len(parts) >= 5:
        return parts[-1].strip().rstrip('.')
    
    return None

async def get_chat_id_from_order(order_id):
    try:
        order_page = await bot.get_order_page(order_id)
        
        if hasattr(order_page, 'chat_id') and order_page.chat_id:
            return order_page.chat_id
        
        if hasattr(order_page, 'chat') and order_page.chat:
            if hasattr(order_page.chat, 'id'):
                return order_page.chat.id
        
        text = str(order_page)
        
        chat_match = re.search(r'data-chat="(\d+)"', text)
        if chat_match:
            return chat_match.group(1)
        
        node_match = re.search(r'node=(\d+)', text)
        if node_match:
            return node_match.group(1)
        
    except Exception as e:
        logging.error(f"Ошибка: {e}")
    return None

async def process_order(order, chat_id=None):
    order_id = order.id
    order_title = order.title
    
    account = extract_account(order_title)
    logging.info(f"Извлечен аккаунт: {account} из заказа {order_id}: {order_title}")
    
    if not chat_id:
        chat_id = await get_chat_id_from_order(order_id)
    
    if not chat_id:
        logging.error(f"chat_id не найден для {order_id}")
        return False
    
    if account:
        msg = f"Здравствуйте, подарок отправлен на аккаунт @{account}"
    else:
        msg = f"Здравствуйте, подарок отправлен!"
    
    await bot.send_message(chat_id=chat_id, text=msg)
    logging.info(f"Сообщение отправлено в чат {chat_id} для заказа {order_id}")
    
    return True

async def check_active_orders():
    logging.info("Ищу оплаченные заказы...")
    try:
        batch = await bot.get_sales()
        for order in batch.orders:
            if order.status == OrderStatus.PAID:
                logging.info(f"Нашел PAID: {order.id} - {order.title}")
                await process_order(order)
                await asyncio.sleep(1)
    except Exception as e:
        logging.error(f"Ошибка: {e}")

@dp.on_new_sale()
async def handle_new_sale(event):
    try:
        chat_id = event.message.chat_id
        order = await event.get_order_preview()
        logging.info(f"Новый заказ {order.id} - {order.title}")
        await process_order(order, chat_id)
    except Exception as e:
        logging.error(f"Ошибка: {e}")

async def main():
    await bot.update()
    await check_active_orders()
    logging.info("Бот онлайн.")
    await bot.listen_events(dp)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

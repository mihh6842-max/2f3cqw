"""
API для получения заявок с сайта и отправки в Telegram
Используйте этот файл для интеграции с веб-формой
"""

import requests
import json
from config import BOT_TOKEN, ADMIN_ID
from bot import save_order

def format_order_message(order):
    """Форматирование сообщения о заявке"""
    msg = "📋 <b>Новая заявка на обмен</b>\n\n"
    msg += f"🔹 <b>ID заявки:</b> <code>{order['id']}</code>\n"
    msg += f"🔹 <b>EXMO код:</b> <code>{order['exmoCode']}</code>\n"
    msg += f"🔹 <b>Сумма:</b> <code>{order['giveAmount']}</code> руб.\n"
    msg += f"🔹 <b>К получению:</b> <code>{order['receiveAmount']}</code> руб.\n\n"
    msg += "👤 <b>Данные клиента:</b>\n"
    msg += f"• ФИО: <code>{order['fullName']}</code>\n"
    msg += f"• Телефон: <code>{order['phone']}</code>\n"
    msg += f"• Банк: <code>{order['bank']}</code>\n\n"
    msg += f"⏰ Дата: <code>{order['createdAt']}</code>"
    return msg

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_order_notification(order_data):
    """
    Отправка уведомления о новой заявке в Telegram

    Args:
        order_data (dict): Данные заявки

    Returns:
        bool: True если успешно отправлено
    """

    if not ADMIN_ID:
        print("WARNING: ADMIN_ID not set in config.py")
        return False

    # Сохраняем заявку в БД
    save_order(order_data)

    # Форматируем сообщение
    message = format_order_message(order_data)

    # Отправляем в Telegram
    url = f"{API_URL}/sendMessage"
    data = {
        'chat_id': ADMIN_ID,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()

        if result.get('ok'):
            print(f"[OK] Notification sent for order #{order_data['id']}")
            return True
        else:
            print(f"[ERROR] Send failed: {result.get('description')}")
            return False

    except Exception as e:
        print(f"[ERROR] Exception: {e}")
        return False

# Пример использования
if __name__ == '__main__':
    # Тестовая заявка
    test_order = {
        'id': 1,
        'type': 'sell',
        'exmoCode': 'TEST-1234-5678-9ABC',
        'giveAmount': 5000,
        'receiveAmount': 5000,
        'fullName': 'Иванов Иван Иванович',
        'phone': '+7 (999) 123-45-67',
        'bank': 'Сбербанк',
        'status': 'pending',
        'createdAt': '2026-01-13T12:00:00.000Z'
    }

    send_order_notification(test_order)

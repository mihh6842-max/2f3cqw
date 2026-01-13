"""
Обработчик фото для Telegram бота
Добавляет возможность отправки скриншотов с заявками
"""

import requests
import base64
import os
from config import BOT_TOKEN

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_photo_with_caption(chat_id, photo_path, caption, parse_mode='HTML'):
    """
    Отправка фото с подписью в Telegram

    Args:
        chat_id: ID чата
        photo_path: Путь к фото или base64 строка
        caption: Подпись под фото
        parse_mode: Режим форматирования

    Returns:
        dict: Ответ от Telegram API
    """

    url = f"{API_URL}/sendPhoto"

    # Проверяем, это файл или base64
    if os.path.exists(photo_path):
        # Отправляем файл
        with open(photo_path, 'rb') as photo:
            files = {'photo': photo}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, files=files)
    else:
        # Пробуем декодировать base64
        try:
            # Убираем префикс data:image/...;base64,
            if ',' in photo_path:
                photo_path = photo_path.split(',', 1)[1]

            photo_bytes = base64.b64decode(photo_path)

            files = {'photo': ('screenshot.jpg', photo_bytes, 'image/jpeg')}
            data = {
                'chat_id': chat_id,
                'caption': caption,
                'parse_mode': parse_mode
            }
            response = requests.post(url, data=data, files=files)
        except Exception as e:
            print(f"[ERROR] Failed to decode/send photo: {e}")
            return {'ok': False, 'description': str(e)}

    return response.json()

def send_order_with_photo(chat_id, order_data, photo_data=None):
    """
    Отправка заявки с фото (если есть)

    Args:
        chat_id: ID чата
        order_data: Данные заявки
        photo_data: Путь к фото или base64 строка

    Returns:
        bool: True если успешно отправлено
    """

    # Форматируем сообщение
    caption = (
        f"📋 <b>Новая заявка #{order_data['id']}</b>\n\n"
        f"💳 <b>EXMO код:</b> <code>{order_data['exmoCode']}</code>\n"
        f"💰 <b>Сумма:</b> {order_data['giveAmount']} ₽\n\n"
        f"👤 <b>Клиент:</b> {order_data['fullName']}\n"
        f"📱 {order_data['phone']}\n"
        f"🏦 {order_data['bank']}\n\n"
        f"⏰ {order_data['createdAt'][:19]}"
    )

    if photo_data:
        # Отправляем с фото
        result = send_photo_with_caption(chat_id, photo_data, caption)
    else:
        # Отправляем только текст
        url = f"{API_URL}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': caption,
            'parse_mode': 'HTML'
        }
        response = requests.post(url, data=data)
        result = response.json()

    return result.get('ok', False)

# Пример использования
if __name__ == '__main__':
    from config import ADMIN_ID

    # Тестовая заявка
    test_order = {
        'id': 999,
        'exmoCode': 'TEST-1234-5678',
        'giveAmount': 5000,
        'receiveAmount': 5000,
        'fullName': 'Тест Тестович',
        'phone': '+7 999 123-45-67',
        'bank': 'Тинькофф',
        'createdAt': '2026-01-13T12:00:00'
    }

    # Отправка без фото
    success = send_order_with_photo(ADMIN_ID, test_order)
    print(f"Test {'passed' if success else 'failed'}")

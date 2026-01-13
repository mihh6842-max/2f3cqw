import requests
import json
import time
import os
from datetime import datetime
from config import BOT_TOKEN, ADMIN_ID, DB_PATH

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def load_orders():
    """Загрузка заявок из БД"""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_order(order):
    """Сохранение заявки в БД"""
    orders = load_orders()
    orders.append(order)
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def send_message(chat_id, text, parse_mode='HTML'):
    """Отправка сообщения через Telegram API"""
    url = f"{API_URL}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode
    }
    response = requests.post(url, data=data)
    return response.json()

def get_updates(offset=None):
    """Получение обновлений (long polling)"""
    url = f"{API_URL}/getUpdates"
    params = {'timeout': 30, 'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

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

def format_order_detail(order):
    """Детальное форматирование заявки"""
    status_icons = {
        'pending': '🟡',
        'processing': '🔵',
        'completed': '🟢',
        'rejected': '🔴'
    }

    status = order.get('status', 'pending')
    icon = status_icons.get(status, '⚪')

    msg = f"{icon} <b>Заявка #{order['id']}</b>\n"
    msg += f"━━━━━━━━━━━━━━━━━━\n\n"

    msg += "💳 <b>Данные кода:</b>\n"
    msg += f"• Код: <code>{order['exmoCode']}</code>\n"
    msg += f"• Сумма: <code>{order['giveAmount']} ₽</code>\n"
    msg += f"• К выплате: <code>{order['receiveAmount']} ₽</code>\n\n"

    msg += "👤 <b>Клиент:</b>\n"
    msg += f"• ФИО: <code>{order['fullName']}</code>\n"
    msg += f"• 📱 Телефон: <code>{order['phone']}</code>\n"
    msg += f"• 🏦 Банк: <code>{order['bank']}</code>\n\n"

    msg += f"📅 Создана: <code>{order['createdAt'][:19]}</code>\n"
    msg += f"📊 Статус: <b>{status.upper()}</b>\n"

    return msg

def send_keyboard(chat_id, text, buttons, parse_mode='HTML'):
    """Отправка сообщения с кнопками"""
    url = f"{API_URL}/sendMessage"

    keyboard = {'inline_keyboard': buttons}

    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': parse_mode,
        'reply_markup': json.dumps(keyboard)
    }

    response = requests.post(url, data=data)
    return response.json()

def answer_callback(callback_id, text=''):
    """Ответ на callback query"""
    url = f"{API_URL}/answerCallbackQuery"
    data = {'callback_query_id': callback_id, 'text': text}
    requests.post(url, data=data)

def handle_message(message):
    """Обработка входящих сообщений"""
    chat_id = message['chat']['id']
    text = message.get('text', '')

    if text == '/start':
        response = (
            "🤖 <b>EXMO Обменник - Telegram бот</b>\n\n"
            "📋 Команды:\n"
            "• /orders - Список заявок\n"
            "• /start - Информация\n\n"
            f"🆔 Ваш ID: <code>{chat_id}</code>"
        )
        send_message(chat_id, response)

    elif text == '/orders':
        orders = load_orders()
        if not orders:
            send_message(chat_id, "📭 Заявок пока нет")
        else:
            # Создаем кнопки для каждой заявки
            buttons = []
            msg = f"📋 <b>Заявки ({len(orders)} шт.)</b>\n\n"

            for order in orders[-10:]:  # Последние 10
                status_icon = {
                    'pending': '🟡',
                    'processing': '🔵',
                    'completed': '🟢',
                    'rejected': '🔴'
                }.get(order.get('status', 'pending'), '⚪')

                msg += f"{status_icon} #{order['id']} - {order['fullName'][:20]} - {order['giveAmount']} ₽\n"

                # Кнопка для просмотра заявки
                buttons.append([{
                    'text': f"📄 Заявка #{order['id']}",
                    'callback_data': f"view_{order['id']}"
                }])

            send_keyboard(chat_id, msg, buttons)

    else:
        send_message(chat_id, "Используйте команды:\n/start - Начать\n/orders - Список заявок")

def handle_callback(callback_query):
    """Обработка нажатий на кнопки"""
    chat_id = callback_query['message']['chat']['id']
    callback_id = callback_query['id']
    data = callback_query['data']

    if data.startswith('view_'):
        order_id = int(data.split('_')[1])
        orders = load_orders()

        # Находим заявку
        order = next((o for o in orders if o['id'] == order_id), None)

        if order:
            # Форматируем детальное сообщение
            msg = format_order_detail(order)

            # Кнопки для действий
            buttons = [
                [
                    {'text': '✅ Выполнена', 'callback_data': f'complete_{order_id}'},
                    {'text': '❌ Отклонена', 'callback_data': f'reject_{order_id}'}
                ],
                [{'text': '🔙 Назад к списку', 'callback_data': 'back_orders'}]
            ]

            send_keyboard(chat_id, msg, buttons)
            answer_callback(callback_id, '✓')
        else:
            answer_callback(callback_id, 'Заявка не найдена')

    elif data == 'back_orders':
        # Возвращаемся к списку
        orders = load_orders()
        buttons = []
        msg = f"📋 <b>Заявки ({len(orders)} шт.)</b>\n\n"

        for order in orders[-10:]:
            status_icon = {
                'pending': '🟡',
                'processing': '🔵',
                'completed': '🟢',
                'rejected': '🔴'
            }.get(order.get('status', 'pending'), '⚪')

            msg += f"{status_icon} #{order['id']} - {order['fullName'][:20]} - {order['giveAmount']} ₽\n"

            buttons.append([{
                'text': f"📄 Заявка #{order['id']}",
                'callback_data': f"view_{order['id']}"
            }])

        send_keyboard(chat_id, msg, buttons)
        answer_callback(callback_id, '✓')

    elif data.startswith('complete_') or data.startswith('reject_'):
        action = 'completed' if data.startswith('complete_') else 'rejected'
        order_id = int(data.split('_')[1])

        orders = load_orders()
        for order in orders:
            if order['id'] == order_id:
                order['status'] = action
                break

        # Сохраняем изменения
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(orders, f, ensure_ascii=False, indent=2)

        status_text = 'выполнена ✅' if action == 'completed' else 'отклонена ❌'
        answer_callback(callback_id, f'Заявка #{order_id} {status_text}')

        # Обновляем сообщение
        order = next((o for o in orders if o['id'] == order_id), None)
        if order:
            msg = format_order_detail(order)
            buttons = [[{'text': '🔙 Назад к списку', 'callback_data': 'back_orders'}]]
            send_keyboard(chat_id, msg, buttons)

def main():
    """Основной цикл бота"""
    print("Bot started...")
    offset = None

    # Проверка токена
    response = requests.get(f"{API_URL}/getMe")
    if response.json().get('ok'):
        bot_info = response.json()['result']
        print(f"Connected as: @{bot_info['username']}")
    else:
        print("Error connecting to Telegram API")
        return

    while True:
        try:
            updates = get_updates(offset)

            if updates.get('ok'):
                for update in updates.get('result', []):
                    offset = update['update_id'] + 1

                    if 'message' in update:
                        handle_message(update['message'])

                    elif 'callback_query' in update:
                        handle_callback(update['callback_query'])

            time.sleep(1)

        except KeyboardInterrupt:
            print("\nBot stopped")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()

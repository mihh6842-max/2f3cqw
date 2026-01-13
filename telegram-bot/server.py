"""
API сервер для приёма заявок с сайта
Запуск: python server.py
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
from datetime import datetime
from config import BOT_TOKEN, ADMIN_IDS, DB_PATH

app = Flask(__name__)
CORS(app)  # Разрешаем запросы с любого домена

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def load_orders():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

@app.route('/api/order', methods=['POST'])
def create_order():
    """Создание новой заявки"""
    try:
        data = request.json
        orders = load_orders()

        # Генерируем ID
        new_id = max([o.get('id', 0) for o in orders], default=0) + 1

        order = {
            'id': new_id,
            'type': 'sell',
            'exmoCode': data.get('exmoCode', ''),
            'giveAmount': data.get('giveAmount', 0),
            'receiveAmount': data.get('receiveAmount', 0),
            'fullName': data.get('fullName', ''),
            'phone': data.get('phone', ''),
            'bank': data.get('bank', ''),
            'status': 'pending',
            'createdAt': datetime.now().isoformat()
        }

        orders.append(order)
        save_orders(orders)

        # Отправляем в Telegram всем админам
        message = (
            f"📋 <b>Новая заявка #{order['id']}</b>\n\n"
            f"💳 <code>{order['exmoCode']}</code>\n"
            f"💰 {order['giveAmount']} руб.\n\n"
            f"👤 <code>{order['fullName']}</code>\n"
            f"📱 <code>{order['phone']}</code>\n"
            f"🏦 <code>{order['bank']}</code>"
        )

        for admin_id in ADMIN_IDS:
            requests.post(f"{API_URL}/sendMessage", data={
                'chat_id': admin_id,
                'text': message,
                'parse_mode': 'HTML'
            })

        return jsonify({'success': True, 'id': new_id})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Получение списка заявок"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    orders = load_orders()
    orders.reverse()  # Новые сверху

    total = len(orders)
    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        'orders': orders[start:end],
        'total': total,
        'page': page,
        'pages': (total + per_page - 1) // per_page
    })

@app.route('/api/order/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Получение одной заявки"""
    orders = load_orders()
    order = next((o for o in orders if o['id'] == order_id), None)

    if order:
        return jsonify(order)
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/order/<int:order_id>/status', methods=['PUT'])
def update_status(order_id):
    """Обновление статуса заявки"""
    data = request.json
    new_status = data.get('status')

    orders = load_orders()
    for order in orders:
        if order['id'] == order_id:
            order['status'] = new_status
            save_orders(orders)
            return jsonify({'success': True})

    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    print("🚀 API сервер запущен на http://localhost:5000")
    print("📋 Эндпоинты:")
    print("   POST /api/order - создать заявку")
    print("   GET  /api/orders - список заявок")
    print("   GET  /api/order/<id> - одна заявка")
    app.run(host='0.0.0.0', port=5000, debug=True)

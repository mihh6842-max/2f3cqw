"""
Тестовый скрипт для проверки работы бота
"""

from api import send_order_notification
from datetime import datetime

def test_notification():
    """Отправка тестового уведомления"""

    test_order = {
        'id': 999,
        'type': 'sell',
        'exmoCode': 'TEST-ABCD-1234-EFGH-5678',
        'giveAmount': 10000,
        'receiveAmount': 10000,
        'fullName': 'Тестов Тест Тестович',
        'phone': '+7 (999) 888-77-66',
        'bank': 'Тинькофф',
        'status': 'pending',
        'createdAt': datetime.now().isoformat()
    }

    print("Отправка тестовой заявки...")
    print(f"ID: {test_order['id']}")
    print(f"Код: {test_order['exmoCode']}")
    print(f"Сумма: {test_order['giveAmount']} руб.")
    print(f"Клиент: {test_order['fullName']}")
    print()

    result = send_order_notification(test_order)

    if result:
        print("[SUCCESS] Test passed!")
        print("Check your Telegram - notification should arrive")
    else:
        print("[FAIL] Send error")
        print("Check:")
        print("1. ADMIN_ID in config.py")
        print("2. Bot token")
        print("3. Internet connection")

if __name__ == '__main__':
    test_notification()

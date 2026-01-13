# Telegram бот для EXMO обменника

Бот для получения уведомлений о новых заявках на обмен EXMO кодов.

## Установка

1. Установите Python 3.7+

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте конфигурацию в `config.py`:
```python
BOT_TOKEN = "ваш_токен"
ADMIN_ID = ваш_telegram_id
```

## Получение Telegram ID

1. Запустите бота
2. Найдите бота в Telegram
3. Отправьте команду `/start`
4. Скопируйте ваш ID из ответа
5. Укажите ID в `config.py`

## Запуск бота

### Локально:
```bash
python bot.py
```

### На хостинге (Linux):
```bash
nohup python3 bot.py > bot.log 2>&1 &
```

### С systemd (Linux):
Создайте файл `/etc/systemd/system/exmo-bot.service`:
```ini
[Unit]
Description=EXMO Telegram Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/telegram-bot
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Запуск:
```bash
sudo systemctl enable exmo-bot
sudo systemctl start exmo-bot
sudo systemctl status exmo-bot
```

## Команды бота

- `/start` - Начать работу, получить Telegram ID
- `/orders` - Показать последние 5 заявок

## Интеграция с сайтом

### Вариант 1: Прямая отправка из JavaScript

```javascript
// В файле sell.html
const orderData = {
    id: orders.length + 1,
    type: 'sell',
    exmoCode: document.getElementById('exmoCode').value,
    giveAmount: giveAmount,
    receiveAmount: giveAmount,
    fullName: document.getElementById('fullName').value,
    phone: document.getElementById('phone').value,
    bank: document.getElementById('bank').value,
    status: 'pending',
    createdAt: new Date().toISOString()
};

// Отправка в Telegram
fetch('https://api.telegram.org/bot8378403510:AAHdYIpQ2hRJ8H0va6kM-ZSfoYwVeosuQVA/sendMessage', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        chat_id: 'ваш_telegram_id',
        text: formatOrderMessage(orderData),
        parse_mode: 'HTML'
    })
});
```

### Вариант 2: Через бэкенд API (рекомендуется)

Используйте `api.py` из папки бота:

```python
from api import send_order_notification

order_data = {
    'id': 1,
    'exmoCode': 'код',
    'giveAmount': 5000,
    # ... остальные поля
}

send_order_notification(order_data)
```

## База данных

Все заявки сохраняются в `data/orders.json`

Структура:
```json
[
  {
    "id": 1,
    "type": "sell",
    "exmoCode": "TEST-1234",
    "giveAmount": 5000,
    "receiveAmount": 5000,
    "fullName": "Иван Иванов",
    "phone": "+7 999 123-45-67",
    "bank": "Сбербанк",
    "status": "pending",
    "createdAt": "2026-01-13T12:00:00.000Z"
  }
]
```

## Тестирование

Запустите тестовую отправку:
```bash
python api.py
```

## Безопасность

⚠️ **Важно:**
- Не публикуйте токен бота в открытом доступе
- Добавьте `config.py` в `.gitignore`
- На хостинге используйте переменные окружения

## Хостинг

### PythonAnywhere
1. Загрузите файлы
2. Установите зависимости
3. Запустите через Always-on task

### Heroku
1. Создайте `Procfile`:
```
worker: python bot.py
```
2. Деплой через Git

### VPS (Ubuntu)
```bash
cd /var/www/telegram-bot
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
nohup python bot.py &
```

## Поддержка

При проблемах проверьте:
- Корректность токена
- Наличие ADMIN_ID
- Подключение к интернету
- Логи: `tail -f bot.log`

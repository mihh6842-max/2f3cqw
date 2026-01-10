<?php
require_once 'db.php';

if (!isset($_SESSION['user_id'])) {
    header('Location: login.html');
    exit;
}
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Продать ключ - EXMO Маркетплейс</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <video autoplay muted loop playsinline class="video-background">
        <source src="19264a464315513c06c2dc242649e340.mp4" type="video/mp4">
    </video>

    <header>
        <div class="main-header">
            <div class="container">
                <div class="header-content">
                    <div class="logo">
                        <h1>EXMO МАРКЕТПЛЕЙС</h1>
                    </div>
                    <nav>
                        <a href="shop.php">Магазин</a>
                        <a href="sell.php">Продать</a>
                    </nav>
                    <div class="user-menu">
                        <span class="user-email">👤 <?php echo htmlspecialchars($_SESSION['user_email']); ?></span>
                        <a href="logout.php" class="btn-logout">Выйти</a>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main>
        <section class="exchange-section">
            <div class="container">
                <h2 class="main-title">Продать EXMO код</h2>

                <form id="sellForm" class="exchange-form">
                    <div class="form-group">
                        <label for="title">Название товара *</label>
                        <input type="text" id="title" name="title" required
                               placeholder="Например: EXMO код 5000₽">
                    </div>

                    <div class="form-group">
                        <label for="description">Краткое описание</label>
                        <textarea id="description" name="description" rows="3"
                                  placeholder="Опишите ваш товар"></textarea>
                    </div>

                    <div class="form-group">
                        <label for="exmo_code">EXMO код *</label>
                        <input type="text" id="exmo_code" name="exmo_code" required
                               placeholder="Вставьте ваш EXMO код">
                    </div>

                    <div class="form-group">
                        <label for="price">Цена (₽) *</label>
                        <input type="number" id="price" name="price" required
                               placeholder="Укажите цену" min="100" step="0.01">
                    </div>

                    <div class="form-group">
                        <label for="payment_phone">Номер телефона для СБП *</label>
                        <input type="tel" id="payment_phone" name="payment_phone" required
                               placeholder="+7 (___) ___-__-__">
                    </div>

                    <div class="form-group">
                        <label for="payment_bank">Банк для перевода *</label>
                        <select id="payment_bank" name="payment_bank" required>
                            <option value="">Выберите банк</option>
                            <option value="Сбербанк">Сбербанк</option>
                            <option value="Тинькофф">Тинькофф</option>
                            <option value="ВТБ">ВТБ</option>
                            <option value="Альфа-Банк">Альфа-Банк</option>
                            <option value="Райффайзен">Райффайзен</option>
                            <option value="Газпромбанк">Газпромбанк</option>
                            <option value="Открытие">Открытие</option>
                            <option value="Росбанк">Росбанк</option>
                            <option value="Другой">Другой</option>
                        </select>
                    </div>

                    <button type="submit" class="btn-submit">Выставить на продажу</button>
                </form>

                <div id="successMessage" class="message success" style="display:none;">
                    ✓ Товар успешно добавлен в магазин!
                </div>
                <div id="errorMessage" class="message error" style="display:none;">
                    ✗ Ошибка добавления товара
                </div>
            </div>
        </section>
    </main>

    <script>
        const phoneInput = document.getElementById('payment_phone');
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 0) {
                if (value[0] === '8') value = '7' + value.substring(1);
                if (value[0] !== '7') value = '7' + value;
            }
            let formatted = '+7';
            if (value.length > 1) formatted += ' (' + value.substring(1, 4);
            if (value.length >= 5) formatted += ') ' + value.substring(4, 7);
            if (value.length >= 8) formatted += '-' + value.substring(7, 9);
            if (value.length >= 10) formatted += '-' + value.substring(9, 11);
            e.target.value = formatted;
        });

        document.getElementById('sellForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const successMessage = document.getElementById('successMessage');
            const errorMessage = document.getElementById('errorMessage');

            successMessage.style.display = 'none';
            errorMessage.style.display = 'none';

            try {
                const response = await fetch('sell_process.php', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();

                if (result.success) {
                    successMessage.style.display = 'block';
                    this.reset();
                    setTimeout(() => {
                        window.location.href = 'shop.php';
                    }, 2000);
                } else {
                    errorMessage.textContent = '✗ ' + (result.message || 'Ошибка добавления товара');
                    errorMessage.style.display = 'block';
                }
            } catch (error) {
                errorMessage.style.display = 'block';
            }
        });
    </script>
</body>
</html>

<?php
require_once 'db.php';

if (!isset($_SESSION['user_id'])) {
    header('Location: login.html');
    exit;
}

$stmt = $pdo->prepare("SELECT p.*, u.phone as seller_phone FROM products p JOIN users u ON p.seller_id = u.id WHERE p.status = 'active' ORDER BY p.created_at DESC");
$stmt->execute();
$products = $stmt->fetchAll();
?>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Магазин EXMO кодов</title>
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
                        <a href="#cart" onclick="toggleCart()">🛒 Корзина (<span id="cartCount">0</span>)</a>
                    </nav>
                    <div class="user-menu">
                        <span class="user-email">👤 <?php echo htmlspecialchars($_SESSION['user_email']); ?></span>
                        <a href="sell.php" class="btn-sell">Продать</a>
                        <a href="logout.php" class="btn-logout">Выйти</a>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <main>
        <section class="shop-section">
            <div class="container">
                <h2 class="main-title">Доступные EXMO коды</h2>

                <div class="products-grid">
                    <?php if (empty($products)): ?>
                        <div class="no-products">
                            <p>Пока нет доступных товаров</p>
                            <a href="sell.php" class="btn-submit">Продать первый ключ</a>
                        </div>
                    <?php else: ?>
                        <?php foreach ($products as $product): ?>
                            <div class="product-card">
                                <div class="product-header">
                                    <h3><?php echo htmlspecialchars($product['title']); ?></h3>
                                    <span class="product-price"><?php echo number_format($product['price'], 0, '', ' '); ?> ₽</span>
                                </div>
                                <p class="product-description"><?php echo htmlspecialchars($product['description']); ?></p>
                                <div class="product-info">
                                    <small>Продавец: <?php echo htmlspecialchars($product['seller_phone']); ?></small>
                                    <small>Добавлено: <?php echo date('d.m.Y H:i', strtotime($product['created_at'])); ?></small>
                                </div>
                                <button class="btn-add-cart" onclick="addToCart(<?php echo $product['id']; ?>, '<?php echo htmlspecialchars($product['title']); ?>', <?php echo $product['price']; ?>)">
                                    Добавить в корзину
                                </button>
                            </div>
                        <?php endforeach; ?>
                    <?php endif; ?>
                </div>
            </div>
        </section>
    </main>

    <aside class="cart-panel" id="cartPanel">
        <button class="close-auth" onclick="toggleCart()">✕</button>
        <h3>Корзина</h3>
        <div id="cartItems"></div>
        <div class="cart-total">
            <strong>Итого: <span id="cartTotal">0</span> ₽</strong>
        </div>
        <button class="btn-submit-auth" onclick="checkout()">Оформить заказ</button>
    </aside>

    <script src="shop.js"></script>
</body>
</html>

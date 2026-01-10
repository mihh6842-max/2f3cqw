<?php
require_once 'db.php';

header('Content-Type: application/json');

if (!isset($_SESSION['user_id'])) {
    echo json_encode(['success' => false, 'message' => 'Необходима авторизация']);
    exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$products = $input['products'] ?? [];

if (empty($products)) {
    echo json_encode(['success' => false, 'message' => 'Корзина пуста']);
    exit;
}

try {
    $pdo->beginTransaction();

    foreach ($products as $product) {
        $stmt = $pdo->prepare("SELECT id, status FROM products WHERE id = ? AND status = 'active'");
        $stmt->execute([$product['id']]);
        $dbProduct = $stmt->fetch();

        if (!$dbProduct) {
            $pdo->rollBack();
            echo json_encode(['success' => false, 'message' => 'Один из товаров уже продан или недоступен']);
            exit;
        }

        $stmt = $pdo->prepare("INSERT INTO orders (buyer_id, product_id, status) VALUES (?, ?, 'pending')");
        $stmt->execute([$_SESSION['user_id'], $product['id']]);

        $stmt = $pdo->prepare("UPDATE products SET status = 'sold', sold_at = NOW() WHERE id = ?");
        $stmt->execute([$product['id']]);
    }

    $pdo->commit();

    echo json_encode(['success' => true, 'message' => 'Заказ успешно оформлен']);

} catch(PDOException $e) {
    $pdo->rollBack();
    echo json_encode(['success' => false, 'message' => 'Ошибка оформления заказа']);
}
?>

<?php
require_once 'db.php';

header('Content-Type: application/json');

if (!isset($_SESSION['user_id'])) {
    echo json_encode(['success' => false, 'message' => 'Необходима авторизация']);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Неверный метод запроса']);
    exit;
}

$title = trim($_POST['title'] ?? '');
$description = trim($_POST['description'] ?? '');
$exmoCode = trim($_POST['exmo_code'] ?? '');
$price = floatval($_POST['price'] ?? 0);
$paymentPhone = trim($_POST['payment_phone'] ?? '');
$paymentBank = trim($_POST['payment_bank'] ?? '');

if (empty($title) || empty($exmoCode) || $price <= 0 || empty($paymentPhone) || empty($paymentBank)) {
    echo json_encode(['success' => false, 'message' => 'Все обязательные поля должны быть заполнены']);
    exit;
}

try {
    $stmt = $pdo->prepare("INSERT INTO products (seller_id, title, description, exmo_code, price, payment_phone, payment_bank) VALUES (?, ?, ?, ?, ?, ?, ?)");
    $stmt->execute([$_SESSION['user_id'], $title, $description, $exmoCode, $price, $paymentPhone, $paymentBank]);

    echo json_encode(['success' => true, 'message' => 'Товар успешно добавлен']);

} catch(PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Ошибка базы данных']);
}
?>

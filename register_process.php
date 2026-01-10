<?php
require_once 'db.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Неверный метод запроса']);
    exit;
}

$phone = trim($_POST['phone'] ?? '');
$email = trim($_POST['email'] ?? '');
$password = trim($_POST['password'] ?? '');

if (empty($phone) || empty($email) || empty($password)) {
    echo json_encode(['success' => false, 'message' => 'Все поля обязательны']);
    exit;
}

if (strlen($password) < 6) {
    echo json_encode(['success' => false, 'message' => 'Пароль должен содержать минимум 6 символов']);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode(['success' => false, 'message' => 'Неверный формат email']);
    exit;
}

try {
    $stmt = $pdo->prepare("SELECT id FROM users WHERE phone = ? OR email = ?");
    $stmt->execute([$phone, $email]);

    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'message' => 'Пользователь с таким телефоном или email уже существует']);
        exit;
    }

    $passwordHash = password_hash($password, PASSWORD_DEFAULT);

    $stmt = $pdo->prepare("INSERT INTO users (phone, email, password_hash) VALUES (?, ?, ?)");
    $stmt->execute([$phone, $email, $passwordHash]);

    echo json_encode(['success' => true, 'message' => 'Регистрация успешна! Перенаправление...']);

} catch(PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Ошибка базы данных: ' . $e->getMessage()]);
}
?>

<?php
require_once 'db.php';

$phone = '+7 (000) 000-00-00';
$email = 'admin@admin.com';
$password = 'admin';

$passwordHash = password_hash($password, PASSWORD_DEFAULT);

try {
    $stmt = $pdo->prepare("SELECT id FROM users WHERE email = ?");
    $stmt->execute([$email]);

    if ($stmt->fetch()) {
        echo "Админ уже существует<br>";
    } else {
        $stmt = $pdo->prepare("INSERT INTO users (phone, email, password_hash) VALUES (?, ?, ?)");
        $stmt->execute([$phone, $email, $passwordHash]);
        echo "✓ Тестовый аккаунт создан<br>";
        echo "Email: admin<br>";
        echo "Пароль: admin<br>";
    }
} catch(PDOException $e) {
    echo "Ошибка: " . $e->getMessage();
}
?>

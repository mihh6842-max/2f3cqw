<?php
require_once 'config.php';

header('Content-Type: application/json');

$botToken = BOT_TOKEN;
$chatId = CHAT_ID;

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    echo json_encode(['success' => false, 'message' => 'Неверный метод запроса']);
    exit;
}

$exmoCode = trim($_POST['exmoCode'] ?? '');
$amount = trim($_POST['amount'] ?? '');
$phone = trim($_POST['phone'] ?? '');
$bank = trim($_POST['bank'] ?? '');
$exmoId = trim($_POST['exmoId'] ?? '');
$email = trim($_POST['email'] ?? '');

if (empty($exmoCode) || empty($amount) || empty($phone) || empty($bank) || empty($exmoId)) {
    echo json_encode(['success' => false, 'message' => 'Все обязательные поля должны быть заполнены']);
    exit;
}

if (!isset($_FILES['screenshot']) || $_FILES['screenshot']['error'] !== UPLOAD_ERR_OK) {
    echo json_encode(['success' => false, 'message' => 'Необходимо загрузить скриншот']);
    exit;
}

$uploadDir = 'uploads/';
if (!is_dir($uploadDir)) {
    mkdir($uploadDir, 0755, true);
}

$fileExtension = pathinfo($_FILES['screenshot']['name'], PATHINFO_EXTENSION);
$allowedExtensions = ['jpg', 'jpeg', 'png', 'gif'];

if (!in_array(strtolower($fileExtension), $allowedExtensions)) {
    echo json_encode(['success' => false, 'message' => 'Недопустимый формат файла']);
    exit;
}

$fileName = uniqid('screenshot_') . '.' . $fileExtension;
$filePath = $uploadDir . $fileName;

if (!move_uploaded_file($_FILES['screenshot']['tmp_name'], $filePath)) {
    echo json_encode(['success' => false, 'message' => 'Ошибка загрузки файла']);
    exit;
}

$message = "🆕 Новая заявка на обмен EXMO кода\n\n";
$message .= "💰 Сумма: " . htmlspecialchars($amount) . " ₽\n";
$message .= "🔑 EXMO код: " . htmlspecialchars($exmoCode) . "\n";
$message .= "📱 Телефон (СБП): " . htmlspecialchars($phone) . "\n";
$message .= "🏦 Банк: " . htmlspecialchars($bank) . "\n";
$message .= "🆔 ID на бирже: " . htmlspecialchars($exmoId) . "\n";

if (!empty($email)) {
    $message .= "📧 Email: " . htmlspecialchars($email) . "\n";
}

$message .= "\n📸 Скриншот прикреплен";

$telegramApiUrl = "https://api.telegram.org/bot{$botToken}/sendPhoto";

$postData = [
    'chat_id' => $chatId,
    'photo' => new CURLFile(realpath($filePath)),
    'caption' => $message,
    'parse_mode' => 'HTML'
];

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $telegramApiUrl);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    echo json_encode(['success' => true, 'message' => 'Заявка успешно отправлена']);
} else {
    echo json_encode(['success' => false, 'message' => 'Ошибка отправки в Telegram']);
}
?>

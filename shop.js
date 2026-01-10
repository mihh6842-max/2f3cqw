let cart = JSON.parse(localStorage.getItem('cart')) || [];

function updateCartCount() {
    document.getElementById('cartCount').textContent = cart.length;
}

function updateCartDisplay() {
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');

    if (cart.length === 0) {
        cartItems.innerHTML = '<p style="color: rgb(180,180,180); text-align: center; padding: 20px;">Корзина пуста</p>';
        cartTotal.textContent = '0';
        return;
    }

    let total = 0;
    let html = '<div class="cart-items-list">';

    cart.forEach((item, index) => {
        total += item.price;
        html += `
            <div class="cart-item">
                <div class="cart-item-info">
                    <strong>${item.title}</strong>
                    <span>${item.price.toLocaleString('ru-RU')} ₽</span>
                </div>
                <button class="btn-remove-cart" onclick="removeFromCart(${index})">✕</button>
            </div>
        `;
    });

    html += '</div>';
    cartItems.innerHTML = html;
    cartTotal.textContent = total.toLocaleString('ru-RU');
}

function addToCart(productId, title, price) {
    const exists = cart.find(item => item.id === productId);

    if (exists) {
        alert('Этот товар уже в корзине');
        return;
    }

    cart.push({ id: productId, title: title, price: price });
    localStorage.setItem('cart', JSON.stringify(cart));

    updateCartCount();
    updateCartDisplay();

    const message = document.createElement('div');
    message.className = 'cart-notification';
    message.textContent = '✓ Добавлено в корзину';
    document.body.appendChild(message);

    setTimeout(() => {
        message.remove();
    }, 2000);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));

    updateCartCount();
    updateCartDisplay();
}

function toggleCart() {
    const cartPanel = document.getElementById('cartPanel');
    cartPanel.classList.toggle('active');
    updateCartDisplay();
}

async function checkout() {
    if (cart.length === 0) {
        alert('Корзина пуста');
        return;
    }

    const currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
    if (!currentUser) {
        alert('Необходима авторизация');
        window.location.href = 'login.html';
        return;
    }

    // Получаем товары и обновляем их статус
    let products = JSON.parse(localStorage.getItem('products') || '[]');

    cart.forEach(cartItem => {
        const productIndex = products.findIndex(p => p.id === cartItem.id);
        if (productIndex !== -1) {
            products[productIndex].status = 'sold';
            products[productIndex].soldAt = new Date().toISOString();
        }
    });

    localStorage.setItem('products', JSON.stringify(products));

    // Сохраняем заказ
    let orders = JSON.parse(localStorage.getItem('orders') || '[]');
    const newOrder = {
        id: orders.length + 1,
        buyerId: currentUser.id,
        products: cart,
        status: 'completed',
        createdAt: new Date().toISOString()
    };

    orders.push(newOrder);
    localStorage.setItem('orders', JSON.stringify(orders));

    alert('Заказ оформлен! Товары отмечены как проданные.');

    cart = [];
    localStorage.removeItem('cart');
    updateCartCount();
    toggleCart();
    location.reload();
}

updateCartCount();

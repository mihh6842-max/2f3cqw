function toggleAuthForm() {
    const authPanel = document.getElementById('authPanel');
    authPanel.classList.toggle('active');
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('exchangeForm');
    const phoneInput = document.getElementById('phone');
    const successMessage = document.getElementById('successMessage');
    const errorMessage = document.getElementById('errorMessage');

    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');

        if (value.length > 0) {
            if (value[0] === '8') {
                value = '7' + value.substring(1);
            }
            if (value[0] !== '7') {
                value = '7' + value;
            }
        }

        let formattedValue = '+7';
        if (value.length > 1) {
            formattedValue += ' (' + value.substring(1, 4);
        }
        if (value.length >= 5) {
            formattedValue += ') ' + value.substring(4, 7);
        }
        if (value.length >= 8) {
            formattedValue += '-' + value.substring(7, 9);
        }
        if (value.length >= 10) {
            formattedValue += '-' + value.substring(9, 11);
        }

        e.target.value = formattedValue;
    });

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        successMessage.style.display = 'none';
        errorMessage.style.display = 'none';

        const formData = new FormData(form);

        try {
            const response = await fetch('submit.php', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                successMessage.style.display = 'block';
                form.reset();

                setTimeout(() => {
                    successMessage.style.display = 'none';
                }, 5000);
            } else {
                errorMessage.textContent = '✗ ' + (result.message || 'Ошибка отправки. Попробуйте еще раз.');
                errorMessage.style.display = 'block';
            }
        } catch (error) {
            console.error('Ошибка:', error);
            errorMessage.style.display = 'block';
        }
    });

    const amountInput = document.getElementById('amount');
    amountInput.addEventListener('input', function(e) {
        if (e.target.value < 0) {
            e.target.value = 0;
        }
    });
});

// Регистрация: валидация, маска даты, автозаполнение email

const form = document.getElementById('register-form');
const password = document.getElementById('password');
const password2 = document.getElementById('password2');
const email = document.getElementById('email');
const errorsBox = document.getElementById('errors');

// Автозаполнение email
const savedEmail = localStorage.getItem('lastEmail');
if (savedEmail) email.value = savedEmail;

// Проверка совпадения паролей в реальном времени
function checkPasswords() {
    if (password2.value && password.value !== password2.value) {
        errorsBox.textContent = 'Пароли не совпадают';
        return false;
    }
    errorsBox.textContent = '';
    return true;
}

password.addEventListener('input', checkPasswords);
password2.addEventListener('input', checkPasswords);

// Обработка отправки
form.addEventListener('submit', (e) => {
    e.preventDefault();
    errorsBox.textContent = '';

    if (!checkPasswords()) return;

    if (!form.checkValidity()) {
        errorsBox.textContent = 'Проверьте правильность заполнения полей';
        return;
    }

    const data = new FormData(form);
    const obj = {};
    data.forEach((value, key) => obj[key] = value);

    console.log('Данные формы:', obj);
    localStorage.setItem('lastEmail', email.value);

    alert('Регистрация прошла успешно!');
    form.reset();
});

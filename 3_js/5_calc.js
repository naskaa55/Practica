const display = document.getElementById('display');
const buttons = document.querySelectorAll('.buttons button');
let expression = '';
const history = [];

function updateDisplay() {
    display.textContent = expression || '0';
}

function calculate() {
    try {
        const safe = expression.replace(/[^0-9+\-*/().\s]/g, '');
        const result = eval(safe);
        if (!isFinite(result)) throw new Error('Деление на ноль');
        history.push({ expression, result });
        console.log('История:', history);
        expression = String(result);
    } catch (e) {
        expression = 'Ошибка';
        history.push({ expression: display.textContent, result: 'Ошибка' });
        console.log('История:', history);
    }
    updateDisplay();
}

function handleInput(value) {
    if (value === 'C') {
        expression = '';
    } else if (value === '=') {
        calculate();
        return;
    } else {
        if (expression === 'Ошибка') expression = '';
        expression += value;
    }
    updateDisplay();
}

buttons.forEach(btn => {
    btn.addEventListener('click', () => handleInput(btn.dataset.value));
});

// Клавиатура
document.addEventListener('keydown', (e) => {
    const key = e.key;
    if ((/[0-9]/).test(key) || '+-*/.'.includes(key)) handleInput(key);
    else if (key === 'Enter' || key === '=') handleInput('=');
    else if (key === 'Escape' || key === 'c' || key === 'C') handleInput('C');
    else if (key === 'Backspace') {
        expression = expression.slice(0, -1);
        updateDisplay();
    }
});

updateDisplay();

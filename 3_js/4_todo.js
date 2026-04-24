const input = document.getElementById('task-input');
const addBtn = document.getElementById('add-btn');
const list = document.getElementById('task-list');
const counter = document.getElementById('counter');
const filterRadios = document.querySelectorAll('input[name="filter"]');

let tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
let currentFilter = 'all';

function save() { localStorage.setItem('tasks', JSON.stringify(tasks)); }

function updateCounter() {
    const active = tasks.filter(t => !t.done).length;
    counter.textContent = active;
}

function render() {
    list.innerHTML = '';
    let shown = tasks.slice().sort((a, b) => a.text.localeCompare(b.text));

    if (currentFilter === 'active') shown = shown.filter(t => !t.done);
    if (currentFilter === 'done')   shown = shown.filter(t => t.done);

    shown.forEach(task => {
        const li = document.createElement('li');
        li.dataset.id = task.id;

        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.id = 'cb-' + task.id;
        cb.checked = task.done;
        cb.addEventListener('change', () => {
            task.done = cb.checked;
            save();
            render();
        });

        const label = document.createElement('label');
        label.htmlFor = cb.id;
        label.textContent = task.text;

        const del = document.createElement('button');
        del.className = 'delete';
        del.textContent = '×';
        del.addEventListener('click', () => {
            li.classList.add('removing');
            setTimeout(() => {
                tasks = tasks.filter(t => t.id !== task.id);
                save();
                render();
            }, 250);
        });

        li.append(cb, label, del);
        list.append(li);
    });

    updateCounter();
}

function addTask() {
    const text = input.value.trim();
    if (!text) return;
    tasks.push({ id: Date.now(), text, done: false });
    input.value = '';
    save();
    render();
}

addBtn.addEventListener('click', addTask);
input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') addTask();
});

filterRadios.forEach(r => {
    r.addEventListener('change', () => {
        currentFilter = r.value;
        render();
    });
});

render();

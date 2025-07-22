// Backend API base URL
const BASE_URL = 'http://localhost:5001/api/todos';
let todos = [];

const input = document.getElementById('todo-input');
const addBtn = document.getElementById('add-btn');
const todoList = document.getElementById('todo-list');
const progressText = document.getElementById('progress-text');
const progressBar = document.getElementById('progress-bar');

addBtn.addEventListener('click', addTask);
input.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') addTask();
});

function renderTodos() {
    todoList.innerHTML = '';
    todos.forEach(todo => {
        const li = document.createElement('li');
        if (todo.completed) li.classList.add('completed');

        const span = document.createElement('span');
        span.textContent = todo.text;
        span.style.cursor = 'pointer';
        span.onclick = () => markComplete(todo.id, !todo.completed);
        li.appendChild(span);

        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.className = 'delete-btn';
        delBtn.onclick = () => deleteTask(todo.id);
        li.appendChild(delBtn);

        todoList.appendChild(li);
    });
    updateProgress();
}

// CRUD operations
async function fetchTodos() {
    const res = await fetch(BASE_URL);
    todos = await res.json();
    renderTodos();
}

async function addTask() {
    const text = input.value.trim();
    if (!text) return;
    await fetch(BASE_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, completed: false })
    });
    input.value = '';
    await fetchTodos();
}

async function deleteTask(id) {
    await fetch(`${BASE_URL}/${id}`, { method: 'DELETE' });
    await fetchTodos();
}

async function markComplete(id, value) {
    await fetch(`${BASE_URL}/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: value })
    });
    await fetchTodos();
}

function updateProgress() {
    const total = todos.length;
    const completed = todos.filter(t => t.completed).length;
    progressText.textContent = `Completed: ${completed}/${total}`;
    progressBar.style.width = total ? ((completed / total) * 100) + '%' : '0%';
}

fetchTodos();

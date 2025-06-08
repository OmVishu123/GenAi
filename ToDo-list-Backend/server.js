const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 5001;

const FILE_PATH = path.join(__dirname, 'todos.json');

app.use(express.json());
app.use(cors());

function readTodos() {
  if (!fs.existsSync(FILE_PATH)) fs.writeFileSync(FILE_PATH, '[]');
  return JSON.parse(fs.readFileSync(FILE_PATH, 'utf-8'));
}

function writeTodos(todos) {
  fs.writeFileSync(FILE_PATH, JSON.stringify(todos, null, 2));
}

app.get('/api/todos', (req, res) => {
  res.json(readTodos());
});

app.post('/api/todos', (req, res) => {
  const { text, completed = false, timer = 0 } = req.body;
  const todos = readTodos();
  const todo = {
    id: Date.now(),
    text,
    completed,
    timer
  };
  todos.push(todo);
  writeTodos(todos);
  res.status(201).json(todo);
});

app.put('/api/todos/:id', (req, res) => {
  const { id } = req.params;
  const { text, completed, timer } = req.body;
  let todos = readTodos();
  const idx = todos.findIndex(t => t.id == id);
  if (idx === -1) return res.status(404).json({ error: 'Todo not found' });
  if (text !== undefined) todos[idx].text = text;
  if (completed !== undefined) todos[idx].completed = completed;
  if (timer !== undefined) todos[idx].timer = timer;
  writeTodos(todos);
  res.json(todos[idx]);
});

app.delete('/api/todos/:id', (req, res) => {
  const { id } = req.params;
  let todos = readTodos();
  todos = todos.filter(t => t.id != id);
  writeTodos(todos);
  res.json({ success: true });
});

app.listen(PORT, () => {
  console.log(`Backend running on http://localhost:${PORT}`);
});

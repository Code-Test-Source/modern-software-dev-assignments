const express = require('express');
const cors = require('cors');
const path = require('path');
const Database = require('better-sqlite3');

const app = express();
const db = new Database('devcenter.db');

// Initialize database
db.exec(`
  CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
  CREATE TABLE IF NOT EXISTS action_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );
`);

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

// Notes routes
app.get('/api/notes', (req, res) => {
  const { q } = req.query;
  let stmt = 'SELECT * FROM notes ORDER BY created_at DESC';
  let params = [];
  if (q) {
    stmt = 'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC';
    params = [`%${q}%`, `%${q}%`];
  }
  const notes = db.prepare(stmt).all(...params);
  res.json(notes);
});

app.post('/api/notes', (req, res) => {
  const { title, content = '' } = req.body;
  const result = db.prepare('INSERT INTO notes (title, content) VALUES (?, ?)').run(title, content);
  const note = db.prepare('SELECT * FROM notes WHERE id = ?').get(result.lastInsertRowid);
  res.status(201).json(note);
});

app.get('/api/notes/:id', (req, res) => {
  const note = db.prepare('SELECT * FROM notes WHERE id = ?').get(req.params.id);
  if (!note) return res.status(404).json({ error: 'Note not found' });
  res.json(note);
});

app.patch('/api/notes/:id', (req, res) => {
  const note = db.prepare('SELECT * FROM notes WHERE id = ?').get(req.params.id);
  if (!note) return res.status(404).json({ error: 'Note not found' });

  const { title = note.title, content = note.content } = req.body;
  db.prepare('UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?')
    .run(title, content, req.params.id);
  const updated = db.prepare('SELECT * FROM notes WHERE id = ?').get(req.params.id);
  res.json(updated);
});

app.delete('/api/notes/:id', (req, res) => {
  db.prepare('DELETE FROM notes WHERE id = ?').run(req.params.id);
  res.status(204).send();
});

// Action Items routes
app.get('/api/action-items', (req, res) => {
  const { completed } = req.query;
  let stmt = 'SELECT * FROM action_items ORDER BY created_at DESC';
  let params = [];
  if (completed !== undefined) {
    stmt = 'SELECT * FROM action_items WHERE completed = ? ORDER BY created_at DESC';
    params = [completed === 'true' ? 1 : 0];
  }
  const items = db.prepare(stmt).all(...params).map(item => ({
    ...item,
    completed: !!item.completed
  }));
  res.json(items);
});

app.post('/api/action-items', (req, res) => {
  const { description, completed = false } = req.body;
  const result = db.prepare('INSERT INTO action_items (description, completed) VALUES (?, ?)')
    .run(description, completed ? 1 : 0);
  const item = db.prepare('SELECT * FROM action_items WHERE id = ?').get(result.lastInsertRowid);
  res.status(201).json({ ...item, completed: !!item.completed });
});

app.put('/api/action-items/:id/complete', (req, res) => {
  db.prepare('UPDATE action_items SET completed = 1 WHERE id = ?').run(req.params.id);
  const item = db.prepare('SELECT * FROM action_items WHERE id = ?').get(req.params.id);
  if (!item) return res.status(404).json({ error: 'Action item not found' });
  res.json({ ...item, completed: !!item.completed });
});

app.patch('/api/action-items/:id', (req, res) => {
  const item = db.prepare('SELECT * FROM action_items WHERE id = ?').get(req.params.id);
  if (!item) return res.status(404).json({ error: 'Action item not found' });

  const { description = item.description, completed = item.completed } = req.body;
  db.prepare('UPDATE action_items SET description = ?, completed = ? WHERE id = ?')
    .run(description, completed ? 1 : 0, req.params.id);
  const updated = db.prepare('SELECT * FROM action_items WHERE id = ?').get(req.params.id);
  res.json({ ...updated, completed: !!updated.completed });
});

app.delete('/api/action-items/:id', (req, res) => {
  db.prepare('DELETE FROM action_items WHERE id = ?').run(req.params.id);
  res.status(204).send();
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));

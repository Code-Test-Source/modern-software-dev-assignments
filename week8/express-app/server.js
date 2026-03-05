const express = require('express');
const cors = require('cors');
const initSqlJs = require('sql.js');
const fs = require('fs');
const path = require('path');

const DB_PATH = 'devcenter.db';

async function startServer() {
  const SQL = await initSqlJs();

  // Load existing database or create new one
  let db;
  if (fs.existsSync(DB_PATH)) {
    const fileBuffer = fs.readFileSync(DB_PATH);
    db = new SQL.Database(fileBuffer);
  } else {
    db = new SQL.Database();
  }

  // Initialize database schema
  db.run(`
    CREATE TABLE IF NOT EXISTS notes (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      content TEXT DEFAULT '',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  db.run(`
    CREATE TABLE IF NOT EXISTS action_items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      description TEXT NOT NULL,
      completed INTEGER DEFAULT 0,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);
  saveDb(db);

  const app = express();
  app.use(cors());
  app.use(express.json());
  app.use(express.static('public'));

  // Helper to save database to file
  function saveDb(database) {
    const data = database.export();
    const buffer = Buffer.from(data);
    fs.writeFileSync(DB_PATH, buffer);
  }

  // Helper to run query and get results
  function queryAll(sql, params = []) {
    const stmt = db.prepare(sql);
    if (params.length > 0) stmt.bind(params);
    const results = [];
    while (stmt.step()) {
      const row = stmt.getAsObject();
      results.push(row);
    }
    stmt.free();
    return results;
  }

  function queryOne(sql, params = []) {
    const results = queryAll(sql, params);
    return results.length > 0 ? results[0] : null;
  }

  function runSql(sql, params = []) {
    db.run(sql, params);
    saveDb(db);
    return { lastInsertRowid: db.exec('SELECT last_insert_rowid() as id')[0]?.values[0]?.[0] };
  }

  // Notes routes
  app.get('/api/notes', (req, res) => {
    const { q } = req.query;
    let sql = 'SELECT * FROM notes ORDER BY created_at DESC';
    let params = [];
    if (q) {
      sql = 'SELECT * FROM notes WHERE title LIKE ? OR content LIKE ? ORDER BY created_at DESC';
      params = [`%${q}%`, `%${q}%`];
    }
    const notes = queryAll(sql, params);
    res.json(notes);
  });

  app.post('/api/notes', (req, res) => {
    const { title, content = '' } = req.body;
    db.run('INSERT INTO notes (title, content) VALUES (?, ?)', [title, content]);
    const id = db.exec('SELECT last_insert_rowid() as id')[0]?.values[0]?.[0];
    saveDb(db);
    const note = queryOne('SELECT * FROM notes WHERE id = ?', [id]);
    res.status(201).json(note);
  });

  app.get('/api/notes/:id', (req, res) => {
    const note = queryOne('SELECT * FROM notes WHERE id = ?', [req.params.id]);
    if (!note) return res.status(404).json({ error: 'Note not found' });
    res.json(note);
  });

  app.patch('/api/notes/:id', (req, res) => {
    const note = queryOne('SELECT * FROM notes WHERE id = ?', [req.params.id]);
    if (!note) return res.status(404).json({ error: 'Note not found' });

    const { title = note.title, content = note.content } = req.body;
    runSql('UPDATE notes SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?', [title, content, req.params.id]);
    const updated = queryOne('SELECT * FROM notes WHERE id = ?', [req.params.id]);
    res.json(updated);
  });

  app.delete('/api/notes/:id', (req, res) => {
    runSql('DELETE FROM notes WHERE id = ?', [req.params.id]);
    res.status(204).send();
  });

  // Action Items routes
  app.get('/api/action-items', (req, res) => {
    const { completed } = req.query;
    let sql = 'SELECT * FROM action_items ORDER BY created_at DESC';
    let params = [];
    if (completed !== undefined) {
      sql = 'SELECT * FROM action_items WHERE completed = ? ORDER BY created_at DESC';
      params = [completed === 'true' ? 1 : 0];
    }
    const items = queryAll(sql, params).map(item => ({
      ...item,
      completed: !!item.completed
    }));
    res.json(items);
  });

  app.post('/api/action-items', (req, res) => {
    const { description, completed = false } = req.body;
    db.run('INSERT INTO action_items (description, completed) VALUES (?, ?)', [description, completed ? 1 : 0]);
    const id = db.exec('SELECT last_insert_rowid() as id')[0]?.values[0]?.[0];
    saveDb(db);
    const item = queryOne('SELECT * FROM action_items WHERE id = ?', [id]);
    res.status(201).json({ ...item, completed: !!item.completed });
  });

  app.put('/api/action-items/:id/complete', (req, res) => {
    runSql('UPDATE action_items SET completed = 1 WHERE id = ?', [req.params.id]);
    const item = queryOne('SELECT * FROM action_items WHERE id = ?', [req.params.id]);
    if (!item) return res.status(404).json({ error: 'Action item not found' });
    res.json({ ...item, completed: !!item.completed });
  });

  app.patch('/api/action-items/:id', (req, res) => {
    const item = queryOne('SELECT * FROM action_items WHERE id = ?', [req.params.id]);
    if (!item) return res.status(404).json({ error: 'Action item not found' });

    const { description = item.description, completed = item.completed } = req.body;
    runSql('UPDATE action_items SET description = ?, completed = ? WHERE id = ?', [description, completed ? 1 : 0, req.params.id]);
    const updated = queryOne('SELECT * FROM action_items WHERE id = ?', [req.params.id]);
    res.json({ ...updated, completed: !!updated.completed });
  });

  app.delete('/api/action-items/:id', (req, res) => {
    runSql('DELETE FROM action_items WHERE id = ?', [req.params.id]);
    res.status(204).send();
  });

  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
}

startServer().catch(console.error);

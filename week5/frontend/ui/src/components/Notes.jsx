import { useState } from 'react';
import { notesApi } from '../services/api';

export function NoteForm({ onSubmit }) {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit({ title, content });
    setTitle('');
    setContent('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
      <input
        placeholder="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        required
      />
      <button type="submit">Add</button>
    </form>
  );
}

export function NoteList({ notes, onEdit, onDelete, onExtract }) {
  return (
    <ul>
      {notes.map((note) => (
        <li key={note.id}>
          <span className="note-content">
            <strong>{note.title}</strong>: {note.content}
          </span>
          {note.tags?.length > 0 && (
            <span className="tags">
              {note.tags.map((tag) => (
                <span key={tag.id} className="tag-chip">
                  #{tag.name}
                </span>
              ))}
            </span>
          )}
          <button onClick={() => onEdit(note)}>Edit</button>
          <button onClick={() => onDelete(note.id)}>Delete</button>
          <button onClick={() => onExtract(note.id)}>Extract</button>
        </li>
      ))}
    </ul>
  );
}

export function NoteSearch({ search, sort, tagFilter, tags, onSearchChange, onSortChange, onTagChange }) {
  return (
    <div className="search-controls">
      <input
        placeholder="Search notes..."
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
      />
      <select value={sort} onChange={(e) => onSortChange(e.target.value)}>
        <option value="created_desc">Newest first</option>
        <option value="title_asc">Title A-Z</option>
      </select>
      <select value={tagFilter} onChange={(e) => onTagChange(e.target.value)}>
        <option value="">All tags</option>
        {tags.map((tag) => (
          <option key={tag.id} value={tag.name}>
            #{tag.name}
          </option>
        ))}
      </select>
    </div>
  );
}

export function Pagination({ page, total, pageSize, onPageChange }) {
  const totalPages = Math.ceil(total / pageSize);
  if (totalPages <= 1) return null;

  return (
    <div className="pagination">
      <span>Page {page} of {totalPages} ({total} items)</span>
      {page > 1 && <button onClick={() => onPageChange(page - 1)}>Prev</button>}
      {page < totalPages && <button onClick={() => onPageChange(page + 1)}>Next</button>}
    </div>
  );
}

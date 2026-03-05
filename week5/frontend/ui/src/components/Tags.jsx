import { useState } from 'react';

export function TagForm({ onSubmit }) {
  const [name, setName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit({ name });
    setName('');
  };

  return (
    <form className="inline-form" onSubmit={handleSubmit}>
      <input
        placeholder="Tag name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        pattern="[a-zA-Z0-9_]+"
        required
      />
      <button type="submit">Add Tag</button>
    </form>
  );
}

export function TagList({ tags, onDelete, onSelect }) {
  return (
    <div className="tags-container">
      {tags.map((tag) => (
        <span
          key={tag.id}
          className="tag-chip"
          onClick={() => onSelect(tag.name)}
        >
          #{tag.name}
          <button
            className="tag-delete"
            onClick={(e) => {
              e.stopPropagation();
              onDelete(tag.id);
            }}
          >
            &times;
          </button>
        </span>
      ))}
    </div>
  );
}

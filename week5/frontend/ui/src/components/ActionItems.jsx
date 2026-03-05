import { useState } from 'react';

export function ActionForm({ onSubmit }) {
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await onSubmit({ description });
    setDescription('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
      />
      <button type="submit">Add</button>
    </form>
  );
}

export function ActionList({ items, onComplete, selectedIds, onToggleSelect }) {
  return (
    <ul>
      {items.map((item) => (
        <li key={item.id}>
          <input
            type="checkbox"
            className="action-checkbox"
            checked={selectedIds.includes(item.id)}
            onChange={() => onToggleSelect(item.id)}
            disabled={item.completed}
          />
          <span>
            {item.description} [{item.completed ? 'done' : 'open'}]
          </span>
          {!item.completed && (
            <button onClick={() => onComplete(item.id)}>Complete</button>
          )}
        </li>
      ))}
    </ul>
  );
}

export function ActionFilter({ filter, onChange }) {
  return (
    <div className="filter-controls">
      <label>
        <input
          type="radio"
          name="action-filter"
          checked={filter === null}
          onChange={() => onChange(null)}
        />
        All
      </label>
      <label>
        <input
          type="radio"
          name="action-filter"
          checked={filter === false}
          onChange={() => onChange(false)}
        />
        Open
      </label>
      <label>
        <input
          type="radio"
          name="action-filter"
          checked={filter === true}
          onChange={() => onChange(true)}
        />
        Completed
      </label>
    </div>
  );
}

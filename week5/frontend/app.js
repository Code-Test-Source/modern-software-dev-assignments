// State
let notesPage = 1;
let actionsPage = 1;
let actionsFilter = null;
let notesSearchQuery = '';
let notesSort = 'created_desc';
let tagFilter = '';
const pageSize = 10;

// Utilities
async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  const json = await res.json();

  // Handle envelope format
  if (json.ok === false) {
    throw new Error(json.error?.message || 'Request failed');
  }

  if (!res.ok) {
    throw new Error(json.error?.message || json.detail || 'Request failed');
  }

  return json.data;
}

function renderPagination(container, currentPage, total, onPageChange) {
  const totalPages = Math.ceil(total / pageSize);
  container.innerHTML = '';

  if (totalPages <= 1) return;

  const info = document.createElement('span');
  info.textContent = `Page ${currentPage} of ${totalPages} (${total} items)`;
  container.appendChild(info);

  if (currentPage > 1) {
    const prev = document.createElement('button');
    prev.textContent = 'Prev';
    prev.onclick = () => onPageChange(currentPage - 1);
    container.appendChild(prev);
  }

  if (currentPage < totalPages) {
    const next = document.createElement('button');
    next.textContent = 'Next';
    next.onclick = () => onPageChange(currentPage + 1);
    container.appendChild(next);
  }
}

function renderTags(tags) {
  const container = document.createElement('span');
  container.className = 'tags';
  for (const tag of tags) {
    const chip = document.createElement('span');
    chip.className = 'tag-chip';
    chip.textContent = `#${tag.name}`;
    chip.onclick = () => {
      tagFilter = tag.name;
      document.getElementById('tag-filter').value = tag.name;
      notesPage = 1;
      loadNotes();
    };
    container.appendChild(chip);
  }
  return container;
}

// Tags
async function loadTags() {
  const container = document.getElementById('tags-list');
  const tagFilterSelect = document.getElementById('tag-filter');

  try {
    const data = await fetchJSON('/tags/?page=1&page_size=100');
    container.innerHTML = '';

    // Update tag filter dropdown
    tagFilterSelect.innerHTML = '<option value="">All tags</option>';
    for (const tag of data.items) {
      const option = document.createElement('option');
      option.value = tag.name;
      option.textContent = `#${tag.name}`;
      if (tag.name === tagFilter) option.selected = true;
      tagFilterSelect.appendChild(option);

      // Render tag chip
      const chip = document.createElement('span');
      chip.className = 'tag-chip';
      chip.innerHTML = `#${tag.name} <button class="tag-delete" data-id="${tag.id}">&times;</button>`;
      container.appendChild(chip);
    }

    // Add delete handlers
    container.querySelectorAll('.tag-delete').forEach(btn => {
      btn.onclick = async (e) => {
        e.stopPropagation();
        if (confirm('Delete this tag?')) {
          await fetchJSON(`/tags/${btn.dataset.id}`, { method: 'DELETE' });
          loadTags();
          loadNotes();
        }
      };
    });
  } catch (err) {
    container.innerHTML = `<span style="color: red;">Error: ${err.message}</span>`;
  }
}

// Notes
async function loadNotes() {
  const list = document.getElementById('notes');
  const pagination = document.getElementById('notes-pagination');
  list.innerHTML = '';

  try {
    let url;
    if (notesSearchQuery) {
      url = `/notes/search/?q=${encodeURIComponent(notesSearchQuery)}&page=${notesPage}&page_size=${pageSize}&sort=${notesSort}`;
    } else {
      url = `/notes/?page=${notesPage}&page_size=${pageSize}`;
    }

    if (tagFilter) {
      url += `&tag=${encodeURIComponent(tagFilter)}`;
    }

    const data = await fetchJSON(url);

    for (const n of data.items) {
      const li = document.createElement('li');
      li.innerHTML = `<strong>${n.title}</strong>: ${n.content} `;

      // Tags
      if (n.tags && n.tags.length > 0) {
        li.appendChild(renderTags(n.tags));
        li.appendChild(document.createTextNode(' '));
      }

      const editBtn = document.createElement('button');
      editBtn.textContent = 'Edit';
      editBtn.onclick = () => editNote(n);
      li.appendChild(editBtn);

      const delBtn = document.createElement('button');
      delBtn.textContent = 'Delete';
      delBtn.onclick = async () => {
        if (confirm('Delete this note?')) {
          await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
          loadNotes();
        }
      };
      li.appendChild(delBtn);

      const extractBtn = document.createElement('button');
      extractBtn.textContent = 'Extract';
      extractBtn.onclick = async () => {
        const apply = confirm('Apply extracted items? (Cancel for preview only)');
        const result = await fetchJSON(`/notes/${n.id}/extract?apply=${apply}`);
        alert(`Extracted:\n- Hashtags: ${result.hashtags.join(', ') || 'none'}\n- Action items: ${result.action_items.join(', ') || 'none'}${apply ? `\n- Created tags: ${result.created_tags.join(', ') || 'none'}` : ''}`);
        if (apply) {
          loadNotes();
          loadActions();
          loadTags();
        }
      };
      li.appendChild(extractBtn);

      list.appendChild(li);
    }

    renderPagination(pagination, notesPage, data.total, (page) => {
      notesPage = page;
      loadNotes();
    });
  } catch (err) {
    list.innerHTML = `<li style="color: red;">Error: ${err.message}</li>`;
  }
}

async function editNote(note) {
  const title = prompt('New title:', note.title);
  if (title === null) return;
  const content = prompt('New content:', note.content);
  if (content === null) return;

  try {
    await fetchJSON(`/notes/${note.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    loadNotes();
  } catch (err) {
    alert('Error: ' + err.message);
  }
}

// Action Items
async function loadActions() {
  const list = document.getElementById('actions');
  const pagination = document.getElementById('actions-pagination');
  list.innerHTML = '';

  try {
    let url = `/action-items/?page=${actionsPage}&page_size=${pageSize}`;
    if (actionsFilter !== null) {
      url += `&completed=${actionsFilter}`;
    }

    const data = await fetchJSON(url);

    for (const a of data.items) {
      const li = document.createElement('li');

      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.className = 'action-checkbox';
      checkbox.dataset.id = a.id;
      checkbox.disabled = a.completed;
      li.appendChild(checkbox);

      const span = document.createElement('span');
      span.textContent = ` ${a.description} [${a.completed ? 'done' : 'open'}] `;
      li.appendChild(span);

      if (!a.completed) {
        const btn = document.createElement('button');
        btn.textContent = 'Complete';
        btn.onclick = async () => {
          await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
          loadActions();
        };
        li.appendChild(btn);
      }
      list.appendChild(li);
    }

    renderPagination(pagination, actionsPage, data.total, (page) => {
      actionsPage = page;
      loadActions();
    });
  } catch (err) {
    list.innerHTML = `<li style="color: red;">Error: ${err.message}</li>`;
  }
}

async function bulkComplete() {
  const checkboxes = document.querySelectorAll('.action-checkbox:checked');
  const ids = Array.from(checkboxes).map(cb => parseInt(cb.dataset.id));

  if (ids.length === 0) {
    alert('Select items to complete');
    return;
  }

  try {
    await fetchJSON('/action-items/bulk-complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids }),
    });
    loadActions();
  } catch (err) {
    alert('Error: ' + err.message);
  }
}

// Event Listeners
window.addEventListener('DOMContentLoaded', () => {
  // Note form
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    try {
      await fetchJSON('/notes/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, content }),
      });
      e.target.reset();
      loadNotes();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  });

  // Tag form
  document.getElementById('tag-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('tag-name').value;
    try {
      await fetchJSON('/tags/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      });
      e.target.reset();
      loadTags();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  });

  // Action form
  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    try {
      await fetchJSON('/action-items/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description }),
      });
      e.target.reset();
      loadActions();
    } catch (err) {
      alert('Error: ' + err.message);
    }
  });

  // Action filter
  document.querySelectorAll('input[name="action-filter"]').forEach(radio => {
    radio.addEventListener('change', (e) => {
      const val = e.target.value;
      actionsFilter = val === 'all' ? null : val === 'completed';
      actionsPage = 1;
      loadActions();
    });
  });

  // Bulk complete
  document.getElementById('bulk-complete-btn').addEventListener('click', bulkComplete);

  // Note search
  const searchInput = document.getElementById('note-search');
  let searchTimeout;
  searchInput.addEventListener('input', (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      notesSearchQuery = e.target.value.trim();
      notesPage = 1;
      loadNotes();
    }, 300);
  });

  // Note sort
  document.getElementById('note-sort').addEventListener('change', (e) => {
    notesSort = e.target.value;
    notesPage = 1;
    loadNotes();
  });

  // Tag filter
  document.getElementById('tag-filter').addEventListener('change', (e) => {
    tagFilter = e.target.value;
    notesPage = 1;
    loadNotes();
  });

  // Initial load
  loadNotes();
  loadActions();
  loadTags();
});

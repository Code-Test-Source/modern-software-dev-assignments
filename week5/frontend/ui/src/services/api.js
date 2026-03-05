const API_BASE = '';

async function fetchJSON(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  const json = await res.json();

  if (json.ok === false) {
    throw new Error(json.error?.message || 'Request failed');
  }

  if (!res.ok) {
    throw new Error(json.error?.message || json.detail || 'Request failed');
  }

  return json.data;
}

// Notes API
export const notesApi = {
  list: (page = 1, pageSize = 10, tag = '') =>
    fetchJSON(`/notes/?page=${page}&page_size=${pageSize}${tag ? `&tag=${encodeURIComponent(tag)}` : ''}`),

  search: (q, page = 1, pageSize = 10, sort = 'created_desc', tag = '') =>
    fetchJSON(`/notes/search/?q=${encodeURIComponent(q)}&page=${page}&page_size=${pageSize}&sort=${sort}${tag ? `&tag=${encodeURIComponent(tag)}` : ''}`),

  get: (id) => fetchJSON(`/notes/${id}`),

  create: (note) => fetchJSON('/notes/', {
    method: 'POST',
    body: JSON.stringify(note),
  }),

  update: (id, note) => fetchJSON(`/notes/${id}`, {
    method: 'PUT',
    body: JSON.stringify(note),
  }),

  delete: (id) => fetchJSON(`/notes/${id}`, { method: 'DELETE' }),

  extract: (id, apply = false) => fetchJSON(`/notes/${id}/extract?apply=${apply}`),

  attachTags: (noteId, tagIds) => fetchJSON(`/notes/${noteId}/tags`, {
    method: 'POST',
    body: JSON.stringify({ tag_ids: tagIds }),
  }),

  detachTag: (noteId, tagId) => fetchJSON(`/notes/${noteId}/tags/${tagId}`, { method: 'DELETE' }),
};

// Tags API
export const tagsApi = {
  list: (page = 1, pageSize = 100) =>
    fetchJSON(`/tags/?page=${page}&page_size=${pageSize}`),

  create: (tag) => fetchJSON('/tags/', {
    method: 'POST',
    body: JSON.stringify(tag),
  }),

  delete: (id) => fetchJSON(`/tags/${id}`, { method: 'DELETE' }),
};

// Action Items API
export const actionsApi = {
  list: (page = 1, pageSize = 10, completed = null) => {
    let url = `/action-items/?page=${page}&page_size=${pageSize}`;
    if (completed !== null) url += `&completed=${completed}`;
    return fetchJSON(url);
  },

  create: (item) => fetchJSON('/action-items/', {
    method: 'POST',
    body: JSON.stringify(item),
  }),

  complete: (id) => fetchJSON(`/action-items/${id}/complete`, { method: 'PUT' }),

  bulkComplete: (ids) => fetchJSON('/action-items/bulk-complete', {
    method: 'POST',
    body: JSON.stringify({ ids }),
  }),
};

async function fetchJSON(url, options) {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(await res.text());
    if (res.status === 204) return null;
    return res.json();
}

async function loadNotes(params = {}) {
    const list = document.getElementById('notes');
    list.innerHTML = '';
    const query = new URLSearchParams(params);
    const notes = await fetchJSON('/notes/?' + query.toString());
    for (const n of notes) {
        const li = document.createElement('li');
        const strong = document.createElement('strong');
        strong.textContent = n.title;
        li.appendChild(strong);
        li.appendChild(document.createTextNode(': ' + n.content));
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.onclick = async () => {
            await fetchJSON(`/notes/${n.id}`, { method: 'DELETE' });
            loadNotes(params);
        };
        li.appendChild(delBtn);
        list.appendChild(li);
    }
}

async function loadActions(params = {}) {
    const list = document.getElementById('actions');
    list.innerHTML = '';
    const query = new URLSearchParams(params);
    const items = await fetchJSON('/action-items/?' + query.toString());
    for (const a of items) {
        const li = document.createElement('li');
        li.className = a.completed ? 'completed' : '';
        li.textContent = a.description;
        if (!a.completed) {
            const btn = document.createElement('button');
            btn.textContent = 'Complete';
            btn.onclick = async () => {
                await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
                loadActions(params);
            };
            li.appendChild(btn);
        }
        const delBtn = document.createElement('button');
        delBtn.textContent = 'Delete';
        delBtn.onclick = async () => {
            await fetchJSON(`/action-items/${a.id}`, { method: 'DELETE' });
            loadActions(params);
        };
        li.appendChild(delBtn);
        list.appendChild(li);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('note-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const title = document.getElementById('note-title').value;
        const content = document.getElementById('note-content').value;
        await fetchJSON('/notes/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, content }),
        });
        e.target.reset();
        loadNotes();
    });

    document.getElementById('note-search-btn').addEventListener('click', () => {
        const q = document.getElementById('note-search').value;
        loadNotes({ q });
    });

    document.getElementById('action-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const description = document.getElementById('action-desc').value;
        await fetchJSON('/action-items/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ description }),
        });
        e.target.reset();
        loadActions();
    });

    document.getElementById('filter-completed').addEventListener('change', (e) => {
        loadActions({ completed: e.target.checked });
    });

    loadNotes();
    loadActions();
});

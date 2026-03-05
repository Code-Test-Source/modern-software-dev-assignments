import { useState, useEffect, useCallback } from 'react';
import { notesApi, tagsApi, actionsApi } from './services/api';
import { NoteForm, NoteList, NoteSearch, Pagination } from './components/Notes';
import { TagForm, TagList } from './components/Tags';
import { ActionForm, ActionList, ActionFilter } from './components/ActionItems';

const PAGE_SIZE = 10;

export default function App() {
  // Notes state
  const [notes, setNotes] = useState([]);
  const [notesTotal, setNotesTotal] = useState(0);
  const [notesPage, setNotesPage] = useState(1);
  const [notesSearch, setNotesSearch] = useState('');
  const [notesSort, setNotesSort] = useState('created_desc');
  const [tagFilter, setTagFilter] = useState('');

  // Tags state
  const [tags, setTags] = useState([]);

  // Actions state
  const [actions, setActions] = useState([]);
  const [actionsTotal, setActionsTotal] = useState(0);
  const [actionsPage, setActionsPage] = useState(1);
  const [actionsFilter, setActionsFilter] = useState(null);
  const [selectedActionIds, setSelectedActionIds] = useState([]);

  // Error state
  const [error, setError] = useState(null);

  // Load notes
  const loadNotes = useCallback(async () => {
    try {
      const data = notesSearch
        ? await notesApi.search(notesSearch, notesPage, PAGE_SIZE, notesSort, tagFilter)
        : await notesApi.list(notesPage, PAGE_SIZE, tagFilter);
      setNotes(data.items);
      setNotesTotal(data.total);
    } catch (err) {
      setError(err.message);
    }
  }, [notesPage, notesSearch, notesSort, tagFilter]);

  // Load tags
  const loadTags = useCallback(async () => {
    try {
      const data = await tagsApi.list();
      setTags(data.items);
    } catch (err) {
      setError(err.message);
    }
  }, []);

  // Load actions
  const loadActions = useCallback(async () => {
    try {
      const data = await actionsApi.list(actionsPage, PAGE_SIZE, actionsFilter);
      setActions(data.items);
      setActionsTotal(data.total);
    } catch (err) {
      setError(err.message);
    }
  }, [actionsPage, actionsFilter]);

  useEffect(() => {
    loadNotes();
  }, [loadNotes]);

  useEffect(() => {
    loadTags();
  }, [loadTags]);

  useEffect(() => {
    loadActions();
  }, [loadActions]);

  // Note handlers
  const handleCreateNote = async (note) => {
    await notesApi.create(note);
    loadNotes();
  };

  const handleEditNote = async (note) => {
    const title = prompt('New title:', note.title);
    if (title === null) return;
    const content = prompt('New content:', note.content);
    if (content === null) return;
    await notesApi.update(note.id, { title, content });
    loadNotes();
  };

  const handleDeleteNote = async (id) => {
    if (confirm('Delete this note?')) {
      await notesApi.delete(id);
      loadNotes();
    }
  };

  const handleExtract = async (noteId) => {
    const apply = confirm('Apply extracted items? (Cancel for preview only)');
    try {
      const result = await notesApi.extract(noteId, apply);
      alert(
        `Extracted:\n- Hashtags: ${result.hashtags.join(', ') || 'none'}\n` +
        `- Action items: ${result.action_items.join(', ') || 'none'}` +
        (apply ? `\n- Created tags: ${result.created_tags?.join(', ') || 'none'}` : '')
      );
      if (apply) {
        loadNotes();
        loadActions();
        loadTags();
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const handleSearchChange = (value) => {
    setNotesSearch(value);
    setNotesPage(1);
  };

  const handleSortChange = (value) => {
    setNotesSort(value);
    setNotesPage(1);
  };

  const handleTagFilterChange = (value) => {
    setTagFilter(value);
    setNotesPage(1);
  };

  // Tag handlers
  const handleCreateTag = async (tag) => {
    await tagsApi.create(tag);
    loadTags();
  };

  const handleDeleteTag = async (id) => {
    if (confirm('Delete this tag?')) {
      await tagsApi.delete(id);
      loadTags();
      loadNotes();
    }
  };

  // Action handlers
  const handleCreateAction = async (item) => {
    await actionsApi.create(item);
    loadActions();
  };

  const handleCompleteAction = async (id) => {
    await actionsApi.complete(id);
    loadActions();
  };

  const handleBulkComplete = async () => {
    if (selectedActionIds.length === 0) {
      alert('Select items to complete');
      return;
    }
    await actionsApi.bulkComplete(selectedActionIds);
    setSelectedActionIds([]);
    loadActions();
  };

  const handleToggleSelect = (id) => {
    setSelectedActionIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  return (
    <main>
      <h1>Modern Software Dev Starter</h1>

      {error && <p className="error">Error: {error}</p>}

      <section>
        <h2>Notes</h2>
        <NoteForm onSubmit={handleCreateNote} />
        <NoteSearch
          search={notesSearch}
          sort={notesSort}
          tagFilter={tagFilter}
          tags={tags}
          onSearchChange={handleSearchChange}
          onSortChange={handleSortChange}
          onTagChange={handleTagFilterChange}
        />
        <Pagination
          page={notesPage}
          total={notesTotal}
          pageSize={PAGE_SIZE}
          onPageChange={setNotesPage}
        />
        <NoteList
          notes={notes}
          onEdit={handleEditNote}
          onDelete={handleDeleteNote}
          onExtract={handleExtract}
        />
      </section>

      <section>
        <h2>Tags</h2>
        <TagForm onSubmit={handleCreateTag} />
        <TagList tags={tags} onDelete={handleDeleteTag} onSelect={handleTagFilterChange} />
      </section>

      <section>
        <h2>Action Items</h2>
        <ActionForm onSubmit={handleCreateAction} />
        <ActionFilter filter={actionsFilter} onChange={setActionsFilter} />
        <button onClick={handleBulkComplete}>Complete Selected</button>
        <Pagination
          page={actionsPage}
          total={actionsTotal}
          pageSize={PAGE_SIZE}
          onPageChange={setActionsPage}
        />
        <ActionList
          items={actions}
          onComplete={handleCompleteAction}
          selectedIds={selectedActionIds}
          onToggleSelect={handleToggleSelect}
        />
      </section>
    </main>
  );
}

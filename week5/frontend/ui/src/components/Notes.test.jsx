import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { NoteForm, NoteList, NoteSearch, Pagination } from './Notes';

describe('NoteForm', () => {
  it('renders form with title and content inputs', () => {
    render(<NoteForm onSubmit={() => {}} />);
    expect(screen.getByPlaceholderText('Title')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Content')).toBeInTheDocument();
    expect(screen.getByText('Add')).toBeInTheDocument();
  });

  it('calls onSubmit with form data', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<NoteForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Test Note' } });
    fireEvent.change(screen.getByPlaceholderText('Content'), { target: { value: 'Test Content' } });
    fireEvent.click(screen.getByText('Add'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ title: 'Test Note', content: 'Test Content' });
    });
  });

  it('clears form after submit', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<NoteForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByPlaceholderText('Title'), { target: { value: 'Test' } });
    fireEvent.change(screen.getByPlaceholderText('Content'), { target: { value: 'Content' } });
    fireEvent.click(screen.getByText('Add'));

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Title').value).toBe('');
      expect(screen.getByPlaceholderText('Content').value).toBe('');
    });
  });
});

describe('NoteList', () => {
  const mockNotes = [
    { id: 1, title: 'Note 1', content: 'Content 1', tags: [{ id: 1, name: 'tag1' }] },
    { id: 2, title: 'Note 2', content: 'Content 2', tags: [] },
  ];

  it('renders list of notes', () => {
    render(<NoteList notes={mockNotes} onEdit={() => {}} onDelete={() => {}} onExtract={() => {}} />);
    expect(screen.getByText('Note 1')).toBeInTheDocument();
    expect(screen.getByText('Note 2')).toBeInTheDocument();
  });

  it('displays tags for notes', () => {
    render(<NoteList notes={mockNotes} onEdit={() => {}} onDelete={() => {}} onExtract={() => {}} />);
    expect(screen.getByText('#tag1')).toBeInTheDocument();
  });

  it('calls onEdit when edit button clicked', () => {
    const onEdit = vi.fn();
    render(<NoteList notes={mockNotes} onEdit={onEdit} onDelete={() => {}} onExtract={() => {}} />);
    fireEvent.click(screen.getAllByText('Edit')[0]);
    expect(onEdit).toHaveBeenCalledWith(mockNotes[0]);
  });

  it('calls onDelete when delete button clicked', () => {
    const onDelete = vi.fn();
    render(<NoteList notes={mockNotes} onEdit={() => {}} onDelete={onDelete} onExtract={() => {}} />);
    fireEvent.click(screen.getAllByText('Delete')[0]);
    expect(onDelete).toHaveBeenCalledWith(1);
  });
});

describe('NoteSearch', () => {
  const mockTags = [
    { id: 1, name: 'python' },
    { id: 2, name: 'javascript' },
  ];

  it('renders search input and filters', () => {
    render(<NoteSearch tags={mockTags} search="" sort="created_desc" tagFilter="" />);
    expect(screen.getByPlaceholderText('Search notes...')).toBeInTheDocument();
    expect(screen.getAllByRole('combobox')).toHaveLength(2);
  });

  it('calls onSearchChange when search input changes', () => {
    const onSearchChange = vi.fn();
    render(<NoteSearch tags={mockTags} search="" onSearchChange={onSearchChange} />);
    fireEvent.change(screen.getByPlaceholderText('Search notes...'), { target: { value: 'test' } });
    expect(onSearchChange).toHaveBeenCalledWith('test');
  });

  it('renders tag options', () => {
    render(<NoteSearch tags={mockTags} search="" sort="created_desc" tagFilter="" />);
    expect(screen.getByText('#python')).toBeInTheDocument();
    expect(screen.getByText('#javascript')).toBeInTheDocument();
  });
});

describe('Pagination', () => {
  it('does not render for single page', () => {
    render(<Pagination page={1} total={5} pageSize={10} />);
    expect(screen.queryByText('Prev')).not.toBeInTheDocument();
  });

  it('renders pagination controls for multiple pages', () => {
    render(<Pagination page={1} total={25} pageSize={10} onPageChange={() => {}} />);
    expect(screen.getByText('Page 1 of 3 (25 items)')).toBeInTheDocument();
    expect(screen.getByText('Next')).toBeInTheDocument();
  });

  it('shows prev button on page 2', () => {
    render(<Pagination page={2} total={25} pageSize={10} onPageChange={() => {}} />);
    expect(screen.getByText('Prev')).toBeInTheDocument();
  });

  it('calls onPageChange when buttons clicked', () => {
    const onPageChange = vi.fn();
    render(<Pagination page={1} total={25} pageSize={10} onPageChange={onPageChange} />);
    fireEvent.click(screen.getByText('Next'));
    expect(onPageChange).toHaveBeenCalledWith(2);
  });
});

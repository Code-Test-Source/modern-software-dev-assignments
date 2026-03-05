import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { TagForm, TagList } from './Tags';

describe('TagForm', () => {
  it('renders form with tag name input', () => {
    render(<TagForm onSubmit={() => {}} />);
    expect(screen.getByPlaceholderText('Tag name')).toBeInTheDocument();
    expect(screen.getByText('Add Tag')).toBeInTheDocument();
  });

  it('calls onSubmit with tag name', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<TagForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByPlaceholderText('Tag name'), { target: { value: 'python' } });
    fireEvent.click(screen.getByText('Add Tag'));

    await waitFor(() => {
      expect(onSubmit).toHaveBeenCalledWith({ name: 'python' });
    });
  });

  it('clears form after submit', async () => {
    const onSubmit = vi.fn().mockResolvedValue(undefined);
    render(<TagForm onSubmit={onSubmit} />);

    fireEvent.change(screen.getByPlaceholderText('Tag name'), { target: { value: 'test' } });
    fireEvent.click(screen.getByText('Add Tag'));

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Tag name').value).toBe('');
    });
  });
});

describe('TagList', () => {
  const mockTags = [
    { id: 1, name: 'python' },
    { id: 2, name: 'javascript' },
  ];

  it('renders list of tags', () => {
    render(<TagList tags={mockTags} onDelete={() => {}} onSelect={() => {}} />);
    expect(screen.getByText('#python')).toBeInTheDocument();
    expect(screen.getByText('#javascript')).toBeInTheDocument();
  });

  it('calls onSelect when tag clicked', () => {
    const onSelect = vi.fn();
    render(<TagList tags={mockTags} onDelete={() => {}} onSelect={onSelect} />);
    fireEvent.click(screen.getByText('#python'));
    expect(onSelect).toHaveBeenCalledWith('python');
  });

  it('calls onDelete when delete button clicked', () => {
    const onDelete = vi.fn();
    render(<TagList tags={mockTags} onDelete={onDelete} onSelect={() => {}} />);
    fireEvent.click(screen.getAllByText('×')[0]);
    expect(onDelete).toHaveBeenCalledWith(1);
  });
});

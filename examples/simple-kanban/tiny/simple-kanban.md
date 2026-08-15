# TinySpec: Simple Kanban

**Status**: done
**Complexity**: small
**Storage**: browser only

## What

Build a clean, minimal todo app presented as a simple Kanban board. Users can create, read, edit, move, complete, and delete todos without an account or backend.

## Context

| File | Role |
|---|---|
| `app/page.tsx` | Board behavior, todo CRUD, drag and drop, and browser storage |
| `app/globals.css` | Responsive visual design and interaction states |
| `app/layout.tsx` | Product metadata |
| `public/tinyspec.md` | Deployable copy of this TinySpec |

## Requirements

1. Display To Do, In Progress, and Done columns with item counts.
2. Add title-only todos from an input inside the To Do column.
3. Move cards between columns using drag and drop.
4. Edit a todo title inline by selecting its title; Enter saves and Escape cancels.
5. Require confirmation before deleting a card.
6. Allow clearing all Done cards after confirmation.
7. Persist todos in browser storage across page reloads.
8. Use a clean, minimal, responsive, and accessible interface.
9. Display a readable copy of this TinySpec from within the app and provide access to the raw Markdown.

## Plan

1. Define a client-side todo model and safe browser-storage helpers.
2. Build the board, columns, add form, cards, inline editor, and destructive actions.
3. Add native drag-and-drop movement and responsive styling.
4. Add an accessible TinySpec viewer and publish the source Markdown with the app.
5. Verify production compilation and core CRUD behavior.

## Tasks

- [x] Replace the starter screen with the Kanban board.
- [x] Implement create, edit, move, and delete behavior.
- [x] Persist and restore todos from browser storage.
- [x] Add confirmation for destructive actions.
- [x] Add responsive and accessible interaction states.
- [x] Add an in-app TinySpec viewer and raw Markdown copy.
- [x] Run the production build.

## Done When

- [x] All CRUD operations work.
- [x] Drag and drop works across all three columns.
- [x] Todos survive a page reload in the same browser.
- [x] Empty and populated board states remain usable on mobile and desktop.
- [x] The current TinySpec is readable on the site and available as Markdown.
- [x] Production build passes.

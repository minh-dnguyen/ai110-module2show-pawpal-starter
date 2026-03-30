# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Smarter Scheduling (Phase 3 Features)

### Sorting & Filtering

- **`sort_by_time(tasks)`** — Sort tasks chronologically by `scheduled_time` (HH:MM format). Tasks without scheduled times are placed at the end.
- **`filter_by_status(tasks, status)`** — Filter tasks by completion status (`pending`, `completed`, or `skipped`).
- **`filter_by_pet(pet)`** — Get all tasks for a specific pet.
- **`filter_tasks(status=None, pet=None)`** — Combined multi-criteria filtering (chainable).

### Recurring Tasks

When a recurring task (daily/weekly) is marked completed, a **new instance is automatically created** for the next occurrence:

- **Daily tasks**: Next occurrence = today + 1 day (using `timedelta`)
- **Weekly tasks**: Next occurrence = today + 7 days

This keeps recurring care routines flowing without manual re-entry.

```python
# Marking a daily task complete creates tomorrow's instance
next_task = task.mark_completed()  # Returns Task or None
if next_task:
    pet.add_task(next_task)  # Adds tomorrow's feeding
```

### Conflict Detection

The scheduler detects time conflicts when two tasks are scheduled at the same time:

- **Same pet, same time**: ⚠️ Critical conflict (owner can't do both)
- **Different pets, same time**: ⚠️ Warning (owner is multi-tasking or context-switching)
- **Implementation**: O(n²) pairwise comparison sufficient for 7-15 daily tasks

Conflicts are returned as warnings (not exceptions), so the schedule doesn't crash:

```python
conflicts = scheduler.detect_conflicts(scheduled_tasks)
warnings = scheduler.get_conflict_warnings()
print(warnings)  # Displays human-readable warnings
```

### Testing

Run comprehensive tests covering:

- Task sorting by time (out-of-order inputs)
- Multi-criteria filtering (pet + status combinations)
- Recurring task creation with `timedelta` calculations
- Conflict detection (same-pet and cross-pet scenarios)

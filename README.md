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

### Smarter Scheduling

- **Core Classes**: Owner (with available time/preferences), Pet (type/age/needs), Task (duration/priority/status), TaskManager (CRUD operations), Scheduler (generates schedules with conflict detection), Schedule (stores tasks/total time), and AppController (backend integration).
- **Scheduling**: Filters pending tasks, sorts by priority, fits within available time starting at 9:00 AM; detects overlaps and notes same-pet conflicts.
- **UI Integration**: Streamlit app in `app.py` for inputting data, adding tasks/pets, and displaying generated schedules with totals.
- **Extras**: Task recurrence for auto-rescheduling, filtering/sorting tasks, and tradeoff-aware design prioritizing realism/simplicity.


### Testing PawPal+

Run the tests with:
```bash
python3 -m pytest tests/test_pawpal.py -v
```

The tests verify key behaviors: task status changes, task counting, chronological ordering in schedules, daily recurrence creation, and conflict detection for overlapping times. I give my system a 5 stars in reliability.
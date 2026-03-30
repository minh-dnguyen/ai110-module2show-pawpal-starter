# 🐾 PawPal+ — Intelligent Pet Care Scheduling

**PawPal+** is a Streamlit application that helps busy pet owners plan and optimize their daily pet care routines. Using intelligent scheduling algorithms, the app prioritizes critical care tasks, detects scheduling conflicts, and explains its reasoning in plain language.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Features](#features)
- [Architecture](#architecture)
- [Demo](#demo)
- [Usage Guide](#usage-guide)
- [Core Algorithms](#core-algorithms)
- [File Structure](#file-structure)

---

## Quick Start

### Installation

```bash
# Clone/navigate to project
cd ai110-module2show-pawpal-starter

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## ✨ Features

### 🏠 Owner & Pet Management

- **Owner Setup** — Enter name and daily time available (15-480 minutes)
- **Multi-Pet Support** — Manage multiple pets simultaneously
- **Pet Profiles** — Track name, species, and age

### 📝 Task Management

- **Task Creation** — Add tasks with:
  - Name, duration (minutes), priority level, category
  - Frequency (daily, weekly, monthly, as-needed)
  - Optional scheduled times (HH:MM format, e.g., "07:00")
- **Task Status Tracking** — Pending, Completed, or Skipped
- **Task Validation** — Prevents invalid priorities, negative durations, and missing data

### 🧠 Intelligent Scheduling Algorithms

#### 1. **Priority-Based Sorting** (`get_all_tasks_by_priority()`)

- Sorts all tasks by criticality: Essential (🔴 Level 1) → Standard (🟡 Level 2) → Bonus (🟢 Level 3)
- Within each priority level, shorter tasks scheduled first
- **Complexity**: O(n log n)
- **Use case**: Ensures critical health/medical tasks always fit in the schedule

#### 2. **Time-Based Sorting** (`sort_by_time()`)

- Sorts tasks by scheduled time in HH:MM format (earliest to latest)
- Tasks without scheduled times placed at the end
- **Complexity**: O(n log n)
- **Use case**: Viewing schedule in chronological order

#### 3. **Status Filtering** (`filter_by_status()`)

- Filters tasks by completion status: `pending`, `completed`, or `skipped`
- **Complexity**: O(n)
- **Use case**: Viewing only incomplete tasks or tasks that didn't fit today

#### 4. **Pet-Based Filtering** (`filter_by_pet()`)

- Retrieves all tasks for a specific pet
- **Complexity**: O(1) lookup
- **Use case**: Reviewing one pet's full care routine

#### 5. **Multi-Criteria Filtering** (`filter_tasks()`)

- Combines status and pet filters for flexible querying
- **Complexity**: O(n)
- **Use case**: "Show me skipped tasks for Mochi"

#### 6. **Greedy Schedule Generation** (`generate_schedule()`)

- **Algorithm**: Iterate through priority-sorted tasks; add each task if it fits within available time
- **Decision Rule**: `if time_used + task.duration ≤ available_time: schedule task`
- **Complexity**: O(n log n) for sorting + O(n) for scheduling = O(n log n) overall
- **Result**: Maximizes time usage while respecting priorities
- **Output**: Scheduled tasks, skipped tasks, time accounting, explanation reasoning

#### 7. **Conflict Detection** (`detect_conflicts()`)

- **Algorithm**: O(n²) pairwise comparison of scheduled tasks
- **Conflict**: Two tasks at the same `scheduled_time`
- **Classification**:
  - 🔴 **CRITICAL**: Same pet at same time (physically impossible)
  - 🟡 **WARNING**: Different pets at same time (owner juggling multiple pets)
- **Output**: List of conflicting task pairs with reasons
- **Appropriate for**: 7-15 daily tasks (cost: ~50-225 comparisons = negligible)

#### 8. **Recurring Task Generation** (`mark_completed()`)

- When a daily/weekly task is marked complete, automatically creates next occurrence
- **Daily**: `next_due_date = today + timedelta(days=1)`
- **Weekly**: `next_due_date = today + timedelta(weeks=1)`
- **Effect**: Pet care routines continue flowing without manual re-entry

### 🎨 Professional UI Components

The Streamlit app showcases all algorithms using:

| Component              | Purpose                                                                 |
| ---------------------- | ----------------------------------------------------------------------- |
| **Color-Coded Tables** | 🔴 Essential, 🟡 Standard, 🟢 Bonus priorities quickly visible          |
| **Category Icons**     | 🍽️ Feed, 🏃 Exercise, ✂️ Groom, 💊 Medical, 🎾 Enrichment, 📋 Other     |
| **Conflict Warnings**  | `st.warning()` prominently displays 🔴 CRITICAL vs 🟡 WARNING conflicts |
| **Success Messages**   | `st.success()` confirms when schedule has no conflicts                  |
| **Metrics Cards**      | Time Used, Utilization %, Remaining Time, Task counts                   |
| **Priority Breakdown** | Summary table showing time allocation by urgency level                  |
| **Tabbed Views**       | "All Tasks by Priority" and "Tasks by Pet" for flexible exploration     |

---

## 🏗️ Architecture

### Class Structure

**4 Core Classes:**

1. **`Task`** — Represents a single pet care activity
   - Attributes: name, duration, priority, category, frequency, status, scheduled_time, due_date
   - Methods: `mark_completed()`, `mark_skipped()`, `reset()`
   - Supports recurring tasks with automatic next-occurrence generation

2. **`Pet`** — Represents a pet with care tasks
   - Attributes: name, species, age, tasks (list)
   - Methods: `add_task()`, `remove_task()`, `get_tasks()`, `get_pending_tasks()`

3. **`Owner`** — Represents the pet owner with time constraints
   - Attributes: name, daily_time_available (minutes), pets (list)
   - Methods: `add_pet()`, `get_all_tasks()`, `get_all_pending_tasks()`

4. **`Scheduler`** — The intelligent scheduling engine
   - Attributes: owner, scheduled_tasks, skipped_tasks, time_used, reasoning
   - Methods: 15+ sorting, filtering, scheduling, and conflict detection methods

### Relationships

```
Owner (1) ──manages──> (*) Pet (1) ──has──> (*) Task
   │
   └── created by ──> Scheduler

Scheduler (1) ──processes──> (*) Task
```

**See [uml_final.md](uml_final.md) for detailed class diagram and Phase 1 → Final evolution.**

---

## 📸 Demo

### Live App Screenshot

<a href="/course_images/ai110/pawpal_app_screenshot.png" target="_blank"><img src='/course_images/ai110/pawpal_app_screenshot.png' title='PawPal+ App' width='100%' alt='PawPal+ App' class='center-block' /></a>

_Note: To add your screenshot here, capture the running Streamlit app and save it as `pawpal_app_screenshot.png` in the course resources folder._

### Quick Example: Daily Schedule Generation

**Input:**

- Owner: "Jordan" with 120 minutes available
- Pet 1: Mochi (dog) with 4 tasks
- Pet 2: Bella (cat) with 3 tasks

**Output:**

```
✅ Schedule Generated Successfully (No Conflicts)

SCHEDULED TASKS (6 total):
  1. 🔴 Bella's Feeding (5m, Level 1)
  2. 🔴 Feeding - Mochi (10m, Level 1)
  3. 🔴 Bella's Medical Check (10m, Level 1)
  4. 🔴 Morning Walk - Mochi (20m, Level 1)
  5. 🟡 Bella's Cuddle Time (15m, Level 2)
  6. 🟡 Grooming - Mochi (45m, Level 2)

SKIPPED TASKS (1 total):
  - 🟢 Playtime - Mochi (30m, Level 3) [Insufficient time]

METRICS:
  ⏱️ Time Used: 105 / 120 minutes (87.5%)
  ⏰ Time Remaining: 15 minutes

TIME BY PRIORITY:
  Level 1 (Essential): 45 min 🔴
  Level 2 (Standard):  60 min 🟡
  Level 3 (Bonus):     0 min  🟢
```

**To see the live app:**

1. Run `streamlit run app.py`
2. Browse to http://localhost:8501
3. Add a pet, add tasks, click "Generate Schedule"

---

## 📖 Usage Guide

### Step 1: Owner Setup

Enter your name and daily time available for pet care (15-480 minutes).

### Step 2: Add Pets

Create profiles for each pet (name, species, age).

### Step 3: Add Tasks

For each pet, add care tasks with:

- **Name**: Task description (e.g., "Morning Walk")
- **Duration**: Minutes required (1-240)
- **Priority**: Level 1 (Essential/Medical), Level 2 (Standard), or Level 3 (Bonus/Enrichment)
- **Category**: Feeding, Exercise, Grooming, Medical, Enrichment, or Other

### Step 4: View & Organize

Use the "View & Sort Tasks" tabs to explore:

- **All Tasks by Priority**: See complete picture sorted by criticality
- **Tasks by Pet**: Review each pet's full care routine

### Step 5: Generate Schedule

Click "Generate Schedule" to:

1. Detect any time conflicts (if tasks have scheduled times)
2. Create optimal daily plan based on priorities
3. Show which tasks fit and which don't
4. Display time metrics and reasoning

### Step 6: Review & Decide

- ✅ See scheduled tasks (green = confirmed for today)
- ⏭️ See skipped tasks (orange = not enough time)
- ⚠️ Address conflicts if any (red = must resolve)

---

## 🔬 Core Algorithms

### Algorithm Examples

**Example: Priority Sorting**

```python
scheduler = Scheduler(owner)
sorted_tasks = scheduler.get_all_tasks_by_priority()
# Returns: [critical_health_task, critical_med_task,
#          standard_feeding, standard_exercise,
#          bonus_playtime, ...]
```

**Example: Conflict Detection**

```python
# Schedule two tasks at same time for same pet
scheduler.scheduled_tasks[0].scheduled_time = "07:00"
scheduler.scheduled_tasks[1].scheduled_time = "07:00"

conflicts = scheduler.detect_conflicts()
# Returns: [(task1, task2, "Same pet (Mochi) at same time")]

warnings = scheduler.get_conflict_warnings()
# Returns formatted string suitable for UI display
```

**Example: Multi-Pet Filtering**

```python
# Get only pending tasks for Mochi
mochi_pending = scheduler.filter_tasks(status="pending", pet=mochi)
# Returns: [task1, task2, ...]

# Get all skipped tasks across all pets
all_skipped = scheduler.filter_by_status(
    owner.get_all_tasks(),
    status="skipped"
)
```

---

## 📁 File Structure

```
ai110-module2show-pawpal-starter/
├── app.py                  # Streamlit UI with all Phase 3 components
├── pawpal_system.py        # Core classes: Task, Pet, Owner, Scheduler
├── main.py                 # Entry point alternative
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── uml_final.md           # Detailed UML diagram with Phase 1→Final evolution
├── uml_diagram.md         # Mermaid class diagram source
├── reflection.md          # Project reflection: design choices, tradeoffs, AI collaboration
│
├── UI_IMPROVEMENTS.md     # Phase 3 UI enhancements guide
├── PHASE3_SUMMARY.md      # Comprehensive Phase 3 completion summary
├── QUICK_REFERENCE.md     # Quick lookup for UI changes
│
├── test_pawpal.py         # Unit tests for core algorithms
├── test_phase3_features.py # Feature demonstration script
│
└── __pycache__/           # Python cache (auto-generated)
```

---

## 🧪 Testing

### Run the Test Suite

```bash
# Test core system functionality
python -m pytest tests/test_pawpal.py -v

# Run Phase 3 feature demonstration
python test_phase3_features.py
```

### Test Coverage

- ✅ **Task creation** and validation (priority, duration, frequency)
- ✅ **Recurring task generation** (daily/weekly with timedelta)
- ✅ **Priority sorting** (correct order with duration tiebreaker)
- ✅ **Time-based sorting** (HH:MM chronological order)
- ✅ **Status filtering** (pending, completed, skipped)
- ✅ **Pet-based filtering** (single pet, multiple pets)
- ✅ **Schedule generation** (greedy algorithm correctness)
- ✅ **Conflict detection** (same-pet critical, cross-pet warning)
- ✅ **Edge cases** (empty task list, boundary time values)

---

## 🎯 Key Design Decisions

1. **Greedy Priority Algorithm** — Focus on getting critical health/medical tasks into the schedule first, then standard care, then bonuses. This maximizes coverage for essential needs within time constraints.

2. **O(n²) Conflict Detection** — For typical daily task counts (7-15), pairwise comparison is simpler to debug and understand than complex interval tree structures. The performance is negligible.

3. **Recurring Task Auto-Creation** — Rather than storing templates, we create the next actual task instance. This allows for easy future edits and status tracking per occurrence.

4. **Back-Reference in Task** (`owner_pet`) — Enables conflict detection to distinguish between same-pet conflicts (critical) and cross-pet conflicts (warning).

5. **Separation of Scheduler from Owner/Pet** — The scheduler is ephemeral/stateless until `generate_schedule()` is called. Multiple schedulers can be created for what-if scenarios.

---

## 🚀 Future Enhancements

- Duration-based conflict detection (detect overlaps like 7:00-7:20 vs 7:15-7:35)
- Drag-and-drop visual timeline scheduling
- Export schedule as PDF or calendar
- Task templates and quick-add buttons
- Pet-specific requirements (senior pet special care, dietary restrictions)
- Recurring task templates with skip/modify options
- Owner collaboration (shared households)
- Integration with calendar apps (Google Calendar, Outlook)

---

## 📚 References

- **Scheduling** inspired by job scheduling and bin packing problems (NP-hard family)
- **Greedy Algorithms** — used for their simplicity and acceptable results in pet care context
- **Python `timedelta`** — for robust date/time calculations across recurring tasks
- **Streamlit** — for rapid UI prototyping and data visualization

---

## 📝 License

This is an educational project (Module 2 - AI110).

---

## ❓ Questions?

Refer to the detailed documentation:

- [uml_final.md](uml_final.md) — Architecture and class relationships
- [reflection.md](reflection.md) — Design tradeoffs and AI collaboration notes
- [UI_IMPROVEMENTS.md](UI_IMPROVEMENTS.md) — Phase 3 UI component guide

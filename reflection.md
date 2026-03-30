# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.

**Three Core User Actions:**

1. **Set up pet profile** – Owner enters their name, pet name, species, and availability (time per day)
2. **Add/manage tasks** – Owner adds care tasks (e.g., morning walk, feeding, grooming) with duration (minutes) and priority
3. **Generate daily schedule** – System creates an optimized daily plan that fits available time, respects task priorities, and explains why tasks were chosen/ordered

**Four Core Objects:**

1. **Owner** (The Constraint Holder)
   - Attributes:
     - name (String): The owner's name
     - daily_time_available (Integer): Total time available for pet care today (in minutes)
   - Responsibility: Represent the user and their time constraint for the day

2. **Pet** (The Subject)
   - Attributes:
     - name (String): The pet's name
     - species (String): Type of pet
     - age (Integer): The pet's age
   - Responsibility: Store basic pet information; expandable for multiple pets or species-specific rules later

3. **Task** (The Building Block)
   - Attributes:
     - name (String): e.g., "Morning Walk," "Give Heartworm Meds"
     - duration (Integer): How long the task takes (in minutes)
     - priority (Integer or String): How critical the task is (1 = Essential/Medical, 2 = Standard Care, 3 = Bonus/Enrichment)
     - category (String): e.g., Feeding, Grooming, Exercise, Medical
   - Responsibility: Represent a single care activity with all data needed for scheduling decisions

4. **DailyPlan** (The Engine and Output)
   - Attributes:
     - scheduled_tasks (List): Tasks that made it into the final schedule
     - skipped_tasks (List): Lower-priority tasks dropped due to time constraints
     - time_used (Integer): Total minutes accounted for in the schedule
     - reasoning (String): Explanation of why certain tasks were prioritized
   - Methods:
     - generate_schedule(available_time, task_list): Sorts tasks by priority, fits them into available time, and stops when time runs out
   - Responsibility: Apply scheduling logic to create the final daily plan and explain decisions

**b. Design changes**

Yes, the design evolved during implementation to address missing relationships and potential logic bottlenecks:

1. **Connected Owner to Pet** – Added `pet` parameter to `Owner.__init__()` so the owner holds a reference to their pet. This ensures context is preserved throughout the scheduling process.

2. **Moved task list to Pet** – Added `tasks` list to `Pet` with `add_task()` and `get_tasks()` methods. This models real-world pet care: each pet has specific tasks, not the owner in isolation.

3. **Connected DailyPlan to Owner and Pet** – Changed `DailyPlan.__init__()` to require both `owner` and `pet` parameters. This eliminates context loss when generating schedules—the plan always knows whose tasks it's scheduling.

4. **Simplified generate_schedule() method** – Changed from `generate_schedule(available_time, task_list)` to `generate_schedule()` with no parameters. The method now reads `owner.daily_time_available` and `pet.tasks` directly, reducing coupling and making the method easier to call and test.

5. **Added Task validation** – Added `VALID_PRIORITIES` and `VALID_CATEGORIES` class constants and validation in `Task.__init__()` to catch invalid inputs early (e.g., priority outside 1-3 range, duration ≤ 0).

**Why these changes:**

- The initial design had Owner and Pet as isolated objects with no way to reference each other or their tasks. This would create friction when building the schedule.
- By connecting the objects, `DailyPlan.generate_schedule()` can build meaningful reasoning ("Owner Jordan has 120 minutes; Mochi needs...") instead of working with abstract parameters.
- Task validation prevents silent bugs from bad data propagating through the scheduler.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers three main constraints:

1. **Time**: Total daily minutes available (hard constraint)
2. **Priority**: Tasks ranked 1-3 (essential → bonus) (soft constraint)
3. **Frequency**: Daily, weekly, monthly occurrence patterns (soft constraint)

Priority ordering: time > priority level > task duration (shorter tasks fit when time is tight).

**b. Tradeoffs**

**Tradeoff: Exact Time Match vs. Overlapping Duration Detection**

The conflict detection algorithm (`detect_conflicts()`) currently checks for **exact time matches only**:

- ✅ **What it catches**: Two tasks scheduled at 07:00 → Conflict detected
- ❌ **What it misses**: Task A at 07:00-07:20 and Task B at 07:15-07:35 → No conflict detected (different schedule strings)

**Why this tradeoff is reasonable:**

| Aspect                  | Current Approach                            | Alternative                           |
| ----------------------- | ------------------------------------------- | ------------------------------------- |
| **Implementation**      | O(n²) pairwise string comparison            | O(n log n) with interval trees        |
| **Typical daily tasks** | 7-15 tasks                                  | ~50-100 comparisons per day (instant) |
| **Data accuracy**       | Requires `scheduled_time` to be precise     | Requires start/end times per task     |
| **Maintenance**         | Simple: check `time1 == time2`              | Complex: overlap mathematics          |
| **Pet care reality**    | Owners think in "7 AM slot" not "7:00-7:20" | More accurate but over-engineered     |

**Decision rationale:**

For a **pet owner scheduling app**, exact time slots are sufficient because:

1. Owners naturally think in discrete time blocks ("morning", "evening", "noon")
2. Task durations are estimates (owner can fit tasks flexibly)
3. Warnings for same-time conflicts help identify double-bookings
4. Future enhancement: Could add soft times (buffer periods) if needed

If overlapping duration detection becomes important (e.g., multi-hour tasks like "Day trip"), the algorithm can evolve to use interval structures without breaking existing code.

---

## 3. AI Collaboration

**a. How you used AI**

Used Copilot throughout the project via Explore agent for:

1. **Algorithm Design** — Asked for "small algorithms or logic improvements" for sorting, filtering, recurring tasks, and conflict detection. Received O(n log n) complexity analysis and practical recommendations.

2. **Optimization Review** — Shared the `detect_conflicts()` method with deeply nested if-else logic, asked: "How could this be simplified for readability or performance?" Received 3 different versions (helper methods, list comprehension, groupby) with complexity tradeoffs.

3. **Timedelta Usage** — Asked for Python's timedelta best practices to calculate next occurrence for recurring daily/weekly tasks. Got clear examples: `due_date + timedelta(days=1)` for daily, `due_date + timedelta(weeks=1)` for weekly.

4. **Conflict Detection Strategy** — Asked for "lightweight" conflict detection that returns warnings instead of crashing, especially for cross-pet scenarios.

**Most helpful prompts:**

- ✅ "How could this algorithm be simplified for better readability or performance?" — Led to discovering helper methods reduce nesting while keeping O(n²)
- ✅ Asking for complexity analysis (O(n²), O(n log n)) — Helped prioritize which optimizations matter
- ✅ Requesting 3 alternative versions — Enabled informed decision between readability vs performance

**b. Judgment and verification**

**Example: Conflict Detection Optimization**

Copilot suggested 3 versions:

1. **Helper methods** (most readable)
2. **List comprehension** (more Pythonic)
3. **Groupby** (more performant)

Initially tempting: Choose groupby for "better performance."

**What I did instead:**

- Analyzed actual constraints: 7-15 daily tasks = ~50-225 comparisons = **instant** either way
- Recognized pet-care context: App users value clarity > microseconds/day
- Chose Version 1 (helper methods) because:
  - O(n²) complexity is negligible for daily task counts
  - Readability improves future maintenance
  - Each helper method (`_has_time_overlap`, `_get_conflict_reason`) can be unit tested independently
  - Decision aligns with YAGNI principle ("You Aren't Gonna Need It")

**Verification:**

- Ran test with Version 1: Same results as original deeply-nested version ✅
- Docstrings added to all helper methods
- Tested edge cases: same-pet conflict, cross-pet conflict, no conflict → all pass ✅

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

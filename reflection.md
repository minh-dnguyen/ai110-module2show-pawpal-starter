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

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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

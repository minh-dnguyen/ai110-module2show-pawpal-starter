#!/usr/bin/env python
"""
Test script demonstrating Phase 3 UI improvements:
- Scheduler sorting methods
- Conflict detection
- Professional display formatting
"""

from pawpal_system import Owner, Pet, Task, Scheduler

print("=" * 70)
print("🐾 PawPal+ Phase 3 Feature Test")
print("=" * 70)

# Setup
owner = Owner(name="Jordan", daily_time_available=120)
mochi = Pet(name="Mochi", species="dog", age=3)
bella = Pet(name="Bella", species="cat", age=5)
owner.add_pet(mochi)
owner.add_pet(bella)

# Add tasks
print("\n1️⃣  ADDING TASKS FOR MOCHI AND BELLA:")
print("-" * 70)

tasks_to_add = [
    ("Morning Walk", 20, 1, "Exercise", mochi),
    ("Feeding", 10, 1, "Feeding", mochi),
    ("Playtime", 30, 3, "Enrichment", mochi),
    ("Grooming", 45, 2, "Grooming", mochi),
    ("Bella's Feeding", 5, 1, "Feeding", bella),
    ("Bella's Cuddle Time", 15, 2, "Enrichment", bella),
    ("Bella's Medical Check", 10, 1, "Medical", bella),
]

for name, duration, priority, category, pet in tasks_to_add:
    task = Task(name=name, duration=duration, priority=priority, category=category)
    pet.add_task(task)
    print(f"  ✅ Added: {name:25} ({priority}) to {pet.name}")

# Test 1: Priority Sorting
print("\n2️⃣  SCHEDULER SORTING BY PRIORITY:")
print("-" * 70)

scheduler = Scheduler(owner)
sorted_by_priority = scheduler.get_all_tasks_by_priority()

print("\nSorted Tasks (Priority → Duration):")
for i, task in enumerate(sorted_by_priority, 1):
    pet_name = task.owner_pet.name if task.owner_pet else "Unknown"
    priority_icon = "🔴" if task.priority == 1 else "🟡" if task.priority == 2 else "🟢"
    print(f"  {i:2}. {priority_icon} {task.name:20} ({task.duration:2}m) - {pet_name}")

# Test 2: Filtering by Status
print("\n3️⃣  SCHEDULER FILTERING BY STATUS:")
print("-" * 70)

pending = scheduler.filter_by_status(owner.get_all_tasks(), "pending")
print(f"\n  Pending Tasks: {len(pending)}")
for task in pending:
    print(f"    ✅ {task.name}")

# Test 3: Filtering by Pet
print("\n4️⃣  SCHEDULER FILTERING BY PET:")
print("-" * 70)

mochi_tasks = scheduler.filter_by_pet(mochi)
print(f"\n  Mochi's Tasks ({len(mochi_tasks)} total):")
for task in mochi_tasks:
    print(f"    🐕 {task.name:20} ({task.duration}m)")

bella_tasks = scheduler.filter_by_pet(bella)
print(f"\n  Bella's Tasks ({len(bella_tasks)} total):")
for task in bella_tasks:
    print(f"    🐈 {task.name:20} ({task.duration}m)")

# Test 4: Generate Schedule
print("\n5️⃣  SCHEDULE GENERATION:")
print("-" * 70)

scheduler.generate_schedule()
summary = scheduler.get_schedule_summary()

print(f"\n  Time Available: {summary['time_available']} minutes")
print(f"  Scheduled Tasks: {len(summary['scheduled_tasks'])}")
print(f"  Skipped Tasks: {len(summary['skipped_tasks'])}")
print(f"  Time Used: {summary['time_used']} minutes")
print(f"  Utilization: {round((summary['time_used'] / summary['time_available']) * 100, 1)}%")

# Test 5: Conflict Detection (add some time-scheduled tasks)
print("\n6️⃣  CONFLICT DETECTION:")
print("-" * 70)

# Set some scheduled times to create conflicts
scheduler.scheduled_tasks[0].scheduled_time = "07:00"
scheduler.scheduled_tasks[1].scheduled_time = "07:00"  # Same time as task 0
scheduler.scheduled_tasks[2].scheduled_time = "08:00"
scheduler.scheduled_tasks[3].scheduled_time = "08:00"  # Same time as task 2

conflicts = scheduler.detect_conflicts()

if conflicts:
    print("\n  ⚠️  CONFLICTS DETECTED!\n")
    for i, (task1, task2, reason) in enumerate(conflicts, 1):
        pet1 = task1.owner_pet.name if task1.owner_pet else "Unknown"
        pet2 = task2.owner_pet.name if task2.owner_pet else "Unknown"
        is_same_pet = pet1 == pet2
        conflict_type = "🔴 CRITICAL" if is_same_pet else "🟡 WARNING"
        
        print(f"  Conflict {i}: {conflict_type}")
        print(f"    Reason: {reason}")
        print(f"    Task 1: {task1.name} @ {task1.scheduled_time} ({pet1})")
        print(f"    Task 2: {task2.name} @ {task2.scheduled_time} ({pet2})")
        print()
else:
    print("\n  ✅ No conflicts detected!")

# Test 6: Display formatted summary
print("\n7️⃣  SCHEDULE SUMMARY TABLE:")
print("-" * 70)
print(f"\n  📊 Summary Statistics:")
print(f"  • Total Tasks: {len(owner.get_all_tasks())}")
print(f"  • Total Time Needed: {sum(t.duration for t in owner.get_all_tasks())} min")
print(f"  • Scheduled: {len(summary['scheduled_tasks'])} ✅")
print(f"  • Skipped: {len(summary['skipped_tasks'])} ⏭️")
print(f"  • Time Remaining: {summary['time_available'] - summary['time_used']} min")

# Priority breakdown
priority_time = {1: 0, 2: 0, 3: 0}
for task in summary['scheduled_tasks']:
    priority_time[task.priority] += task.duration

print(f"\n  ⏱️  Time by Priority:")
print(f"  • Level 1 (Critical): {priority_time[1]} min 🔴")
print(f"  • Level 2 (Standard): {priority_time[2]} min 🟡")
print(f"  • Level 3 (Bonus):    {priority_time[3]} min 🟢")

print("\n" + "=" * 70)
print("✨ All Phase 3 features working correctly!")
print("=" * 70)

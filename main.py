"""
Temporary testing script to verify PawPal+ system logic.
Tests: sorting, filtering, recurring tasks, and conflict detection.
"""

from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import datetime, timedelta



def main():
    print("=" * 70)
    print("🐾 PawPal+ Scheduler - Phase 3 Testing (Recurring Tasks & Conflicts)")
    print("=" * 70)
    print()
    
    # Create Owner with 120 minutes available
    owner = Owner(name="Jordan", daily_time_available=120)
    print(f"Created owner: {owner}")
    print()
    
    # Create two pets
    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)
    print(f"Added pets to owner: {[pet.name for pet in owner.get_pets()]}")
    print()
    
    # ===== SETUP WITH DUE DATES (using timedelta) =====
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)
    next_week = today + timedelta(weeks=1)
    
    print("=" * 70)
    print("FEATURE 1: RECURRING TASKS WITH TIMEDELTA DATE TRACKING")
    print("=" * 70)
    print()
    
    # Add tasks to Mochi (dog) WITH DUE DATES
    print("Adding DAILY tasks to Mochi (dog):")
    task1 = Task(
        name="Morning Walk",
        duration=20,
        priority=1,
        category="Exercise",
        frequency="daily",
        scheduled_time="07:00",
        due_date=today
    )
    task2 = Task(
        name="Feeding (Mochi)",
        duration=10,
        priority=1,
        category="Feeding",
        frequency="daily",
        scheduled_time="07:30",
        due_date=today
    )
    task3 = Task(
        name="Play/Enrichment",
        duration=30,
        priority=2,
        category="Enrichment",
        frequency="daily",
        scheduled_time="18:00",
        due_date=today
    )
    mochi.add_task(task1)
    mochi.add_task(task2)
    mochi.add_task(task3)
    print(f"  - {task1.name} @ {task1.scheduled_time} (due: {task1.due_date.date()})")
    print(f"  - {task2.name} @ {task2.scheduled_time} (due: {task2.due_date.date()})")
    print(f"  - {task3.name} @ {task3.scheduled_time} (due: {task3.due_date.date()})")
    print()
    
    # Add tasks to Luna (cat) WITH DUE DATES
    print("Adding DAILY and WEEKLY tasks to Luna (cat):")
    task4 = Task(
        name="Litter Box Cleaning",
        duration=5,
        priority=1,
        category="Grooming",
        frequency="daily",
        scheduled_time="08:00",
        due_date=today
    )
    task5 = Task(
        name="Feeding (Luna)",
        duration=5,
        priority=1,
        category="Feeding",
        frequency="daily",
        scheduled_time="06:00",
        due_date=today
    )
    task6 = Task(
        name="Playtime",
        duration=15,
        priority=2,
        category="Enrichment",
        frequency="daily",
        scheduled_time="19:00",
        due_date=today
    )
    task7 = Task(
        name="Full Grooming",
        duration=30,
        priority=2,
        category="Grooming",
        frequency="weekly",
        scheduled_time="10:00",
        due_date=today
    )
    luna.add_task(task4)
    luna.add_task(task5)
    luna.add_task(task6)
    luna.add_task(task7)
    print(f"  - {task4.name} @ {task4.scheduled_time} (daily, due: {task4.due_date.date()})")
    print(f"  - {task5.name} @ {task5.scheduled_time} (daily, due: {task5.due_date.date()})")
    print(f"  - {task6.name} @ {task6.scheduled_time} (daily, due: {task6.due_date.date()})")
    print(f"  - {task7.name} @ {task7.scheduled_time} (weekly, due: {task7.due_date.date()})")
    print()
    
    scheduler = Scheduler(owner)
    all_tasks = owner.get_all_tasks()
    
    # Test marking task complete and creating next occurrence
    print("-" * 70)
    print("Testing RECURRING TASK CREATION (mark_completed with timedelta):")
    print("-" * 70)
    print()
    
    print(f"BEFORE: Task '{task2.name}' status: {task2.completion_status}, due: {task2.due_date.date()}")
    print(f"BEFORE: Total tasks in Mochi's list: {len(mochi.tasks)}")
    print()
    
    # Mark task2 (daily Feeding) as complete - should create tomorrow's instance
    next_task = task2.mark_completed()
    
    if next_task:
        print(f"✓ mark_completed() returned a new task!")
        print(f"  Original task: '{task2.name}' now status={task2.completion_status}")
        print(f"  New task: '{next_task.name}' status={next_task.completion_status}, due: {next_task.due_date.date()}")
        print(f"  Next occurrence due date: {next_task.due_date} (calculated with timedelta)")
        mochi.add_task(next_task)
        print(f"  Added new task to Mochi. Total tasks now: {len(mochi.tasks)}")
    else:
        print("✗ No next task created")
    print()
    
    # Test weekly task
    print("Testing WEEKLY task recurring:")
    print(f"BEFORE: Task '{task7.name}' status: {task7.completion_status}, due: {task7.due_date.date()}")
    
    next_weekly = task7.mark_completed()
    if next_weekly:
        print(f"✓ mark_completed() returned a new weekly task!")
        print(f"  Original task: '{task7.name}' now status={task7.completion_status}")
        print(f"  New task: '{next_weekly.name}' status={next_weekly.completion_status}, due: {next_weekly.due_date.date()}")
        print(f"  Next occurrence: +7 days = {next_weekly.due_date.date()}")
        luna.add_task(next_weekly)
    print()
    
    # ===== CONFLICT DETECTION =====
    print("=" * 70)
    print("FEATURE 2: CONFLICT DETECTION (Same Pet, Same Time)")
    print("=" * 70)
    print()
    
    # Create new tasks to demonstrate conflicts
    print("Creating test scenario: Two tasks for Mochi at the SAME TIME (07:00)")
    print()
    
    conflict_task1 = Task(
        name="Morning Walk",
        duration=20,
        priority=1,
        category="Exercise",
        frequency="daily",
        scheduled_time="07:00",
        due_date=today
    )
    
    conflict_task2 = Task(
        name="Medication - Morning Dose",
        duration=10,
        priority=1,
        category="Medical",
        frequency="daily",
        scheduled_time="07:00",  # SAME TIME as walk!
        due_date=today
    )
    
    mochi.add_task(conflict_task1)
    mochi.add_task(conflict_task2)
    
    print(f"Task 1: {conflict_task1.name} @ {conflict_task1.scheduled_time} (Mochi)")
    print(f"Task 2: {conflict_task2.name} @ {conflict_task2.scheduled_time} (Mochi)")
    print()
    
    # Manually add to scheduled_tasks for testing
    test_scheduler = Scheduler(owner)
    test_scheduler.scheduled_tasks = [conflict_task1, conflict_task2]
    
    print("Checking for conflicts...")
    conflicts = test_scheduler.detect_conflicts()
    print(f"Found {len(conflicts)} conflict(s)")
    print()
    
    # Print conflict warnings
    warnings = test_scheduler.get_conflict_warnings()
    if warnings:
        print(warnings)
    else:
        print("✓ No conflicts detected")
    print()
    
    # ===== DIFFERENT PETS, SAME TIME =====
    print("-" * 70)
    print("Testing CROSS-PET CONFLICTS (Different pets at same time):")
    print("-" * 70)
    print()
    
    other_task = Task(
        name="Supplements for Luna",
        duration=5,
        priority=1,
        category="Medical",
        frequency="daily",
        scheduled_time="07:00",  # Same time as Mochi's walk!
        due_date=today
    )
    luna.add_task(other_task)
    
    print(f"Mochi task: {conflict_task1.name} @ {conflict_task1.scheduled_time}")
    print(f"Luna task:  {other_task.name} @ {other_task.scheduled_time}")
    print()
    
    test_scheduler.scheduled_tasks = [conflict_task1, other_task]
    conflicts = test_scheduler.detect_conflicts()
    
    warnings = test_scheduler.get_conflict_warnings()
    if warnings:
        print(warnings)
    else:
        print("✓ No conflicts detected")
    print()
    
    # ===== GENERATE NORMAL SCHEDULE =====
    print("=" * 70)
    print("GENERATING DAILY SCHEDULE")
    print("=" * 70)
    print()
    
    # Reset to use original tasks
    all_tasks = owner.get_all_tasks()
    scheduler.generate_schedule()
    
    summary = scheduler.get_schedule_summary()
    print(summary['reasoning'])
    print()
    
    print("SCHEDULED TASKS:")
    print("-" * 70)
    if summary['scheduled_tasks']:
        for i, task in enumerate(summary['scheduled_tasks'], 1):
            pet_name = task.owner_pet.name if task.owner_pet else "Unknown"
            print(f"{i}. {task.name:30} @ {str(task.scheduled_time):6} ({pet_name})")
    print()
    
    print("=" * 70)
    print(f"Time Summary: {summary['time_used']}/{summary['time_available']} minutes used")
    print("=" * 70)


if __name__ == "__main__":
    main()

"""
Temporary testing script to verify PawPal+ system logic.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("=" * 60)
    print("🐾 PawPal+ Scheduler - Testing Ground")
    print("=" * 60)
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
    
    # Add tasks to Mochi (dog)
    print("Adding tasks to Mochi (dog):")
    task1 = Task(
        name="Morning Walk",
        duration=20,
        priority=1,
        category="Exercise",
        frequency="daily"
    )
    task2 = Task(
        name="Feeding",
        duration=10,
        priority=1,
        category="Feeding",
        frequency="daily"
    )
    task3 = Task(
        name="Play/Enrichment",
        duration=30,
        priority=2,
        category="Enrichment",
        frequency="daily"
    )
    mochi.add_task(task1)
    mochi.add_task(task2)
    mochi.add_task(task3)
    print(f"  - {task1}")
    print(f"  - {task2}")
    print(f"  - {task3}")
    print()
    
    # Add tasks to Luna (cat)
    print("Adding tasks to Luna (cat):")
    task4 = Task(
        name="Litter Box Cleaning",
        duration=5,
        priority=1,
        category="Grooming",
        frequency="daily"
    )
    task5 = Task(
        name="Feeding",
        duration=5,
        priority=1,
        category="Feeding",
        frequency="daily"
    )
    task6 = Task(
        name="Playtime",
        duration=15,
        priority=2,
        category="Enrichment",
        frequency="daily"
    )
    task7 = Task(
        name="Grooming",
        duration=25,
        priority=3,
        category="Grooming",
        frequency="weekly"
    )
    luna.add_task(task4)
    luna.add_task(task5)
    luna.add_task(task6)
    luna.add_task(task7)
    print(f"  - {task4}")
    print(f"  - {task5}")
    print(f"  - {task6}")
    print(f"  - {task7}")
    print()
    
    # Display all tasks
    all_tasks = owner.get_all_tasks()
    print(f"Total tasks across all pets: {len(all_tasks)}")
    print()
    
    # Create scheduler and generate schedule
    print("=" * 60)
    print("GENERATING TODAY'S SCHEDULE")
    print("=" * 60)
    print()
    
    scheduler = Scheduler(owner)
    scheduler.generate_schedule()
    
    # Display results
    summary = scheduler.get_schedule_summary()
    print(summary['reasoning'])
    print()
    
    print("SCHEDULED TASKS:")
    print("-" * 60)
    if summary['scheduled_tasks']:
        total_duration = 0
        for i, task in enumerate(summary['scheduled_tasks'], 1):
            print(f"{i}. {task.name}")
            print(f"   Duration: {task.duration} min | Priority: {task.priority} | Category: {task.category}")
            total_duration += task.duration
        print(f"\nTotal scheduled time: {total_duration} minutes")
    else:
        print("No tasks scheduled.")
    print()
    
    print("SKIPPED TASKS (due to time constraints):")
    print("-" * 60)
    if summary['skipped_tasks']:
        for i, task in enumerate(summary['skipped_tasks'], 1):
            print(f"{i}. {task.name}")
            print(f"   Duration: {task.duration} min | Priority: {task.priority} | Category: {task.category}")
    else:
        print("All tasks fit in the available time!")
    print()
    
    print("=" * 60)
    print(f"Time Summary: {summary['time_used']}/{summary['time_available']} minutes used")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Unit tests for PawPal+ system classes.
"""

import pytest
from pawpal_system import Task, Pet, Owner, Scheduler


class TestTaskCompletion:
    """Tests for Task completion status."""
    
    def test_mark_completed_changes_status(self):
        """Verify that calling mark_completed() changes task status to 'completed'."""
        # Arrange
        task = Task(
            name="Morning Walk",
            duration=20,
            priority=1,
            category="Exercise"
        )
        assert task.completion_status == "pending"  # Initial status
        
        # Act
        task.mark_completed()
        
        # Assert
        assert task.completion_status == "completed"
    
    def test_mark_skipped_changes_status(self):
        """Verify that calling mark_skipped() changes task status to 'skipped'."""
        # Arrange
        task = Task(
            name="Grooming",
            duration=30,
            priority=2,
            category="Grooming"
        )
        assert task.completion_status == "pending"
        
        # Act
        task.mark_skipped()
        
        # Assert
        assert task.completion_status == "skipped"
    
    def test_reset_task_status(self):
        """Verify that calling reset() changes status back to 'pending'."""
        # Arrange
        task = Task(
            name="Feeding",
            duration=10,
            priority=1,
            category="Feeding"
        )
        task.mark_completed()
        assert task.completion_status == "completed"
        
        # Act
        task.reset()
        
        # Assert
        assert task.completion_status == "pending"


class TestTaskAddition:
    """Tests for adding tasks to pets."""
    
    def test_adding_task_increases_pet_task_count(self):
        """Verify that adding a task to a Pet increases that pet's task count."""
        # Arrange
        pet = Pet(name="Mochi", species="dog", age=3)
        initial_count = len(pet.get_tasks())
        assert initial_count == 0  # Should start with no tasks
        
        # Act
        task = Task(
            name="Morning Walk",
            duration=20,
            priority=1,
            category="Exercise"
        )
        pet.add_task(task)
        
        # Assert
        assert len(pet.get_tasks()) == initial_count + 1
        assert len(pet.get_tasks()) == 1
    
    def test_adding_multiple_tasks_to_pet(self):
        """Verify that multiple tasks can be added to a pet."""
        # Arrange
        pet = Pet(name="Luna", species="cat", age=5)
        
        # Act
        task1 = Task(name="Feeding", duration=5, priority=1, category="Feeding")
        task2 = Task(name="Playtime", duration=15, priority=2, category="Enrichment")
        task3 = Task(name="Grooming", duration=20, priority=3, category="Grooming")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # Assert
        assert len(pet.get_tasks()) == 3
        assert pet.get_tasks()[0] == task1
        assert pet.get_tasks()[1] == task2
        assert pet.get_tasks()[2] == task3
    
    def test_removing_task_from_pet(self):
        """Verify that removing a task decreases pet's task count."""
        # Arrange
        pet = Pet(name="Mochi", species="dog", age=3)
        task1 = Task(name="Morning Walk", duration=20, priority=1, category="Exercise")
        task2 = Task(name="Evening Walk", duration=20, priority=2, category="Exercise")
        pet.add_task(task1)
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2
        
        # Act
        pet.remove_task(task1)
        
        # Assert
        assert len(pet.get_tasks()) == 1
        assert task1 not in pet.get_tasks()
        assert task2 in pet.get_tasks()


class TestOwnerAndPets:
    """Tests for Owner managing multiple pets."""
    
    def test_owner_can_add_multiple_pets(self):
        """Verify that Owner can add and retrieve multiple pets."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Luna", species="cat", age=5)
        
        # Act
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Assert
        assert len(owner.get_pets()) == 2
        assert pet1 in owner.get_pets()
        assert pet2 in owner.get_pets()
    
    def test_owner_get_all_tasks_across_pets(self):
        """Verify that Owner can retrieve all tasks from all pets."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Luna", species="cat", age=5)
        
        task1 = Task(name="Walk Mochi", duration=20, priority=1, category="Exercise")
        task2 = Task(name="Mochi Feeding", duration=10, priority=1, category="Feeding")
        task3 = Task(name="Luna Feeding", duration=5, priority=1, category="Feeding")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        # Act
        all_tasks = owner.get_all_tasks()
        
        # Assert
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks


class TestScheduler:
    """Tests for Scheduler logic."""
    
    def test_scheduler_generates_schedule_with_available_time(self):
        """Verify that Scheduler can generate a schedule within time constraints."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=60)
        pet = Pet(name="Mochi", species="dog", age=3)
        
        task1 = Task(name="Walk", duration=20, priority=1, category="Exercise")
        task2 = Task(name="Feeding", duration=10, priority=1, category="Feeding")
        task3 = Task(name="Play", duration=15, priority=2, category="Enrichment")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        # Act
        scheduler = Scheduler(owner)
        scheduler.generate_schedule()
        summary = scheduler.get_schedule_summary()
        
        # Assert
        assert summary['time_used'] <= owner.daily_time_available
        assert len(summary['scheduled_tasks']) > 0
    
    def test_scheduler_skips_tasks_when_time_insufficient(self):
        """Verify that Scheduler skips lower-priority tasks when time is insufficient."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=30)
        pet = Pet(name="Mochi", species="dog", age=3)
        
        # High priority tasks that fit
        task1 = Task(name="Walk", duration=20, priority=1, category="Exercise")
        task2 = Task(name="Feeding", duration=10, priority=1, category="Feeding")
        # Low priority task that won't fit
        task3 = Task(name="Grooming", duration=30, priority=3, category="Grooming")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        owner.add_pet(pet)
        
        # Act
        scheduler = Scheduler(owner)
        scheduler.generate_schedule()
        summary = scheduler.get_schedule_summary()
        
        # Assert
        assert task3 in summary['skipped_tasks']
        assert task1 in summary['scheduled_tasks']
        assert task2 in summary['scheduled_tasks']
        assert summary['time_used'] == 30


class TestSortingCorrectness:
    """Tests for sort_by_time() chronological ordering. Happy path: tasks sorted earliest→latest."""
    
    def test_sort_by_time_chronological_order(self):
        """Verify that sort_by_time() returns tasks in chronological order (earliest first)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Evening Walk", duration=20, priority=2, category="Exercise", scheduled_time="18:00")
        task2 = Task(name="Morning Walk", duration=20, priority=1, category="Exercise", scheduled_time="07:30")
        task3 = Task(name="Midday Play", duration=15, priority=2, category="Enrichment", scheduled_time="12:00")
        
        # Act
        sorted_tasks = scheduler.sort_by_time([task1, task2, task3])
        
        # Assert - should be in order: 07:30, 12:00, 18:00
        assert sorted_tasks[0].scheduled_time == "07:30"
        assert sorted_tasks[1].scheduled_time == "12:00"
        assert sorted_tasks[2].scheduled_time == "18:00"
    
    def test_sort_by_time_unscheduled_tasks_last(self):
        """Verify that tasks without scheduled_time appear at the end (edge case: unscheduled tasks)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Flexible Task", duration=15, priority=2, category="Enrichment", scheduled_time=None)
        task2 = Task(name="Morning Walk", duration=20, priority=1, category="Exercise", scheduled_time="08:00")
        task3 = Task(name="Another Flexible", duration=10, priority=3, category="Other", scheduled_time=None)
        
        # Act
        sorted_tasks = scheduler.sort_by_time([task1, task2, task3])
        
        # Assert - scheduled task first, unscheduled at end
        assert sorted_tasks[0].scheduled_time == "08:00"
        assert sorted_tasks[1].scheduled_time is None
        assert sorted_tasks[2].scheduled_time is None
    
    def test_sort_by_time_empty_list(self):
        """Verify that sort_by_time() handles empty task list gracefully (edge case: no tasks)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Act
        sorted_tasks = scheduler.sort_by_time([])
        
        # Assert
        assert sorted_tasks == []
        assert len(sorted_tasks) == 0
    
    def test_sort_by_time_single_task(self):
        """Verify that sort_by_time() handles single task correctly."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task = Task(name="Morning Walk", duration=20, priority=1, category="Exercise", scheduled_time="07:30")
        
        # Act
        sorted_tasks = scheduler.sort_by_time([task])
        
        # Assert
        assert len(sorted_tasks) == 1
        assert sorted_tasks[0] == task


class TestRecurrenceLogic:
    """Tests for recurring task creation. Happy path: marking daily task complete creates next-day task."""
    
    def test_daily_task_recurrence_creates_next_day(self):
        """Verify that marking a daily task complete creates a new task for the next day."""
        # Arrange
        from datetime import datetime, timedelta
        today = datetime(2026, 3, 30, 8, 0)  # March 30
        
        task = Task(
            name="Morning Walk",
            duration=20,
            priority=1,
            category="Exercise",
            frequency="daily",
            completion_status="pending",
            scheduled_time="08:00",
            due_date=today
        )
        assert task.completion_status == "pending"
        
        # Act
        next_task = task.mark_completed()
        
        # Assert - original marked complete, new task created
        assert task.completion_status == "completed"
        assert next_task is not None
        assert next_task.name == "Morning Walk"
        assert next_task.completion_status == "pending"
        assert next_task.due_date == today + timedelta(days=1)
        assert next_task.scheduled_time == "08:00"
    
    def test_weekly_task_recurrence_creates_next_week(self):
        """Verify that marking a weekly task complete creates a new task for the next week."""
        # Arrange
        from datetime import datetime, timedelta
        today = datetime(2026, 3, 30, 10, 0)  # Monday
        
        task = Task(
            name="Weekly Grooming",
            duration=45,
            priority=2,
            category="Grooming",
            frequency="weekly",
            completion_status="pending",
            scheduled_time="10:00",
            due_date=today
        )
        
        # Act
        next_task = task.mark_completed()
        
        # Assert - new task scheduled 7 days later
        assert task.completion_status == "completed"
        assert next_task is not None
        assert next_task.due_date == today + timedelta(weeks=1)
        assert next_task.frequency == "weekly"
    
    def test_non_recurring_task_returns_none(self):
        """Verify that marking a non-recurring (as_needed) task complete returns None (edge case)."""
        # Arrange
        task = Task(
            name="Vet Checkup",
            duration=30,
            priority=1,
            category="Medical",
            frequency="as_needed",
            completion_status="pending"
        )
        
        # Act
        result = task.mark_completed()
        
        # Assert
        assert task.completion_status == "completed"
        assert result is None
    
    def test_daily_task_preserves_properties_on_recurrence(self):
        """Verify that all task properties (duration, priority, category) carry forward on recurrence."""
        # Arrange
        from datetime import datetime
        today = datetime(2026, 3, 30)
        
        task = Task(
            name="Heartworm Meds",
            duration=5,
            priority=1,
            category="Medical",
            frequency="daily",
            scheduled_time="09:00",
            due_date=today
        )
        
        # Act
        next_task = task.mark_completed()
        
        # Assert - all properties match original
        assert next_task.name == task.name
        assert next_task.duration == task.duration
        assert next_task.priority == task.priority
        assert next_task.category == task.category
        assert next_task.frequency == task.frequency
        assert next_task.scheduled_time == task.scheduled_time


class TestConflictDetection:
    """Tests for detecting duplicate-time conflicts. Happy path: flags tasks at same time."""
    
    def test_detect_conflict_same_pet_same_time(self):
        """Verify that detect_conflicts() flags two tasks for same pet at the exact same time."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Morning Meds", duration=5, priority=1, category="Medical", scheduled_time="08:00")
        task2 = Task(name="Morning Walk", duration=20, priority=1, category="Exercise", scheduled_time="08:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.owner_pet = pet
        task2.owner_pet = pet
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 1
        conflict_task1, conflict_task2, reason = conflicts[0]
        assert conflict_task1 == task1
        assert conflict_task2 == task2
        assert "Mochi" in reason
        assert "same pet" in reason.lower()
    
    def test_detect_conflict_different_pets_same_time(self):
        """Verify that detect_conflicts() flags two tasks for different pets at same time (cross-pet conflict)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet1 = Pet(name="Mochi", species="dog", age=3)
        pet2 = Pet(name="Luna", species="cat", age=5)
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Mochi Walk", duration=20, priority=1, category="Exercise", scheduled_time="09:00")
        task2 = Task(name="Luna Feeding", duration=5, priority=1, category="Feeding", scheduled_time="09:00")
        
        pet1.add_task(task1)
        pet2.add_task(task2)
        task1.owner_pet = pet1
        task2.owner_pet = pet2
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 1
        _, _, reason = conflicts[0]
        assert "Different pets" in reason or "different pets" in reason.lower()
    
    def test_no_conflict_different_times(self):
        """Verify that detect_conflicts() returns empty list when tasks have different times."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Morning Walk", duration=20, priority=1, category="Exercise", scheduled_time="08:00")
        task2 = Task(name="Evening Walk", duration=20, priority=2, category="Exercise", scheduled_time="18:00")
        
        pet.add_task(task1)
        pet.add_task(task2)
        task1.owner_pet = pet
        task2.owner_pet = pet
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 0
    
    def test_no_conflict_unscheduled_tasks(self):
        """Verify that unscheduled tasks (no time) don't create conflicts (edge case)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Flexible Task 1", duration=15, priority=2, category="Enrichment", scheduled_time=None)
        task2 = Task(name="Flexible Task 2", duration=10, priority=3, category="Other", scheduled_time=None)
        
        pet.add_task(task1)
        pet.add_task(task2)
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2])
        
        # Assert
        assert len(conflicts) == 0
    
    def test_conflict_warnings_formatted_output(self):
        """Verify that get_conflict_warnings() produces human-readable warning message."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        task1 = Task(name="Meds", duration=5, priority=1, category="Medical", scheduled_time="09:00")
        task2 = Task(name="Walk", duration=20, priority=1, category="Exercise", scheduled_time="09:00")
        
        task1.owner_pet = pet
        task2.owner_pet = pet
        
        # Act
        warning_msg = scheduler.get_conflict_warnings([task1, task2])
        
        # Assert
        assert "⚠️" in warning_msg or "conflict" in warning_msg.lower()
        assert "09:00" in warning_msg
        assert len(warning_msg) > 0


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""
    
    def test_pet_with_no_tasks(self):
        """Verify that a pet with zero tasks handles gracefully (edge case: empty pet)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Act
        pending_tasks = pet.get_pending_tasks()
        all_tasks = owner.get_all_pending_tasks()
        
        # Assert
        assert len(pending_tasks) == 0
        assert len(all_tasks) == 0
    
    def test_schedule_generation_with_zero_available_time(self):
        """Verify schedule generation handles zero available time (edge case: no time budget)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=0)
        pet = Pet(name="Mochi", species="dog", age=3)
        task = Task(name="Walk", duration=20, priority=1, category="Exercise")
        
        pet.add_task(task)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Act
        scheduler.generate_schedule()
        summary = scheduler.get_schedule_summary()
        
        # Assert
        assert len(summary['scheduled_tasks']) == 0
        assert len(summary['skipped_tasks']) == 1
        assert summary['time_used'] == 0
    
    def test_multiple_conflicts_detected(self):
        """Verify that multiple conflicts are all detected (edge case: cascade conflicts)."""
        # Arrange
        owner = Owner(name="Jordan", daily_time_available=120)
        pet = Pet(name="Mochi", species="dog", age=3)
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        # Three tasks all at same time
        task1 = Task(name="Task 1", duration=10, priority=1, category="Other", scheduled_time="10:00")
        task2 = Task(name="Task 2", duration=10, priority=2, category="Other", scheduled_time="10:00")
        task3 = Task(name="Task 3", duration=10, priority=3, category="Other", scheduled_time="10:00")
        
        for task in [task1, task2, task3]:
            task.owner_pet = pet
        
        # Act
        conflicts = scheduler.detect_conflicts([task1, task2, task3])
        
        # Assert - should detect 3 pairwise conflicts: (1,2), (1,3), (2,3)
        assert len(conflicts) == 3

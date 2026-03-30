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

"""
PawPal+ System Classes

Core classes for pet care planning and scheduling.
"""
from typing import List, Optional
from datetime import datetime


class Task:
    """Represents a single pet care activity."""
    
    VALID_PRIORITIES = [1, 2, 3]  # 1=Essential/Medical, 2=Standard Care, 3=Bonus/Enrichment
    VALID_CATEGORIES = ['Feeding', 'Grooming', 'Exercise', 'Medical', 'Enrichment', 'Other']
    VALID_FREQUENCIES = ['daily', 'weekly', 'monthly', 'as_needed']
    VALID_STATUSES = ['pending', 'completed', 'skipped']
    
    def __init__(self, name: str, duration: int, priority: int, category: str, 
                 frequency: str = 'daily', completion_status: str = 'pending'):
        """
        Initialize a Task.
        
        Args:
            name: Task name (e.g., 'Morning Walk', 'Give Heartworm Meds')
            duration: How long the task takes (in minutes)
            priority: How critical (1 = Essential/Medical, 2 = Standard Care, 3 = Bonus/Enrichment)
            category: Task category (Feeding, Grooming, Exercise, Medical, Enrichment, Other)
            frequency: How often task occurs (daily, weekly, monthly, as_needed)
            completion_status: Current status (pending, completed, skipped)
        
        Raises:
            ValueError: If priority, frequency, or status invalid, or duration <= 0
        """
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}, got {priority}")
        if duration <= 0:
            raise ValueError(f"Duration must be positive, got {duration}")
        if frequency not in self.VALID_FREQUENCIES:
            raise ValueError(f"Frequency must be one of {self.VALID_FREQUENCIES}, got {frequency}")
        if completion_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}, got {completion_status}")
        
        self.name = name
        self.duration = duration
        self.priority = priority
        self.category = category
        self.frequency = frequency
        self.completion_status = completion_status
    
    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.completion_status = 'completed'
    
    def mark_skipped(self) -> None:
        """Mark this task as skipped due to time or other constraints."""
        self.completion_status = 'skipped'
    
    def reset(self) -> None:
        """Reset task status back to pending for re-scheduling."""
        self.completion_status = 'pending'
    
    def __repr__(self) -> str:
        return f"Task({self.name}, {self.duration}min, priority={self.priority}, status={self.completion_status})"


class Pet:
    """Represents a pet with basic information and a list of care tasks."""
    
    def __init__(self, name: str, species: str, age: int):
        """
        Initialize a Pet.
        
        Args:
            name: The pet's name
            species: Type of pet (e.g., 'dog', 'cat', 'bird')
            age: The pet's age (in years)
        """
        self.name = name
        self.species = species
        self.age = age
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a new care task to this pet's routine."""
        self.tasks.append(task)
    
    def remove_task(self, task: Task) -> None:
        """Remove a care task from this pet's routine."""
        if task in self.tasks:
            self.tasks.remove(task)
    
    def get_tasks(self) -> List[Task]:
        """Return a list of all tasks for this pet."""
        return self.tasks
    
    def get_pending_tasks(self) -> List[Task]:
        """Return a list of only pending (unscheduled) tasks for this pet."""
        return [task for task in self.tasks if task.completion_status == 'pending']
    
    def __repr__(self) -> str:
        return f"Pet({self.name}, {self.species}, age={self.age}, tasks={len(self.tasks)})"


class Owner:
    """Represents a pet owner who manages multiple pets and time constraints."""
    
    def __init__(self, name: str, daily_time_available: int):
        """
        Initialize an Owner.
        
        Args:
            name: The owner's name
            daily_time_available: Total time available for pet care today (in minutes)
        """
        self.name = name
        self.daily_time_available = daily_time_available
        self.pets: List[Pet] = []
    
    def add_pet(self, pet: Pet) -> None:
        """Add a new pet to this owner's care."""
        self.pets.append(pet)
    
    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's care."""
        if pet in self.pets:
            self.pets.remove(pet)
    
    def get_pets(self) -> List[Pet]:
        """Return a list of all pets owned by this owner."""
        return self.pets
    
    def get_all_tasks(self) -> List[Task]:
        """Return a combined list of all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks
    
    def get_all_pending_tasks(self) -> List[Task]:
        """Return a combined list of all pending tasks from all pets."""
        all_pending = []
        for pet in self.pets:
            all_pending.extend(pet.get_pending_tasks())
        return all_pending
    
    def __repr__(self) -> str:
        return f"Owner({self.name}, {len(self.pets)} pet(s), {self.daily_time_available}min available)"


class Scheduler:
    """The brain that retrieves, organizes, and manages tasks across multiple pets."""
    
    def __init__(self, owner: Owner):
        """
        Initialize a Scheduler for an owner.
        
        Args:
            owner: Owner object whose pets and tasks will be scheduled
        """
        self.owner = owner
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.time_used = 0
        self.reasoning = ""
    
    def get_all_tasks_by_priority(self) -> List[Task]:
        """Retrieve and sort all pending tasks by priority (1=highest) and duration (shortest first)."""
        pending_tasks = self.owner.get_all_pending_tasks()
        # Sort by priority ascending (1 comes first), then by duration (shorter first)
        return sorted(pending_tasks, key=lambda t: (t.priority, t.duration))
    
    def generate_schedule(self) -> None:
        """Generate an optimized daily schedule using a greedy priority-based algorithm."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.time_used = 0
        self.reasoning = ""
        
        available_time = self.owner.daily_time_available
        sorted_tasks = self.get_all_tasks_by_priority()
        
        reasoning_lines = [
            f"Owner {self.owner.name} has {available_time} minutes available.",
            f"Scheduling across {len(self.owner.pets)} pet(s).",
            ""
        ]
        
        for task in sorted_tasks:
            if self.time_used + task.duration <= available_time:
                self.scheduled_tasks.append(task)
                self.time_used += task.duration
                reasoning_lines.append(
                    f"✓ {task.name} ({task.duration}min, priority {task.priority}) - SCHEDULED"
                )
            else:
                self.skipped_tasks.append(task)
                reasoning_lines.append(
                    f"✗ {task.name} ({task.duration}min, priority {task.priority}) - SKIPPED (not enough time)"
                )
        
        reasoning_lines.append("")
        reasoning_lines.append(f"Summary: {len(self.scheduled_tasks)} tasks scheduled, "
                              f"{len(self.skipped_tasks)} skipped. Time used: {self.time_used}/{available_time} minutes.")
        
        self.reasoning = "\n".join(reasoning_lines)
    
    def get_schedule_summary(self) -> dict:
        """Return a structured summary of the generated schedule with tasks, time usage, and reasoning."""
        return {
            'scheduled_tasks': self.scheduled_tasks,
            'skipped_tasks': self.skipped_tasks,
            'time_used': self.time_used,
            'time_available': self.owner.daily_time_available,
            'reasoning': self.reasoning
        }
    
    def reset_schedule(self) -> None:
        """Clear the current schedule and reset all task statuses to pending."""
        for task in self.scheduled_tasks + self.skipped_tasks:
            task.reset()
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.time_used = 0
        self.reasoning = ""
    
    def __repr__(self) -> str:
        return f"Scheduler(owner={self.owner.name}, scheduled={len(self.scheduled_tasks)}, skipped={len(self.skipped_tasks)})"

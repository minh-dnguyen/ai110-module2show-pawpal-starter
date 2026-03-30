"""
PawPal+ System Classes

Core classes for pet care planning and scheduling.
"""
from typing import List, Optional
from datetime import datetime, timedelta


class Task:
    """Represents a single pet care activity."""
    
    VALID_PRIORITIES = [1, 2, 3]  # 1=Essential/Medical, 2=Standard Care, 3=Bonus/Enrichment
    VALID_CATEGORIES = ['Feeding', 'Grooming', 'Exercise', 'Medical', 'Enrichment', 'Other']
    VALID_FREQUENCIES = ['daily', 'weekly', 'monthly', 'as_needed']
    VALID_STATUSES = ['pending', 'completed', 'skipped']
    
    def __init__(self, name: str, duration: int, priority: int, category: str, 
                 frequency: str = 'daily', completion_status: str = 'pending', scheduled_time: str = None,
                 due_date: datetime = None, owner_pet: 'Pet' = None):
        """
        Initialize a Task.
        
        Args:
            name: Task name (e.g., 'Morning Walk', 'Give Heartworm Meds')
            duration: How long the task takes (in minutes)
            priority: How critical (1 = Essential/Medical, 2 = Standard Care, 3 = Bonus/Enrichment)
            category: Task category (Feeding, Grooming, Exercise, Medical, Enrichment, Other)
            frequency: How often task occurs (daily, weekly, monthly, as_needed)
            completion_status: Current status (pending, completed, skipped)
            scheduled_time: Optional task time in HH:MM format (e.g., '07:30', '14:00')
            due_date: Optional datetime for when task is due (used for recurring tasks)
            owner_pet: Reference to the Pet object that owns this task (for conflict detection)
        
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
        self.scheduled_time = scheduled_time
        self.due_date = due_date or datetime.now()
        self.owner_pet = owner_pet
    
    def mark_completed(self) -> Optional['Task']:
        """
        Mark this task as completed.
        If the task is recurring (daily/weekly), automatically create and return the next occurrence.
        
        Returns:
            A new Task instance for the next occurrence (if recurring), or None
        """
        self.completion_status = 'completed'
        
        # If task is recurring, create next occurrence
        if self.frequency == 'daily':
            next_due_date = self.due_date + timedelta(days=1)
            next_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                frequency=self.frequency,
                completion_status='pending',
                scheduled_time=self.scheduled_time,
                due_date=next_due_date,
                owner_pet=self.owner_pet
            )
            return next_task
        elif self.frequency == 'weekly':
            next_due_date = self.due_date + timedelta(weeks=1)
            next_task = Task(
                name=self.name,
                duration=self.duration,
                priority=self.priority,
                category=self.category,
                frequency=self.frequency,
                completion_status='pending',
                scheduled_time=self.scheduled_time,
                due_date=next_due_date,
                owner_pet=self.owner_pet
            )
            return next_task
        
        return None
    
    def mark_skipped(self) -> None:
        """Mark this task as skipped due to time or other constraints."""
        self.completion_status = 'skipped'
    
    def reset(self) -> None:
        """Reset task status back to pending for re-scheduling."""
        self.completion_status = 'pending'
    
    def __repr__(self) -> str:
        time_str = f" @ {self.scheduled_time}" if self.scheduled_time else ""
        return f"Task({self.name}, {self.duration}min, priority={self.priority}, status={self.completion_status}{time_str})"


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
        task.owner_pet = self  # Set the task's owner reference
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
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by their scheduled_time attribute in HH:MM format.
        Tasks without scheduled_time are placed at the end.
        
        Args:
            tasks: List of Task objects to sort
        
        Returns:
            Sorted list of tasks by time (earliest first)
        """
        # Lambda key: (has_no_time, time_value)
        # Tasks with no time get (True, '') which sorts last
        # Tasks with time get (False, 'HH:MM') which sorts by time alphanumerically
        return sorted(tasks, key=lambda t: (t.scheduled_time is None, t.scheduled_time or ''))
    
    def filter_by_status(self, tasks: List[Task], status: str) -> List[Task]:
        """
        Filter tasks by their completion status.
        
        Args:
            tasks: List of Task objects to filter
            status: Status to filter by ('pending', 'completed', or 'skipped')
        
        Returns:
            List of tasks matching the given status
        """
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of {Task.VALID_STATUSES}")
        return [task for task in tasks if task.completion_status == status]
    
    def filter_by_pet(self, pet: Pet) -> List[Task]:
        """
        Filter tasks by pet name (get all tasks for a specific pet).
        
        Args:
            pet: Pet object to get tasks for
        
        Returns:
            List of all tasks for the given pet
        """
        return pet.get_tasks()
    
    def filter_tasks(self, status: str = None, pet: Pet = None) -> List[Task]:
        """
        Filter tasks by status and/or pet name.
        
        Args:
            status: Optional status filter ('pending', 'completed', or 'skipped')
            pet: Optional Pet object to filter by
        
        Returns:
            Filtered list of tasks matching all criteria
        """
        if pet is not None:
            tasks = self.filter_by_pet(pet)
        else:
            tasks = self.owner.get_all_tasks()
        
        if status is not None:
            tasks = self.filter_by_status(tasks, status)
        
        return tasks
    
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
    
    def detect_conflicts(self, tasks: List[Task] = None) -> List[tuple]:
        """
        Detect time conflicts among scheduled tasks.
        A conflict occurs when two tasks are scheduled at the same time.
        
        Args:
            tasks: Optional list of tasks to check. Defaults to scheduled_tasks.
        
        Returns:
            List of tuples: [(task1, task2, conflict_reason), ...]
            Empty list if no conflicts found.
        """
        if tasks is None:
            tasks = self.scheduled_tasks
        
        conflicts = []
        
        # O(n²) pairwise comparison - acceptable for 7-15 daily tasks
        for i, task1 in enumerate(tasks):
            for task2 in tasks[i+1:]:
                if self._has_time_overlap(task1, task2):
                    reason = self._get_conflict_reason(task1, task2)
                    conflicts.append((task1, task2, reason))
        
        return conflicts
    
    def _has_time_overlap(self, task1: Task, task2: Task) -> bool:
        """
        Check if two tasks have the same scheduled time.
        
        Args:
            task1: First task to compare
            task2: Second task to compare
        
        Returns:
            True if both tasks have times and they match, False otherwise
        """
        return (task1.scheduled_time and 
                task2.scheduled_time and 
                task1.scheduled_time == task2.scheduled_time)
    
    def _get_conflict_reason(self, task1: Task, task2: Task) -> str:
        """
        Determine the reason why two tasks conflict.
        Distinguishes between same-pet conflicts (critical) and cross-pet conflicts (warning).
        
        Args:
            task1: First task
            task2: Second task
        
        Returns:
            String describing the conflict reason
        """
        pet1_name = task1.owner_pet.name if task1.owner_pet else "Unknown"
        pet2_name = task2.owner_pet.name if task2.owner_pet else "Unknown"
        
        if pet1_name == pet2_name:
            return f"Same pet ({pet1_name}) scheduled at same time"
        elif pet1_name != "Unknown" and pet2_name != "Unknown":
            return f"Different pets at same time: {pet1_name} and {pet2_name}"
        else:
            return "Both tasks at same time"
    
    def get_conflict_warnings(self, tasks: List[Task] = None) -> str:
        """
        Generate human-readable warning messages for detected conflicts.
        Returns a formatted string summary rather than crashing.
        
        Args:
            tasks: Optional list of tasks to check. Defaults to scheduled_tasks.
        
        Returns:
            String with conflict warnings (empty if no conflicts)
        """
        conflicts = self.detect_conflicts(tasks)
        
        if not conflicts:
            return ""
        
        warning_lines = ["⚠️  TIME CONFLICT WARNINGS:"]
        for i, (task1, task2, reason) in enumerate(conflicts, 1):
            warning_lines.append(f"  {i}. {reason}")
            warning_lines.append(f"     → Task 1: {task1.name} @ {task1.scheduled_time}")
            warning_lines.append(f"     → Task 2: {task2.name} @ {task2.scheduled_time}")
        
        return "\n".join(warning_lines)
    
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

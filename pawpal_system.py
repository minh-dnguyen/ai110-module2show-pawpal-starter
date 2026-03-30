"""
PawPal+ System Classes

Core classes for pet care planning and scheduling.
"""


class Owner:
    """Represents a pet owner with time constraints."""
    
    def __init__(self, name: str, daily_time_available: int):
        """
        Initialize an Owner.
        
        Args:
            name: The owner's name
            daily_time_available: Total time available for pet care today (in minutes)
        """
        self.name = name
        self.daily_time_available = daily_time_available


class Pet:
    """Represents a pet with basic information."""
    
    def __init__(self, name: str, species: str, age: int):
        """
        Initialize a Pet.
        
        Args:
            name: The pet's name
            species: Type of pet (e.g., 'dog', 'cat')
            age: The pet's age
        """
        self.name = name
        self.species = species
        self.age = age


class Task:
    """Represents a single pet care task."""
    
    def __init__(self, name: str, duration: int, priority: int, category: str):
        """
        Initialize a Task.
        
        Args:
            name: Task name (e.g., 'Morning Walk', 'Give Heartworm Meds')
            duration: How long the task takes (in minutes)
            priority: How critical the task is (1 = Essential/Medical, 2 = Standard Care, 3 = Bonus/Enrichment)
            category: Task category (e.g., 'Feeding', 'Grooming', 'Exercise', 'Medical')
        """
        self.name = name
        self.duration = duration
        self.priority = priority
        self.category = category


class DailyPlan:
    """Orchestrates scheduling logic and holds the daily plan results."""
    
    def __init__(self):
        """Initialize an empty DailyPlan."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.time_used = 0
        self.reasoning = ""
    
    def generate_schedule(self, available_time: int, task_list: list) -> None:
        """
        Generate an optimized daily schedule based on available time and task priorities.
        
        Args:
            available_time: Total minutes available for pet care
            task_list: List of Task objects to schedule
        """
        pass

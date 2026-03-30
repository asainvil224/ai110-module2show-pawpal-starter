class Owner:
    def __init__(self, name, available_time, preferences):
        self.name = name
        self.available_time = available_time  # e.g., hours per day
        self.preferences = preferences  # dict of preferences
        self.pets = []  # list of Pet objects
        self.task_manager = TaskManager()  # each owner has their own task manager

    def update_preferences(self, new_preferences):
        pass

    def get_available_time(self):
        pass

    def add_pet(self, pet):
        self.pets.append(pet)

    def get_pets(self):
        return self.pets


class Pet:
    def __init__(self, name, pet_type, age, special_needs):
        self.name = name
        self.pet_type = pet_type  # e.g., dog, cat
        self.age = age
        self.special_needs = special_needs  # list of special care needs
        self.tasks = []  # list of Task objects

    def add_special_need(self, need):
        pass

    def get_special_needs(self):
        pass

    def add_task(self, task):
        self.tasks.append(task)

    def task_count(self):
        return len(self.tasks)


class Task:
    def __init__(self, name, duration, priority, pet, time_constraints=None):
        self.name = name
        self.duration = duration  # in minutes
        self.priority = priority  # e.g., 1 (high), 2 (medium), 3 (low)
        self.pet = pet  # reference to Pet object
        self.time_constraints = time_constraints  # optional dict or list
        self.status = "pending"  # pending or completed

    def is_feasible(self, available_time):
        pass

    def update_duration(self, new_duration):
        pass

    def mark_complete(self):
        self.status = "completed"


class TaskManager:
    def __init__(self):
        self.tasks = []  # list of Task objects

    def add_task(self, task):
        self.tasks.append(task)

    def edit_task(self, task_id, updated_task):
        if 0 <= task_id < len(self.tasks):
            self.tasks[task_id] = updated_task

    def remove_task(self, task_id):
        if 0 <= task_id < len(self.tasks):
            self.tasks.pop(task_id)

    def get_tasks(self):
        return self.tasks

    def get_task_by_id(self, task_id):
        if 0 <= task_id < len(self.tasks):
            return self.tasks[task_id]
        return None


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def generate_schedule(self, date=None):
        # Simple implementation: include all tasks
        schedule = Schedule(self.owner, date)
        tasks = self.owner.task_manager.get_tasks()
        for task in tasks:
            schedule.add_task(task)
        return schedule

    def prioritize_tasks(self, tasks):
        pass

    def fit_tasks_in_time(self, tasks, available_time):
        pass


class Schedule:
    def __init__(self, owner, date):
        self.owner = owner  # reference to Owner
        self.date = date  # date for the schedule
        self.selected_tasks = []  # list of selected Task objects
        self.total_time = 0  # total time in minutes

    def add_task(self, task):
        self.selected_tasks.append(task)
        self.total_time += task.duration

    def remove_task(self, task_id):
        if 0 <= task_id < len(self.selected_tasks):
            removed_task = self.selected_tasks.pop(task_id)
            self.total_time -= removed_task.duration

    def get_total_time(self):
        return self.total_time

    def get_selected_tasks(self):
        return self.selected_tasks


class AppController:
    def __init__(self, owner):
        self.owner = owner
        self.scheduler = Scheduler(owner)  # scheduler uses owner

    def create_schedule(self, date=None):
        return self.scheduler.generate_schedule(date)

    def update_owner(self, new_owner_info):
        # Simple update, assuming new_owner_info is a dict
        for key, value in new_owner_info.items():
            if hasattr(self.owner, key):
                setattr(self.owner, key, value)

    def add_task(self, task):
        self.owner.task_manager.add_task(task)

    def get_schedule(self, date):
        return self.create_schedule(date)
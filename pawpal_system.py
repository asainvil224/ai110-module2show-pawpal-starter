import datetime
from datetime import timedelta

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
        pet.owner = self

    def get_pets(self):
        return self.pets


class Pet:
    def __init__(self, name, pet_type, age, special_needs):
        self.name = name
        self.pet_type = pet_type  # e.g., dog, cat
        self.age = age
        self.special_needs = special_needs  # list of special care needs
        self.tasks = []  # list of Task objects
        self.owner = None

    def add_special_need(self, need):
        pass

    def get_special_needs(self):
        pass

    def add_task(self, task):
        self.tasks.append(task)

    def task_count(self):
        return len(self.tasks)


class Task:
    def __init__(self, name, duration, priority, pet, time_constraints=None, recurrence=None, scheduled_date=None):
        self.name = name
        self.duration = duration  # in minutes
        self.priority = priority  # e.g., 1 (high), 2 (medium), 3 (low)
        self.pet = pet  # reference to Pet object
        self.time_constraints = time_constraints  # optional dict or list
        self.status = "pending"  # pending or completed
        self.recurrence = recurrence  # 'daily', 'weekly', or None
        self.scheduled_date = scheduled_date  # datetime.date
        self.start_time = None  # datetime.time, assigned by scheduler

    def is_feasible(self, available_time):
        pass

    def update_duration(self, new_duration):
        pass

    def mark_complete(self):
        self.status = "completed"
        if self.recurrence and self.pet.owner:
            task_manager = self.pet.owner.task_manager
            if self.recurrence == 'daily':
                next_date = self.scheduled_date + timedelta(days=1)
            elif self.recurrence == 'weekly':
                next_date = self.scheduled_date + timedelta(days=7)
            new_task = Task(self.name, self.duration, self.priority, self.pet, self.time_constraints, self.recurrence, next_date)
            task_manager.add_task(new_task)


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

    def filter_tasks(self, status=None, pet_name=None):
        filtered = self.tasks
        if status:
            filtered = [t for t in filtered if t.status == status]
        if pet_name:
            filtered = [t for t in filtered if t.pet.name == pet_name]
        return filtered

    def sort_tasks(self, by='priority', reverse=False):
        if by == 'priority':
            self.tasks.sort(key=lambda t: t.priority, reverse=reverse)
        elif by == 'duration':
            self.tasks.sort(key=lambda t: t.duration, reverse=reverse)
        elif by == 'name':
            self.tasks.sort(key=lambda t: t.name, reverse=reverse)


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def generate_schedule(self, date=None):
        if date is None:
            date = datetime.date.today()
        schedule = Schedule(self.owner, date)
        # Filter pending tasks and sort by priority
        pending_tasks = [t for t in self.owner.task_manager.get_tasks() if t.status == "pending"]
        pending_tasks.sort(key=lambda t: t.priority)
        # Fit tasks within available time (convert hours to minutes)
        available_minutes = self.owner.available_time * 60
        current_time = datetime.time(9, 0)
        for task in pending_tasks:
            if schedule.get_total_time() + task.duration <= available_minutes:
                task.scheduled_date = date
                task.start_time = current_time
                schedule.add_task(task)
                current_time = self._add_minutes_to_time(current_time, task.duration)
        return schedule

    def _add_minutes_to_time(self, start_time, minutes):
        """Helper to add minutes to a time object."""
        total_minutes = start_time.hour * 60 + start_time.minute + minutes
        new_hour = total_minutes // 60
        new_minute = total_minutes % 60
        return datetime.time(new_hour, new_minute)

    def prioritize_tasks(self, tasks):
        pass

    def fit_tasks_in_time(self, tasks, available_time):
        pass

    def detect_conflicts(self, schedule):
        conflicts = []
        tasks = schedule.selected_tasks
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                t1 = tasks[i]
                t2 = tasks[j]
                if t1.scheduled_date == t2.scheduled_date and t1.start_time and t2.start_time:
                    # calculate end times
                    t1_start_dt = datetime.datetime.combine(t1.scheduled_date, t1.start_time)
                    t1_end_dt = t1_start_dt + timedelta(minutes=t1.duration)
                    t2_start_dt = datetime.datetime.combine(t2.scheduled_date, t2.start_time)
                    t2_end_dt = t2_start_dt + timedelta(minutes=t2.duration)
                    # check overlap
                    if t1_start_dt < t2_end_dt and t2_start_dt < t1_end_dt:
                        same_pet = t1.pet.name == t2.pet.name
                        conflicts.append({
                            'task1': t1.name,
                            'task2': t2.name,
                            'same_pet': same_pet,
                            'pet1': t1.pet.name,
                            'pet2': t2.pet.name
                        })
        return conflicts


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
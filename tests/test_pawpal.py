import pytest
from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta, time


def test_task_mark_complete_changes_status():
	pet = Pet("Buddy", "Dog", 3, ["Needs daily walks"])
	task = Task("Walk Buddy", 30, 1, pet)
	assert task.status == "pending"
	task.mark_complete()
	assert task.status == "completed"


def test_adding_task_to_pet_increases_task_count():
	pet = Pet("Whiskers", "Cat", 2, ["Litter box cleaning"])
	assert pet.task_count() == 0
	task1 = Task("Feed Whiskers", 10, 2, pet)
	pet.add_task(task1)
	assert pet.task_count() == 1
	task2 = Task("Clean Litter", 15, 1, pet)
	pet.add_task(task2)
	assert pet.task_count() == 2


def test_tasks_returned_in_chronological_order():
    owner = Owner("John", 4, {})
    pet = Pet("Buddy", "Dog", 3, [])
    owner.add_pet(pet)
    task1 = Task("Task A", 30, 2, pet)
    task2 = Task("Task B", 20, 1, pet)  # Higher priority
    owner.task_manager.add_task(task1)
    owner.task_manager.add_task(task2)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule(date.today())
    # Tasks should be in order of start time: task2 first (priority 1), then task1
    assert len(schedule.selected_tasks) == 2
    assert schedule.selected_tasks[0].start_time <= schedule.selected_tasks[1].start_time


def test_marking_daily_task_complete_creates_new_task_next_day():
    owner = Owner("John", 4, {})
    pet = Pet("Buddy", "Dog", 3, [])
    owner.add_pet(pet)
    today = date.today()
    task = Task("Daily Walk", 30, 1, pet, recurrence='daily', scheduled_date=today)
    owner.task_manager.add_task(task)
    initial_task_count = len(owner.task_manager.get_tasks())
    task.mark_complete()
    # Should create a new task for tomorrow
    new_tasks = owner.task_manager.get_tasks()
    assert len(new_tasks) == initial_task_count + 1
    new_task = new_tasks[-1]  # Last added
    assert new_task.name == "Daily Walk"
    assert new_task.scheduled_date == today + timedelta(days=1)
    assert new_task.status == "pending"


def test_scheduler_flags_duplicate_times():
    owner = Owner("John", 4, {})
    pet1 = Pet("Buddy", "Dog", 3, [])
    pet2 = Pet("Whiskers", "Cat", 2, [])
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    today = date.today()
    task1 = Task("Walk Buddy", 60, 1, pet1, scheduled_date=today)
    task2 = Task("Feed Cat", 30, 2, pet2, scheduled_date=today)
    owner.task_manager.add_task(task1)
    owner.task_manager.add_task(task2)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_schedule(today)
    # Manually set overlapping times
    schedule.selected_tasks[0].start_time = time(9, 0)
    schedule.selected_tasks[1].start_time = time(9, 30)  # Overlaps with task1
    conflicts = scheduler.detect_conflicts(schedule)
    assert len(conflicts) > 0
    assert "Walk Buddy" in conflicts[0]['task1'] or conflicts[0]['task2']
    assert "Feed Cat" in conflicts[0]['task1'] or conflicts[0]['task2']

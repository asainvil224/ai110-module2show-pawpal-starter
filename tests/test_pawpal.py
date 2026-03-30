import pytest
from pawpal_system import Owner, Pet, Task


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

from pawpal_system import Owner, Pet, Task, AppController
from datetime import date, time

# Create an Owner
owner = Owner("John Doe", 4, {"morning_person": True})  # 4 hours available

# Create two Pets
pet1 = Pet("Buddy", "Dog", 3, ["Needs daily walks"])
pet2 = Pet("Whiskers", "Cat", 2, ["Litter box cleaning"])

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create three Tasks with different durations
task1 = Task("Walk Buddy", 30, 1, pet1)  # 30 min, high priority
task2 = Task("Feed Whiskers", 10, 2, pet2)  # 10 min, medium priority
task3 = Task("Play with Buddy", 45, 1, pet1)  # 45 min, high priority

# Create AppController
app = AppController(owner)

# Add tasks out of order
app.add_task(task3)  # Add task3 first
app.add_task(task1)  # Then task1
app.add_task(task2)  # Then task2

# Mark task1 as complete
task1.mark_complete()

# Sort tasks by priority
owner.task_manager.sort_tasks(by='priority')

# Generate today's schedule
today = date.today()
schedule = app.get_schedule(today)

# Manually set overlapping times for testing conflicts
schedule.selected_tasks[0].start_time = time(9, 0)  # task3 starts at 9:00
schedule.selected_tasks[1].start_time = time(9, 30)  # task1 starts at 9:30, overlaps with task3

# Detect conflicts
conflicts = app.scheduler.detect_conflicts(schedule)
if conflicts:
    print("\nConflicts detected:")
    for conflict in conflicts:
        print(f"- {conflict['task1']} and {conflict['task2']} overlap. Same pet: {conflict['same_pet']}")
else:
    print("\nNo conflicts detected.")

# Print Today's Schedule
print("Today's Schedule (sorted by priority):")
for task in schedule.get_selected_tasks():
    print(f"- {task.name} for {task.pet.name} ({task.pet.pet_type}): {task.duration} minutes, Priority: {task.priority}, Status: {task.status}")
print(f"Total time: {schedule.get_total_time()} minutes")

# Filter and print completed tasks
completed_tasks = owner.task_manager.filter_tasks(status='completed')
print("\nCompleted Tasks:")
for task in completed_tasks:
    print(f"- {task.name} for {task.pet.name}")

# Filter and print tasks for Buddy
buddy_tasks = owner.task_manager.filter_tasks(pet_name='Buddy')
print("\nTasks for Buddy:")
for task in buddy_tasks:
    print(f"- {task.name}: {task.duration} minutes, Status: {task.status}")

# Filter and print completed tasks for Buddy
completed_buddy_tasks = owner.task_manager.filter_tasks(status='completed', pet_name='Buddy')
print("\nCompleted Tasks for Buddy:")
for task in completed_buddy_tasks:
    print(f"- {task.name}: {task.duration} minutes")
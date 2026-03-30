from pawpal_system import Owner, Pet, Task, AppController
from datetime import date

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

# Add tasks
app.add_task(task1)
app.add_task(task2)
app.add_task(task3)

# Generate today's schedule
today = date.today()
schedule = app.get_schedule(today)

# Print Today's Schedule
print("Today's Schedule:")
for task in schedule.get_selected_tasks():
    print(f"- {task.name} for {task.pet.name} ({task.pet.pet_type}): {task.duration} minutes")
print(f"Total time: {schedule.get_total_time()} minutes")
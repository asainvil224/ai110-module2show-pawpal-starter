import streamlit as st
from pawpal_system import Owner, Pet, Task, AppController

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "owner" not in st.session_state:
    # initial owner object in session state for reuse across interactions
    st.session_state.owner = Owner(owner_name, 120, {"morning_person": True})
    st.session_state.owner.add_pet(Pet(pet_name, species, 2, []))

else:
    # if owner exists in state, keep current pet task inputs only
    # if user changes the owner/pet inputs manually, we can update.
    st.session_state.owner.name = owner_name
    # note: we do not fully recreate to avoid wiping existing schedules

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add pet"):
    # Add pet via owner.add_pet() method
    new_pet = Pet(pet_name, species, 2, [])
    if pet_name and species:
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added pet {pet_name} ({species})")

pet_names = [p.name for p in st.session_state.owner.pets] if st.session_state.owner.pets else []

selected_pet_name = st.selectbox("Select pet for task", pet_names or [pet_name])
selected_pet = next((p for p in st.session_state.owner.pets if p.name == selected_pet_name), st.session_state.owner.pets[0] if st.session_state.owner.pets else None)

if st.button("Add task"):
    # Create a Task object and add to task manager + pet
    priority_map = {"high": 1, "medium": 2, "low": 3}
    task_obj = Task(task_title or "Untitled", int(duration), priority_map.get(priority, 3), selected_pet)
    st.session_state.owner.task_manager.add_task(task_obj)
    if selected_pet:
        selected_pet.add_task(task_obj)
    st.session_state.tasks.append({"title": task_title, "duration_minutes": int(duration), "priority": priority})
    st.success(f"Added task {task_title} to {selected_pet.name if selected_pet else 'no pet'}")

if st.session_state.tasks:
    st.write("Current tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    # Build a simple runtime owner/pet/task schedule using the backend classes.
    demo_owner = st.session_state.owner

    # use already stored Task objects in owner's TaskManager
    # scheduler will read these. no rebuild required.

    controller = AppController(demo_owner)
    schedule = controller.get_schedule(date=None)

    # Check for conflicts using Scheduler's detect_conflicts method
    conflicts = controller.scheduler.detect_conflicts(schedule)
    if conflicts:
        st.warning("⚠️ Scheduling Conflicts Detected")
        with st.expander("View Conflict Details"):
            for conflict in conflicts:
                st.write(f"• **{conflict['task1']}** (Pet: {conflict['pet1']}) and **{conflict['task2']}** (Pet: {conflict['pet2']}) overlap in time.")
                if conflict['same_pet']:
                    st.write("   _Note: Both tasks are for the same pet, which may not be feasible._")
    else:
        st.success("✅ Schedule Generated Successfully - No Conflicts Detected")

    # Display schedule summary
    total_minutes = schedule.get_total_time()
    num_tasks = len(schedule.get_selected_tasks())
    available_hours = demo_owner.available_time

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Scheduled Time", f"{total_minutes} min")
    with col2:
        st.metric("Number of Tasks", num_tasks)
    with col3:
        st.metric("Available Time", f"{available_hours} hours")

    st.subheader("📅 Today's Schedule")
    st.caption("Tasks are sorted by priority and fit within your available time, starting at 9:00 AM.")

    if schedule.get_selected_tasks():
        rows = []
        for task in schedule.get_selected_tasks():
            start_time_str = task.start_time.strftime("%H:%M") if task.start_time else "N/A"
            priority_label = {1: "High", 2: "Medium", 3: "Low"}.get(task.priority, "Unknown")
            rows.append(
                {
                    "Task": task.name,
                    "Pet": task.pet.name,
                    "Duration (min)": task.duration,
                    "Priority": priority_label,
                    "Start Time": start_time_str,
                    "Status": task.status.capitalize(),
                }
            )
        st.table(rows)
    else:
        st.info("No pending tasks to schedule for today.")

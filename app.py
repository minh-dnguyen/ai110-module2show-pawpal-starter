import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ============================================================================
# Session State Initialization
# ============================================================================
# Initialize Owner in session_state (persists across page refreshes)
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", daily_time_available=120)

if "selected_pet_idx" not in st.session_state:
    st.session_state.selected_pet_idx = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+, your pet care planning assistant!

This app helps you manage multiple pets and create optimized daily schedules based on time constraints and task priorities.
"""
)

st.divider()

# ============================================================================
# Owner Setup Section
# ============================================================================
st.subheader("👤 Owner Setup")
col1, col2 = st.columns(2)

with col1:
    new_owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
    if new_owner_name != st.session_state.owner.name:
        st.session_state.owner.name = new_owner_name

with col2:
    new_time_available = st.number_input(
        "Daily time available (minutes)",
        min_value=15,
        max_value=480,
        value=st.session_state.owner.daily_time_available
    )
    if new_time_available != st.session_state.owner.daily_time_available:
        st.session_state.owner.daily_time_available = new_time_available

st.info(f"📋 {st.session_state.owner.name} has {st.session_state.owner.daily_time_available} minutes available daily.")
st.divider()

# ============================================================================
# Pet Management Section
# ============================================================================
st.subheader("🐾 Manage Pets")

# Add Pet Form
col1, col2, col3 = st.columns(3)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
with col3:
    pet_age = st.number_input("Pet age (years)", min_value=0, max_value=50, value=3)

if st.button("➕ Add Pet"):
    # Create new pet and add to owner
    new_pet = Pet(name=pet_name, species=species, age=pet_age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"✅ Added {pet_name} the {species}!")
    st.session_state.selected_pet_idx = len(st.session_state.owner.get_pets()) - 1

# Display current pets
pets = st.session_state.owner.get_pets()
if pets:
    st.markdown("**Current Pets:**")
    for idx, pet in enumerate(pets):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"🐾 {pet.name} ({pet.species}, age {pet.age}) — {len(pet.get_tasks())} task(s)")
        with col2:
            if st.button("Select", key=f"select_pet_{idx}"):
                st.session_state.selected_pet_idx = idx
else:
    st.info("No pets yet. Add one above!")

st.divider()

# ============================================================================
# Task Management Section
# ============================================================================
if pets:
    st.subheader("📋 Manage Tasks")
    
    # Select which pet to add tasks to
    selected_idx = st.session_state.selected_pet_idx
    if selected_idx is None or selected_idx >= len(pets):
        selected_idx = 0
    
    selected_pet = pets[selected_idx]
    st.markdown(f"**Adding tasks for: {selected_pet.name}**")
    
    # Task input form
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_name = st.text_input("Task name", value="Morning walk")
    with col2:
        task_duration = st.number_input("Duration (min)", min_value=1, max_value=240, value=20)
    with col3:
        task_priority = st.selectbox("Priority", [1, 2, 3], index=0, format_func=lambda x: f"Level {x} {'🔴' if x==1 else '🟡' if x==2 else '🟢'}")
    with col4:
        task_category = st.selectbox("Category", ["Feeding", "Exercise", "Grooming", "Medical", "Enrichment"])
    
    if st.button("➕ Add Task"):
        try:
            # Create new task and add to selected pet
            new_task = Task(
                name=task_name,
                duration=task_duration,
                priority=task_priority,
                category=task_category
            )
            selected_pet.add_task(new_task)
            st.success(f"✅ Added '{task_name}' to {selected_pet.name}!")
        except ValueError as e:
            st.error(f"❌ Error adding task: {e}")
    
    # Display tasks for selected pet
    tasks = selected_pet.get_tasks()
    if tasks:
        st.markdown(f"**Tasks for {selected_pet.name}:**")
        task_data = []
        for task in tasks:
            task_data.append({
                "Task": task.name,
                "Duration (min)": task.duration,
                "Priority": f"Level {task.priority}",
                "Category": task.category,
                "Status": task.completion_status
            })
        st.dataframe(task_data, use_container_width=True)
    else:
        st.info(f"No tasks yet for {selected_pet.name}. Add one above!")
    
    st.divider()
    
    # ============================================================================
    # Schedule Generation Section
    # ============================================================================
    st.subheader("📅 Generate Daily Schedule")
    
    if st.button("🚀 Generate Schedule", type="primary"):
        # Create scheduler and generate schedule
        scheduler = Scheduler(st.session_state.owner)
        scheduler.generate_schedule()
        summary = scheduler.get_schedule_summary()
        
        # Display schedule results
        st.markdown("### Daily Schedule")
        st.markdown(summary['reasoning'])
        
        if summary['scheduled_tasks']:
            st.markdown("#### ✅ Scheduled Tasks")
            scheduled_data = []
            for task in summary['scheduled_tasks']:
                scheduled_data.append({
                    "Task": task.name,
                    "Pet": next((p.name for p in pets if task in p.get_tasks()), "Unknown"),
                    "Duration (min)": task.duration,
                    "Priority": f"Level {task.priority}",
                    "Category": task.category
                })
            st.dataframe(scheduled_data, use_container_width=True)
        
        if summary['skipped_tasks']:
            st.markdown("#### ⏭️ Skipped Tasks (insufficient time)")
            skipped_data = []
            for task in summary['skipped_tasks']:
                skipped_data.append({
                    "Task": task.name,
                    "Pet": next((p.name for p in pets if task in p.get_tasks()), "Unknown"),
                    "Duration (min)": task.duration,
                    "Priority": f"Level {task.priority}",
                    "Category": task.category
                })
            st.dataframe(skipped_data, use_container_width=True)
        
        st.markdown(f"### Time Summary")
        st.metric("Time Used", f"{summary['time_used']} min", f"of {summary['time_available']} available")


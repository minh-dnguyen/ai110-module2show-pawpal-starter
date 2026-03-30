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
            priority_icon = "🔴 Critical" if task.priority == 1 else "🟡 Standard" if task.priority == 2 else "🟢 Bonus"
            status_icon = "✅ Pending" if task.completion_status == "pending" else "⏭️ Skipped" if task.completion_status == "skipped" else "✓ Completed"
            
            task_data.append({
                "Task": task.name,
                "Duration": f"{task.duration} min",
                "Priority": priority_icon,
                "Category": task.category,
                "Status": status_icon
            })
        st.table(task_data)
    else:
        st.info(f"No tasks yet for {selected_pet.name}. Add one above!")
    
    st.divider()
    
    # ============================================================================
    # Advanced Tasks Viewer (Using Scheduler Methods)
    # ============================================================================
    st.subheader("🔍 View & Sort Tasks")
    
    view_tab1, view_tab2 = st.tabs(["All Tasks by Priority", "Tasks by Pet"])
    
    with view_tab1:
        st.markdown("**All tasks sorted by Priority (Highest → Lowest) then Duration (Shortest → Longest)**")
        if st.session_state.owner.get_all_tasks():
            # Use Scheduler method to sort by priority
            scheduler_preview = Scheduler(st.session_state.owner)
            priority_sorted = scheduler_preview.get_all_tasks_by_priority()
            
            view_data = []
            for task in priority_sorted:
                pet_owner = next((p.name for p in pets if task in p.get_tasks()), "Unknown")
                priority_icon = "🔴" if task.priority == 1 else "🟡" if task.priority == 2 else "🟢"
                category_icon = {
                    "Feeding": "🍽️",
                    "Exercise": "🏃",
                    "Grooming": "✂️",
                    "Medical": "💊",
                    "Enrichment": "🎾",
                    "Other": "📋"
                }.get(task.category, "📋")
                
                view_data.append({
                    "Priority": f"{priority_icon} Level {task.priority}",
                    "Task": task.name,
                    "Pet": pet_owner,
                    "Duration": f"{task.duration} min",
                    "Category": f"{category_icon} {task.category}",
                    "Status": "✅ Pending" if task.completion_status == "pending" else "⏭️ Skipped" if task.completion_status == "skipped" else "✓ Completed"
                })
            st.table(view_data)
            
            # Summary statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Tasks", len(scheduler_preview.owner.get_all_tasks()))
            with col2:
                total_time = sum(t.duration for t in scheduler_preview.owner.get_all_tasks())
                st.metric("Total Time Needed", f"{total_time} min")
            with col3:
                pending_tasks = len(scheduler_preview.owner.get_all_pending_tasks())
                st.metric("Pending Tasks", pending_tasks)
        else:
            st.info("No tasks yet. Add tasks to view them here.")
    
    with view_tab2:
        st.markdown("**View tasks grouped by each pet**")
        for pet in pets:
            pet_tasks = pet.get_tasks()
            if pet_tasks:
                st.markdown(f"##### {pet.name} 🐾")
                pet_view_data = []
                for task in pet_tasks:
                    priority_icon = "🔴" if task.priority == 1 else "🟡" if task.priority == 2 else "🟢"
                    pet_view_data.append({
                        "Priority": f"{priority_icon} Level {task.priority}",
                        "Task": task.name,
                        "Duration": f"{task.duration} min",
                        "Category": task.category,
                        "Status": "✅ Pending" if task.completion_status == "pending" else "⏭️ Skipped" if task.completion_status == "skipped" else "✓ Completed"
                    })
                st.table(pet_view_data)
            else:
                st.markdown(f"##### {pet.name} 🐾")
                st.info(f"No tasks for {pet.name} yet.")
    
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
        
        # ====== AUTOMATED CONFLICT DETECTION & WARNINGS ======
        conflicts = scheduler.detect_conflicts()
        if conflicts:
            st.warning("⚠️ **TIME CONFLICTS DETECTED!**")
            conflict_details = []
            for task1, task2, reason in conflicts:
                pet1 = next((p.name for p in pets if task1 in p.get_tasks()), "Unknown")
                pet2 = next((p.name for p in pets if task2 in p.get_tasks()), "Unknown")
                is_same_pet = pet1 == pet2
                
                conflict_type = "🔴 **CRITICAL**" if is_same_pet else "🟡 **WARNING**"
                conflict_details.append({
                    "Type": conflict_type,
                    "Reason": reason,
                    "Task 1": f"{task1.name} ({pet1}) @ {task1.scheduled_time}",
                    "Task 2": f"{task2.name} ({pet2}) @ {task2.scheduled_time}"
                })
            
            st.table(conflict_details)
            st.info(
                "💡 **Tip:** Reschedule conflicting tasks to different times, or consider which tasks "
                "are truly necessary for this pet today."
            )
        else:
            st.success("✅ No time conflicts detected!")
        
        st.divider()
        
        # ====== DISPLAY SCHEDULED TASKS (sorted by priority & time) ======
        if summary['scheduled_tasks']:
            st.markdown("### ✅ **Scheduled Tasks** (Prioritized Schedule)")
            
            # Sort by priority then by duration for optimal display
            sorted_scheduled = scheduler.get_all_tasks_by_priority()
            sorted_scheduled = [t for t in sorted_scheduled if t in summary['scheduled_tasks']]
            
            scheduled_data = []
            for task in sorted_scheduled:
                pet_owner = next((p.name for p in pets if task in p.get_tasks()), "Unknown")
                priority_emoji = "🔴" if task.priority == 1 else "🟡" if task.priority == 2 else "🟢"
                category_emoji = {
                    "Feeding": "🍽️",
                    "Exercise": "🏃",
                    "Grooming": "✂️",
                    "Medical": "💊",
                    "Enrichment": "🎾",
                    "Other": "📋"
                }.get(task.category, "📋")
                
                scheduled_data.append({
                    "Priority": f"{priority_emoji} Level {task.priority}",
                    "Task": task.name,
                    "Pet": pet_owner,
                    "Duration": f"{task.duration} min",
                    "Category": f"{category_emoji} {task.category}",
                    "Time": task.scheduled_time or "Flexible"
                })
            
            st.table(scheduled_data)
            st.success(
                f"🎉 **Great news!** {len(summary['scheduled_tasks'])} task(s) fit into the schedule. "
                f"Total time: **{summary['time_used']} minutes**"
            )
        else:
            st.info("No tasks scheduled yet. Add tasks to get started!")
        
        # ====== DISPLAY SKIPPED TASKS ======
        if summary['skipped_tasks']:
            st.divider()
            st.markdown("### ⏭️ **Skipped Tasks** (Insufficient Time)")
            
            skipped_data = []
            for task in summary['skipped_tasks']:
                pet_owner = next((p.name for p in pets if task in p.get_tasks()), "Unknown")
                priority_emoji = "🔴" if task.priority == 1 else "🟡" if task.priority == 2 else "🟢"
                category_emoji = {
                    "Feeding": "🍽️",
                    "Exercise": "🏃",
                    "Grooming": "✂️",
                    "Medical": "💊",
                    "Enrichment": "🎾",
                    "Other": "📋"
                }.get(task.category, "📋")
                
                skipped_data.append({
                    "Priority": f"{priority_emoji} Level {task.priority}",
                    "Task": task.name,
                    "Pet": pet_owner,
                    "Duration": f"{task.duration} min",
                    "Category": f"{category_emoji} {task.category}",
                    "Reason": "Not enough time today"
                })
            
            st.table(skipped_data)
            st.warning(
                f"⏰ **Not enough time** for {len(summary['skipped_tasks'])} task(s). "
                f"Consider increasing available time or prioritizing critical tasks."
            )
        
        # ====== TIME SUMMARY & STATISTICS ======
        st.divider()
        st.markdown("### 📊 **Schedule Summary**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Scheduled",
                len(summary['scheduled_tasks']),
                f"{len(summary['scheduled_tasks'])} tasks"
            )
        with col2:
            st.metric(
                "Time Used",
                f"{summary['time_used']}m",
                f"of {summary['time_available']} available"
            )
        with col3:
            remaining = summary['time_available'] - summary['time_used']
            st.metric(
                "Time Remaining",
                f"{remaining}m",
                "Spare time ✨" if remaining > 0 else "Over time ⚠️"
            )
        with col4:
            utilization = round((summary['time_used'] / summary['time_available']) * 100, 1)
            st.metric(
                "Utilization",
                f"{utilization}%",
                delta=None
            )
        
        # Time breakdown by priority
        st.markdown("#### Time Breakdown by Priority Level")
        priority_time = {1: 0, 2: 0, 3: 0}
        for task in summary['scheduled_tasks']:
            priority_time[task.priority] += task.duration
        
        breakdown_data = [
            {"Priority Level": "1 - Essential/Medical 🔴", "Time (min)": priority_time[1]},
            {"Priority Level": "2 - Standard Care 🟡", "Time (min)": priority_time[2]},
            {"Priority Level": "3 - Bonus/Enrichment 🟢", "Time (min)": priority_time[3]},
        ]
        st.table(breakdown_data)
        
        st.markdown("---")
        st.markdown("**📋 Detailed Reasoning:**")
        st.info(summary['reasoning'])


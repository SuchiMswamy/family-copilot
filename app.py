
import streamlit as st
import streamlit.components.v1 as components
from datetime import date, datetime
import uuid
import html

st.set_page_config(
    page_title="Our Family Hub",
    page_icon="🏡",
    layout="wide",
)

# -------------------- SESSION STATE --------------------

defaults = {
    "tasks": [],
    "groceries": [],
    "appointments": [],
    "notes": [],
    "reaction": "welcome",
    "reaction_message": "Welcome home! Let's make today a happy one.",
    "theme": "Pastel",
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def react(kind, message):
    st.session_state.reaction = kind
    st.session_state.reaction_message = message


# -------------------- STYLING --------------------

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #fff8f1, #f5f0ff, #eefaff);
    }
    .block-container {
        padding-top: 1.6rem;
        max-width: 1200px;
    }
    .hero {
        padding: 1.5rem;
        border-radius: 25px;
        background: linear-gradient(120deg, #ffe1ec, #e7e2ff, #dff7ff);
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 8px 24px #6b558018;
    }
    .hero h1 {
        color: #48385e;
        margin-bottom: .2rem;
    }
    .hero p {
        color: #675b79;
        margin-bottom: 0;
    }
    .panel {
        background: rgba(255,255,255,.85);
        border: 1px solid #eee5f4;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        margin: .4rem 0 1rem 0;
        box-shadow: 0 4px 15px #6b558010;
    }
    .task-done {
        color: #32866a;
        text-decoration: line-through;
        opacity: .7;
    }
    .small-muted {
        color: #776d83;
        font-size: .88rem;
    }
    div.stButton > button {
        border-radius: 12px;
    }

    /* Animated cartoon family */
    .scene {
        height: 230px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        position: relative;
        border-radius: 20px;
        background: linear-gradient(#fff4fa, #f1edff);
        margin: .8rem 0;
    }
    .sparkle {
        position: absolute;
        font-size: 24px;
        animation: twinkle 1.4s infinite alternate;
    }
    .s1 { left: 12%; top: 22%; }
    .s2 { right: 14%; top: 17%; animation-delay: .4s; }
    .s3 { left: 23%; bottom: 18%; animation-delay: .7s; }
    .s4 { right: 24%; bottom: 20%; animation-delay: .2s; }

    .family {
        position: relative;
        width: 260px;
        height: 180px;
    }
    .person {
        position: absolute;
        bottom: 5px;
        width: 100px;
        height: 145px;
        animation: bounce 1.7s ease-in-out infinite;
    }
    .boy { left: 18px; }
    .girl { right: 18px; animation-delay: .2s; }

    .head {
        position: absolute;
        top: 10px;
        left: 23px;
        width: 56px;
        height: 57px;
        border: 2px solid #664d4d;
        border-radius: 48% 48% 45% 45%;
        background: #ffd7b5;
        z-index: 3;
    }
    .hair {
        position: absolute;
        left: -2px;
        top: -5px;
        width: 57px;
        height: 25px;
        border-radius: 55% 55% 30% 20%;
        background: #654333;
    }
    .girl .hair {
        background: #493247;
        height: 39px;
        width: 65px;
        left: -6px;
        border-radius: 50% 50% 35% 35%;
    }
    .eye {
        position: absolute;
        top: 29px;
        width: 5px;
        height: 7px;
        background: #49363b;
        border-radius: 50%;
    }
    .eye.left { left: 15px; }
    .eye.right { right: 15px; }
    .smile {
        position: absolute;
        top: 36px;
        left: 20px;
        width: 15px;
        height: 8px;
        border-bottom: 2px solid #a64e55;
        border-radius: 50%;
    }
    .body {
        position: absolute;
        top: 65px;
        left: 15px;
        width: 72px;
        height: 72px;
        border-radius: 25px 25px 15px 15px;
        background: #72bde8;
        border: 2px solid #ffffff;
        z-index: 2;
    }
    .girl .body { background: #f28fb6; }
    .arm {
        position: absolute;
        top: 76px;
        width: 47px;
        height: 15px;
        border: 2px solid #ffd7b5;
        border-radius: 20px;
        background: #ffd7b5;
        z-index: 4;
        transform-origin: 10px center;
    }
    .boy .arm { left: 48px; transform: rotate(18deg); }
    .girl .arm { left: 5px; transform: rotate(162deg); }

    .hug .boy {
        animation: boyhug .8s ease-in-out forwards;
    }
    .hug .girl {
        animation: girlhug .8s ease-in-out forwards;
    }
    .hug .boy .arm {
        animation: boyarm .8s ease-in-out forwards;
    }
    .hug .girl .arm {
        animation: girlarm .8s ease-in-out forwards;
    }
    .sad .person { animation: droop 1.3s ease-in-out infinite; }
    .sad .smile {
        top: 41px;
        border-bottom: none;
        border-top: 2px solid #a64e55;
    }

    @keyframes bounce {
        0%,100% { transform: translateY(0); }
        50% { transform: translateY(-7px); }
    }
    @keyframes boyhug {
        to { transform: translateX(43px) rotate(-4deg); }
    }
    @keyframes girlhug {
        to { transform: translateX(-43px) rotate(4deg); }
    }
    @keyframes boyarm {
        to { transform: rotate(145deg); }
    }
    @keyframes girlarm {
        to { transform: rotate(35deg); }
    }
    @keyframes twinkle {
        from { transform: scale(.7) rotate(-12deg); opacity: .5; }
        to { transform: scale(1.2) rotate(12deg); opacity: 1; }
    }
    @keyframes droop {
        0%,100% { transform: translateY(2px); }
        50% { transform: translateY(10px); }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- HEADER --------------------

st.markdown(
    """
    <div class="hero">
        <h1>🏡 Our Family Hub</h1>
        <p>A little teamwork, a little kindness, and lots of love.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- FAMILY ANIMATION --------------------

reaction = st.session_state.reaction
scene_class = "hug" if reaction == "happy" else (
    "sad" if reaction == "sad" else ""
)

st.markdown(
    f"""
    <div class="scene {scene_class}">
      <span class="sparkle s1">✨</span>
      <span class="sparkle s2">💖</span>
      <span class="sparkle s3">⭐</span>
      <span class="sparkle s4">💕</span>
      <div class="family">
        <div class="person boy">
          <div class="head">
            <div class="hair"></div>
            <div class="eye left"></div>
            <div class="eye right"></div>
            <div class="smile"></div>
          </div>
          <div class="body"></div>
          <div class="arm"></div>
        </div>
        <div class="person girl">
          <div class="head">
            <div class="hair"></div>
            <div class="eye left"></div>
            <div class="eye right"></div>
            <div class="smile"></div>
          </div>
          <div class="body"></div>
          <div class="arm"></div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

message = html.escape(st.session_state.reaction_message)
st.markdown(
    f"<h3 style='text-align:center;color:#67527d'>{message}</h3>",
    unsafe_allow_html=True,
)

# -------------------- SUMMARY --------------------

total_tasks = len(st.session_state.tasks)
completed_tasks = sum(
    1 for task in st.session_state.tasks if task["done"]
)
progress = completed_tasks / total_tasks if total_tasks else 0

a, b, c = st.columns(3)
a.metric("📋 Family tasks", total_tasks)
b.metric("✅ Completed", completed_tasks)
c.metric("🛒 Grocery items", len(st.session_state.groceries))

st.progress(progress, text=f"Family teamwork: {int(progress * 100)}%")

# -------------------- TABS --------------------

tasks_tab, grocery_tab, calendar_tab, notes_tab = st.tabs(
    ["📋 Tasks", "🛒 Groceries", "📅 Appointments", "💌 Family Notes"]
)

# -------------------- TASKS --------------------

with tasks_tab:
    st.subheader("Our family to-do list")

    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("What needs to be done?")
        col1, col2 = st.columns(2)
        with col1:
            assigned_to = st.selectbox(
                "Who is responsible?",
                ["Everyone", "Mom", "Dad", "Boy", "Girl", "Other"],
            )
        with col2:
            priority = st.selectbox(
                "Priority", ["Normal", "High", "Low"]
            )
        due_date = st.date_input("Due date", value=date.today())
        add_task = st.form_submit_button("➕ Add task", use_container_width=True)

        if add_task:
            if task_name.strip():
                st.session_state.tasks.append({
                    "id": str(uuid.uuid4()),
                    "name": task_name.strip(),
                    "assigned": assigned_to,
                    "priority": priority,
                    "due": due_date.isoformat(),
                    "done": False,
                })
                react("welcome", "A new task, a fresh start! 🌈")
                st.rerun()
            else:
                st.warning("Please enter a task first.")

    st.divider()

    if not st.session_state.tasks:
        st.info("No tasks yet. Add one above to get started! 💜")
    else:
        for task in list(st.session_state.tasks):
            with st.container(border=True):
                left, middle, right = st.columns([5, 2, 1])

                with left:
                    if task["done"]:
                        st.markdown(
                            f"~~{html.escape(task['name'])}~~"
                        )
                    else:
                        st.markdown(f"**{html.escape(task['name'])}**")
                    st.caption(
                        f"👤 {task['assigned']} · "
                        f"📅 {task['due']} · "
                        f"Priority: {task['priority']}"
                    )

                with middle:
                    if task["done"]:
                        st.success("Completed 🎉")
                    else:
                        if st.button(
                            "✅ Complete",
                            key=f"complete_{task['id']}",
                            use_container_width=True,
                        ):
                            task["done"] = True
                            react(
                                "happy",
                                f"Yaaay! '{task['name']}' is done! "
                                "Time for a big family hug! 🤗",
                            )
                            st.rerun()

                        if task["priority"] == "High":
                            st.warning("High priority")
                        elif task["priority"] == "Low":
                            st.caption("Low priority")

                with right:
                    if task["done"]:
                        if st.button(
                            "↩️",
                            key=f"undo_{task['id']}",
                            help="Undo completion",
                        ):
                            task["done"] = False
                            react(
                                "sad",
                                "Oops! This task is back on the list. "
                                "No worries—we can try again! 💪",
                            )
                            st.rerun()

                    if st.button(
                        "🗑️",
                        key=f"delete_task_{task['id']}",
                        help="Delete task",
                    ):
                        st.session_state.tasks.remove(task)
                        react("welcome", "One less thing to worry about! 🌷")
                        st.rerun()

    if total_tasks and completed_tasks == total_tasks:
        st.balloons()
        st.success("Every task is complete. Amazing family teamwork! 🏆")

# -------------------- GROCERIES --------------------

with grocery_tab:
    st.subheader("Shopping list")

    with st.form("add_grocery_form", clear_on_submit=True):
        item_name = st.text_input("Add a grocery item")
        quantity = st.text_input("Quantity or details", placeholder="e.g. 2 cartons")
        add_item = st.form_submit_button("➕ Add to list", use_container_width=True)

        if add_item:
            if item_name.strip():
                st.session_state.groceries.append({
                    "id": str(uuid.uuid4()),
                    "name": item_name.strip(),
                    "quantity": quantity.strip(),
                    "bought": False,
                })
                st.rerun()
            else:
                st.warning("Enter an item to add.")

    st.divider()

    for item in list(st.session_state.groceries):
        c1, c2 = st.columns([5, 1])
        with c1:
            label = item["name"]
            if item["quantity"]:
                label += f" — {item['quantity']}"
            checked = st.checkbox(
                label,
                value=item["bought"],
                key=f"grocery_{item['id']}",
            )
            if checked != item["bought"]:
                item["bought"] = checked
                if checked:
                    react("happy", f"Nice shopping! {item['name']} is checked off! 🛍️")
                st.rerun()
        with c2:
            if st.button("🗑️", key=f"delete_grocery_{item['id']}"):
                st.session_state.groceries.remove(item)
                st.rerun()

    if not st.session_state.groceries:
        st.info("Your shopping list is empty.")

    if st.session_state.groceries:
        if st.button("🧹 Clear purchased items"):
            st.session_state.groceries = [
                item for item in st.session_state.groceries
                if not item["bought"]
            ]
            st.rerun()

# -------------------- APPOINTMENTS --------------------

with calendar_tab:
    st.subheader("Family calendar")

    with st.form("add_appointment_form", clear_on_submit=True):
        appointment_name = st.text_input("Appointment or event")
        appointment_date = st.date_input(
            "Date", value=date.today(), key="appointment_date"
        )
        appointment_time = st.time_input(
            "Time", value=datetime.now().replace(second=0, microsecond=0).time()
        )
        appointment_person = st.selectbox(
            "For whom?",
            ["Everyone", "Mom", "Dad", "Boy", "Girl", "Other"],
            key="appointment_person",
        )
        appointment_details = st.text_input("Details (optional)")
        add_appointment = st.form_submit_button(
            "➕ Add appointment", use_container_width=True
        )

        if add_appointment:
            if appointment_name.strip():
                st.session_state.appointments.append({
                    "id": str(uuid.uuid4()),
                    "name": appointment_name.strip(),
                    "date": appointment_date.isoformat(),
                    "time": appointment_time.strftime("%H:%M"),
                    "person": appointment_person,
                    "details": appointment_details.strip(),
                })
                st.rerun()
            else:
                st.warning("Enter an event name.")

    st.divider()

    appointments = sorted(
        st.session_state.appointments,
        key=lambda appt: (appt["date"], appt["time"]),
    )

    if not appointments:
        st.info("Nothing scheduled yet. Add a family event above.")
    else:
        for appt in appointments:
            with st.container(border=True):
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**📌 {html.escape(appt['name'])}**")
                    st.write(f"📅 {appt['date']} at {appt['time']}")
                    st.caption(f"👤 {appt['person']}")
                    if appt["details"]:
                        st.write(appt["details"])
                with col2:
                    if st.button("🗑️", key=f"delete_appt_{appt['id']}"):
                        st.session_state.appointments.remove(appt)
                        st.rerun()

# -------------------- FAMILY NOTES --------------------

with notes_tab:
    st.subheader("Little notes, big love 💌")

    with st.form("add_note_form", clear_on_submit=True):
        note_author = st.text_input("From")
        note_text = st.text_area(
            "Write a family message",
            placeholder="You make our family special because...",
        )
        add_note = st.form_submit_button("💌 Leave a note", use_container_width=True)

        if add_note:
            if note_text.strip():
                st.session_state.notes.insert(0, {
                    "id": str(uuid.uuid4()),
                    "author": note_author.strip() or "A family member",
                    "text": note_text.strip(),
                    "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                react("happy", "A little love note makes everything brighter! 💖")
                st.rerun()
            else:
                st.warning("Write a note before saving it.")

    st.divider()

    if not st.session_state.notes:
        st.info("No notes yet. Leave someone a little encouragement!")
    else:
        for note in st.session_state.notes:
            with st.container(border=True):
                st.markdown(f"💗 **{html.escape(note['author'])}**")
                st.write(note["text"])
                st.caption(note["created"])
                if st.button("🗑️ Delete note", key=f"delete_note_{note['id']}"):
                    st.session_state.notes.remove(note)
                    st.rerun()

# -------------------- FOOTER --------------------

st.divider()
st.markdown(
    """
    <p style="text-align:center;color:#857790">
    Made with 💜 for the people who make a house a home.
    </p>
    """,
    unsafe_allow_html=True,
)

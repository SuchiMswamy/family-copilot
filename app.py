import streamlit as st
from datetime import date, datetime

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Our Family Hub — Suchi & Abi",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# THEME CONFIGURATION
# --------------------------------------------------
THEMES = {
    "Light": {
        "bg": "#FFFFFF",
        "surface": "#F4F5F7",
        "text": "#202124",
        "muted": "#5F6368",
        "border": "#DADCE0",
        "accent": "#456B82",
        "input": "#FFFFFF",
        "success": "#DDEFE2",
    },
    "Dark": {
        "bg": "#17191C",
        "surface": "#25282D",
        "text": "#F4F5F7",
        "muted": "#C1C5CC",
        "border": "#484D55",
        "accent": "#A9C9EB",
        "input": "#30343A",
        "success": "#244234",
    },
    "Pastel": {
        "bg": "#FFF9F6",
        "surface": "#F5EAEF",
        "text": "#40343B",
        "muted": "#695B64",
        "border": "#E3D0DA",
        "accent": "#80566F",
        "input": "#FFFFFF",
        "success": "#E3F0E4",
    },
}

if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Pastel"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
DEFAULTS = {
    "tasks": [],
    "groceries": [],
    "appointments": [],
    "notes": [],
    "shopping_history": [],
    "mood": "Happy",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --------------------------------------------------
# THEME SELECTOR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🏡 Our Family Hub")
    st.caption("A little space for our everyday life")

    st.selectbox(
        "🎨 Choose your theme",
        ["Light", "Dark", "Pastel"],
        key="selected_theme",
    )

    st.divider()
    st.markdown("### 💕 Our little home")
    st.caption("Suchi & Abi")
    st.caption("Small steps, big love.")

colors = THEMES[st.session_state.selected_theme]

# --------------------------------------------------
# CONSISTENT, READABLE STYLING
# --------------------------------------------------
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {colors["bg"]};
        color: {colors["text"]};
    }}

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp li,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6,
    .stApp [data-testid="stMarkdownContainer"] {{
        color: {colors["text"]};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {colors["surface"]};
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {colors["text"]};
    }}

    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stExpander"] {{
        border-color: {colors["border"]};
        border-radius: 12px;
    }}

    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="select"] > div {{
        color: {colors["text"]};
        background-color: {colors["input"]};
        border-color: {colors["border"]};
    }}

    .stApp [data-baseweb="select"] * {{
        color: {colors["text"]};
    }}

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {{
        background-color: {colors["surface"]};
    }}

    .stApp .stButton > button,
    .stApp .stDownloadButton > button {{
        background-color: {colors["surface"]};
        color: {colors["text"]};
        border: 1px solid {colors["border"]};
        border-radius: 10px;
        min-height: 40px;
    }}

    .stApp .stButton > button:hover,
    .stApp .stDownloadButton > button:hover {{
        border-color: {colors["accent"]};
        color: {colors["accent"]};
    }}

    .stApp [data-testid="stWidgetLabel"] p,
    .stApp [data-testid="stCaptionContainer"] p {{
        color: {colors["muted"]};
    }}

    .family-card {{
        background-color: {colors["surface"]};
        color: {colors["text"]};
        border: 1px solid {colors["border"]};
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
    }}

    .family-card h3 {{
        color: {colors["text"]};
        margin-top: 0;
    }}

    .family-card p {{
        color: {colors["muted"]};
    }}

    .hero {{
        background-color: {colors["surface"]};
        color: {colors["text"]};
        border: 1px solid {colors["border"]};
        border-radius: 20px;
        padding: 28px;
        margin-bottom: 20px;
    }}

    .hero h1 {{
        color: {colors["text"]};
        margin-bottom: 8px;
    }}

    .hero p {{
        color: {colors["muted"]};
        font-size: 1.05rem;
    }}

    div[data-testid="stMetric"] {{
        background-color: {colors["surface"]};
        border: 1px solid {colors["border"]};
        padding: 14px;
        border-radius: 12px;
    }}

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: {colors["text"]};
    }}

    .stApp hr {{
        border-color: {colors["border"]};
    }}

    #MainMenu, footer {{
        visibility: hidden;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# REUSABLE HELPERS
# --------------------------------------------------
def family_card(title, body):
    """Display a simple themed information card."""
    st.markdown(
        f"""
        <div class="family-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d %b %Y")
    return str(value)


def add_history(action, item):
    st.session_state.shopping_history.append({
        "action": action,
        "item": item,
        "date": datetime.now().strftime("%d %b %Y, %H:%M"),
    })


# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1>🏡 Our Family Hub</h1>
        <p>Suchi & Abi · Organising life, one little step at a time.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

today = date.today()

st.caption(
    f"📅 Today is {today.strftime('%A, %d %B %Y')} "
    f"· Current theme: {st.session_state.selected_theme}"
)

# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------
pages = [
    "🏠 Home",
    "✅ Tasks",
    "🛒 Groceries",
    "📅 Appointments",
    "💌 Family Notes",
    "🧾 Shopping History",
]

page = st.sidebar.radio("Navigate", pages)

# ==================================================
# HOME
# ==================================================
if page == "🏠 Home":
    st.subheader("Welcome home, Suchi & Abi! 💕")

    col1, col2, col3 = st.columns(3)

    with col1:
        pending = sum(
            1 for task in st.session_state.tasks
            if not task["done"]
        )
        st.metric("Pending tasks", pending)

    with col2:
        remaining = sum(
            1 for item in st.session_state.groceries
            if not item["bought"]
        )
        st.metric("Groceries to buy", remaining)

    with col3:
        st.metric(
            "Upcoming appointments",
            len(st.session_state.appointments),
        )

    st.markdown("### 💗 Our daily mood")

    mood_options = [
        "Happy",
        "Relaxed",
        "Grateful",
        "Busy",
        "Tired",
        "Need a little love",
    ]

    st.session_state.mood = st.selectbox(
        "How are we feeling today?",
        mood_options,
        index=mood_options.index(st.session_state.mood)
        if st.session_state.mood in mood_options else 0,
    )

    mood_messages = {
        "Happy": "Keep collecting those little happy moments! ☀️",
        "Relaxed": "Take it slow. There is no rush. 🌿",
        "Grateful": "There is always something lovely to appreciate. 💕",
        "Busy": "One thing at a time. You have got this! 🌸",
        "Tired": "Rest is productive, too. Be kind to yourselves. ☁️",
        "Need a little love": "A hug, a kind word, and a fresh start. ❤️",
    }

    family_card(
        "Today's little reminder 💌",
        mood_messages[st.session_state.mood],
    )

    st.markdown("### 🌷 A little note for us")

    st.info(
        "We don't have to make every day perfect. "
        "Let's make our home a place where we feel loved, "
        "supported, and happy to come back to."
    )

    st.markdown("### 📌 Quick overview")

    if st.session_state.tasks:
        st.markdown("**Your next tasks**")
        for task in st.session_state.tasks[:5]:
            status = "✅" if task["done"] else "⬜"
            st.write(f"{status} {task['name']}")
    else:
        st.caption("No tasks yet. Add your first one in the Tasks section!")

    if st.session_state.groceries:
        st.markdown("**Your grocery list**")
        for item in st.session_state.groceries[:5]:
            status = "✅" if item["bought"] else "🛒"
            st.write(f"{status} {item['name']}")

# ==================================================
# TASKS
# ==================================================
elif page == "✅ Tasks":
    st.subheader("Our Tasks ✅")
    st.write("Keep track of the little things that make life easier.")

    with st.form("add_task_form", clear_on_submit=True):
        task_name = st.text_input("Task name", placeholder="e.g. Tidy the living room")
        assigned_to = st.selectbox("Assigned to", ["Both", "Suchi", "Abi"])
        due_date = st.date_input("Due date", value=None)
        priority = st.selectbox("Priority", ["Normal", "High", "Low"])
        submitted = st.form_submit_button("➕ Add task")

        if submitted:
            if task_name.strip():
                st.session_state.tasks.append({
                    "name": task_name.strip(),
                    "assigned": assigned_to,
                    "due": due_date,
                    "priority": priority,
                    "done": False,
                })
                st.success("Task added!")
                st.rerun()
            else:
                st.warning("Please enter a task name.")

    st.divider()

    if not st.session_state.tasks:
        st.info("No tasks yet. Enjoy the breathing room, or add one above!")
    else:
        filter_status = st.radio(
            "Show tasks",
            ["All", "Pending", "Completed"],
            horizontal=True,
        )

        for index, task in enumerate(st.session_state.tasks):
            if filter_status == "Pending" and task["done"]:
                continue
            if filter_status == "Completed" and not task["done"]:
                continue

            with st.container(border=True):
                left, middle, right = st.columns([0.12, 0.68, 0.20])

                with left:
                    new_status = st.checkbox(
                        "Done",
                        value=task["done"],
                        key=f"task_done_{index}",
                    )
                    if new_status != task["done"]:
                        task["done"] = new_status
                        st.rerun()

                with middle:
                    st.markdown(f"**{task['name']}**")
                    st.caption(
                        f"Assigned: {task['assigned']} · "
                        f"Priority: {task['priority']} · "
                        f"Due: {format_date(task['due'])}"
                    )

                with right:
                    if st.button("🗑️ Delete", key=f"delete_task_{index}"):
                        st.session_state.tasks.pop(index)
                        st.rerun()

# ==================================================
# GROCERIES
# ==================================================
elif page == "🛒 Groceries":
    st.subheader("Our Grocery List 🛒")

    with st.form("add_grocery_form", clear_on_submit=True):
        grocery_name = st.text_input(
            "Item",
            placeholder="e.g. Milk, apples, bread",
        )
        quantity = st.text_input("Quantity", placeholder="e.g. 2 packs")
        submitted = st.form_submit_button("➕ Add to list")

        if submitted:
            if grocery_name.strip():
                item = {
                    "name": grocery_name.strip(),
                    "quantity": quantity.strip() or "Not specified",
                    "bought": False,
                }
                st.session_state.groceries.append(item)
                add_history("Added to grocery list", item["name"])
                st.success("Added to your grocery list!")
                st.rerun()
            else:
                st.warning("Please enter an item name.")

    st.divider()

    if not st.session_state.groceries:
        st.info("Your grocery list is empty.")
    else:
        for index, item in enumerate(st.session_state.groceries):
            with st.container(border=True):
                col1, col2, col3 = st.columns([0.14, 0.66, 0.20])

                with col1:
                    checked = st.checkbox(
                        "Bought",
                        value=item["bought"],
                        key=f"grocery_bought_{index}",
                    )
                    if checked != item["bought"]:
                        item["bought"] = checked
                        if checked:
                            add_history("Marked as bought", item["name"])
                        st.rerun()

                with col2:
                    st.markdown(f"**{item['name']}**")
                    st.caption(f"Quantity: {item['quantity']}")

                with col3:
                    if st.button("🗑️ Remove", key=f"delete_grocery_{index}"):
                        add_history("Removed from grocery list", item["name"])
                        st.session_state.groceries.pop(index)
                        st.rerun()

        if st.button("🧹 Clear bought items"):
            st.session_state.groceries = [
                item for item in st.session_state.groceries
                if not item["bought"]
            ]
            st.rerun()

# ==================================================
# APPOINTMENTS
# ==================================================
elif page == "📅 Appointments":
    st.subheader("Our Appointments 📅")

    with st.form("add_appointment_form", clear_on_submit=True):
        title = st.text_input(
            "Appointment",
            placeholder="e.g. Dentist, family dinner",
        )
        appointment_date = st.date_input("Date", value=date.today())
        appointment_time = st.time_input("Time")
        location = st.text_input("Location (optional)")
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("➕ Add appointment")

        if submitted:
            if title.strip():
                st.session_state.appointments.append({
                    "title": title.strip(),
                    "date": appointment_date,
                    "time": appointment_time.strftime("%H:%M"),
                    "location": location.strip(),
                    "notes": notes.strip(),
                })
                st.success("Appointment added!")
                st.rerun()
            else:
                st.warning("Please enter an appointment name.")

    st.divider()

    appointments = sorted(
        enumerate(st.session_state.appointments),
        key=lambda pair: (pair[1]["date"], pair[1]["time"]),
    )

    if not appointments:
        st.info("Nothing scheduled yet.")
    else:
        for original_index, appointment in appointments:
            with st.container(border=True):
                col1, col2 = st.columns([0.8, 0.2])

                with col1:
                    st.markdown(f"### 📌 {appointment['title']}")
                    st.write(
                        f"**Date:** {format_date(appointment['date'])}"
                        f" · **Time:** {appointment['time']}"
                    )
                    if appointment["location"]:
                        st.write(f"**Location:** {appointment['location']}")
                    if appointment["notes"]:
                        st.write(appointment["notes"])

                with col2:
                    if st.button(
                        "🗑️ Delete",
                        key=f"delete_appointment_{original_index}",
                    ):
                        st.session_state.appointments.pop(original_index)
                        st.rerun()

# ==================================================
# FAMILY NOTES
# ==================================================
elif page == "💌 Family Notes":
    st.subheader("Family Notes 💌")
    st.write("Little reminders, lovely memories, and things to remember.")

    with st.form("add_note_form", clear_on_submit=True):
        note_title = st.text_input(
            "Title",
            placeholder="e.g. Something to remember",
        )
        note_body = st.text_area(
            "Your note",
            placeholder="Write your note here...",
            height=150,
        )
        submitted = st.form_submit_button("💌 Save note")

        if submitted:
            if note_body.strip():
                st.session_state.notes.append({
                    "title": note_title.strip() or "A little note",
                    "body": note_body.strip(),
                    "created": datetime.now().strftime("%d %b %Y, %H:%M"),
                })
                st.success("Your note has been saved!")
                st.rerun()
            else:
                st.warning("Write something before saving your note.")

    st.divider()

    if not st.session_state.notes:
        st.info("No notes yet. Leave a little message for your future selves.")
    else:
        for index, note in enumerate(reversed(st.session_state.notes)):
            original_index = len(st.session_state.notes) - 1 - index

            with st.container(border=True):
                st.markdown(f"### 💗 {note['title']}")
                st.caption(note["created"])
                st.write(note["body"])

                if st.button("🗑️ Delete note", key=f"delete_note_{original_index}"):
                    st.session_state.notes.pop(original_index)
                    st.rerun()

# ==================================================
# SHOPPING HISTORY
# ==================================================
elif page == "🧾 Shopping History":
    st.subheader("Shopping History 🧾")
    st.write("A simple record of grocery-list changes.")

    if not st.session_state.shopping_history:
        st.info("Your shopping history will appear here as you use the list.")
    else:
        for entry in reversed(st.session_state.shopping_history):
            with st.container(border=True):
                st.markdown(f"**{entry['action']}**")
                st.write(entry["item"])
                st.caption(entry["date"])

        if st.button("🧹 Clear shopping history"):
            st.session_state.shopping_history = []
            st.rerun()

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown(
    f"""
    <div style="
        text-align: center;
        color: {colors["muted"]};
        padding: 12px;
    ">
        Made with 💗 for Suchi & Abi<br>
        Small steps, big love 🏡
    </div>
    """,
    unsafe_allow_html=True,
)

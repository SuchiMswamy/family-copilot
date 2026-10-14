
import streamlit as st
from datetime import date, datetime
from uuid import uuid4
import html

# ============================================================
# OUR FAMILY HUB — SUCHI & ABI 💗
# Single-file Streamlit application
#
# Features:
# - 10 colour themes
# - Animated Suchi & Abi couple
# - Happy, sleepy, hugging and party moods
# - Tasks, priorities, due dates and overdue nudges
# - Grocery list and shopping history
# - Family progress dashboard
# - Appointments and family notes
# - Responsive styling and reduced-motion support
#
# Data is stored in Streamlit session state.
# It is NOT yet shared or permanently saved in Supabase.
# ============================================================

st.set_page_config(
    page_title="Our Family Hub",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- THEMES --------------------

THEMES = {
    "Pastel Dreams": {
        "bg": "#FFF9FC", "text": "#594657", "surface": "#FFFFFF",
        "accents": ["#F8DDEB", "#DDEBFA", "#DDF3E4", "#FFF0D4"],
        "button_text": "#594657",
    },
    "Sage & Olive": {
        "bg": "#F7F8F1", "text": "#344438", "surface": "#FFFFFF",
        "accents": ["#DCE8D5", "#A8B99A", "#788B68", "#F2EBDD"],
        "button_text": "#FFFFFF",
    },
    "Ocean Blues": {
        "bg": "#F2FAFC", "text": "#244657", "surface": "#FFFFFF",
        "accents": ["#D9F0F5", "#A8D9E8", "#5DA8C4", "#24566D"],
        "button_text": "#FFFFFF",
    },
    "Lavender Haze": {
        "bg": "#FAF7FF", "text": "#51436C", "surface": "#FFFFFF",
        "accents": ["#E9DFFC", "#CDBBF2", "#A18ADD", "#F9F3FF"],
        "button_text": "#51436C",
    },
    "Peach & Coral": {
        "bg": "#FFF8F4", "text": "#75483F", "surface": "#FFFFFF",
        "accents": ["#FFE1D6", "#FFBFAE", "#F28E7B", "#FFF0D9"],
        "button_text": "#75483F",
    },
    "Warm Earth": {
        "bg": "#FAF5ED", "text": "#594633", "surface": "#FFFFFF",
        "accents": ["#E8D8C3", "#C9A987", "#9B7653", "#F4EBDD"],
        "button_text": "#FFFFFF",
    },
    "Rose & Burgundy": {
        "bg": "#FFF7F9", "text": "#68384B", "surface": "#FFFFFF",
        "accents": ["#F7DDE4", "#E6A8B8", "#B85C78", "#71374F"],
        "button_text": "#FFFFFF",
    },
    "Midnight Blue": {
        "bg": "#172230", "text": "#F0F5FA", "surface": "#28364B",
        "accents": ["#28364B", "#344D68", "#6689A8", "#B8D5E8"],
        "button_text": "#F0F5FA",
    },
    "Charcoal & Gold": {
        "bg": "#1C1C1C", "text": "#F5EEDC", "surface": "#282828",
        "accents": ["#282828", "#48443D", "#C6A765", "#E8DCC0"],
        "button_text": "#1C1C1C",
    },
    "Mint & Teal": {
        "bg": "#F2FCF8", "text": "#28564C", "surface": "#FFFFFF",
        "accents": ["#D5F3E9", "#A1DDCC", "#4DAF9A", "#23796D"],
        "button_text": "#28564C",
    },
}

# -------------------- SESSION DATA --------------------

DEFAULTS = {
    "tasks": [],
    "groceries": [],
    "appointments": [],
    "family_notes": [],
    "shopping_history": [],
    "last_celebration": None,
    "celebration_id": None,
    "celebration_counter": 0,
    "total_completed": 0,
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value.copy() if isinstance(value, list) else value


def make_item(name, priority="Normal", due=None):
    return {
        "id": str(uuid4()),
        "name": name.strip(),
        "checked": False,
        "created_at": datetime.now(),
        "checked_at": None,
        "priority": priority,
        "due": due,
    }


def age_days(item):
    created = item.get("created_at")
    if not isinstance(created, datetime):
        return 0
    return max(0, (datetime.now() - created).days)


def family_mood():
    items = st.session_state.tasks + st.session_state.groceries

    if not items:
        return (
            "happy", "😊",
            "Suchi and Abi are ready for a fresh start!",
        )

    unfinished = [item for item in items if not item["checked"]]

    if not unfinished:
        return (
            "party", "🥳",
            "EVERYTHING IS DONE! Suchi and Abi are celebrating!",
        )

    neglected = [
        item for item in unfinished
        if age_days(item) >= 3
    ]

    if neglected:
        return (
            "sleepy", "😴",
            f"Suchi and Abi are getting sleepy! "
            f"{len(neglected)} item(s) have been waiting for 3 days.",
        )

    return (
        "happy", "😊",
        "We're doing great, one little step at a time!",
    )


def show_couple(mood, message):
    """Draw the animated couple using inline CSS and HTML."""
    expression = {
        "happy": ("☺", "☺"),
        "sleepy": ("😴", "😴"),
        "hug": ("☺", "☺"),
        "party": ("🥳", "🥳"),
    }
    girl_face, boy_face = expression.get(mood, ("☺", "☺"))

    st.markdown(
        f"""
        <div class="couple-scene mood-{mood}">
            <div class="floating heart-one">💗</div>
            <div class="floating heart-two">✨</div>
            <div class="floating heart-three">💕</div>

            <div class="couple">
                <div class="character girl">
                    <div class="hair"></div>
                    <div class="face">{girl_face}</div>
                    <div class="body"></div>
                    <div class="character-name">Suchi 🌸</div>
                </div>

                <div class="character boy">
                    <div class="hair"></div>
                    <div class="face">{boy_face}</div>
                    <div class="body"></div>
                    <div class="character-name">Abi 💙</div>
                </div>
            </div>

            <div class="mood-message">{html.escape(message)}</div>
            <div class="mood-caption">
                {'Confetti time! 🎉' if mood == 'party'
                 else 'Sending you a little love 💞' if mood == 'hug'
                 else 'A gentle reminder, not a guilt trip 💛' if mood == 'sleepy'
                 else 'Small steps, big love 🏡'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def celebrate(message, event_id=None):
    st.session_state.last_celebration = message
    st.session_state.celebration_id = event_id or str(uuid4())
    st.session_state.celebration_counter += 1


def add_shopping_record(item):
    st.session_state.shopping_history.insert(
        0,
        {
            "name": item["name"],
            "bought_at": datetime.now(),
        },
    )


# -------------------- THEME SELECTOR --------------------

with st.sidebar:
    st.markdown("# 🏡 Our Family Hub")
    st.caption("A little more organised, a little less stressed.")

    theme_name = st.selectbox(
        "🎨 Choose your theme",
        list(THEMES.keys()),
        key="family_theme",
    )

theme = THEMES[theme_name]
bg = theme["bg"]
text_color = theme["text"]
surface = theme["surface"]
a0, a1, a2, a3 = theme["accents"]
button_text = theme["button_text"]

# -------------------- STYLING --------------------

st.markdown(
    f"""
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap'
    );

    .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {{
        background: {bg} !important;
        color: {text_color} !important;
        font-family: 'DM Sans', sans-serif;
    }}

    [data-testid="stSidebar"] {{
        background: {surface} !important;
        border-right: 1px solid {a1} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {text_color};
    }}

    h1, h2, h3 {{
        color: {text_color} !important;
        font-family: 'Playfair Display', Georgia, serif !important;
    }}

    p, label, [data-testid="stMarkdownContainer"] {{
        color: {text_color};
    }}

    .hero {{
        background: linear-gradient(120deg, {a0}, {a3});
        padding: 28px;
        border-radius: 22px;
        border: 1px solid {a1};
        margin: 12px 0 22px;
    }}

    .hero h1, .hero p {{
        color: {text_color} !important;
    }}

    .metric-card {{
        background: {surface};
        border: 1px solid {a1};
        border-radius: 18px;
        padding: 18px;
        min-height: 110px;
    }}

    .metric-value {{
        font: 600 2rem 'Playfair Display', Georgia, serif;
        margin-top: 6px;
    }}

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button {{
        background: {a2} !important;
        color: {button_text} !important;
        border: 1px solid {a1} !important;
        border-radius: 11px;
        min-height: 44px;
        font-weight: 600;
    }}

    div[data-testid="stForm"] {{
        background: {surface};
        border: 1px solid {a1};
        border-radius: 16px;
        padding: 16px;
    }}

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {{
        color: {text_color} !important;
    }}

    .item-name {{
        font-size: 1rem;
        font-weight: 600;
        padding-top: 5px;
        overflow-wrap: anywhere;
    }}

    .completed {{
        text-decoration: line-through;
        opacity: .55;
    }}

    .gentle-nudge {{
        background: {a0};
        border: 1px solid {a1};
        border-radius: 10px;
        padding: 8px;
        font-size: .85rem;
        margin: 4px 0;
    }}

    /* Animated Suchi & Abi */
    .couple-scene {{
        position: relative;
        overflow: hidden;
        text-align: center;
        padding: 18px;
        margin: 12px 0 22px;
        border-radius: 22px;
        background: linear-gradient(135deg, {a0}, {a3});
        border: 1px solid {a1};
    }}

    .couple {{
        height: 150px;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }}

    .character {{
        width: 92px;
        height: 125px;
        position: relative;
        animation: bob 1.2s ease-in-out infinite alternate;
    }}

    .character .hair {{
        position: absolute;
        top: 5px;
        left: 26px;
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: #654333;
        z-index: 1;
    }}

    .character .face {{
        position: absolute;
        top: 15px;
        left: 27px;
        width: 40px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #FFD8BB;
        border-radius: 45%;
        font-size: 23px;
        z-index: 2;
    }}

    .character .body {{
        position: absolute;
        top: 49px;
        left: 14px;
        width: 66px;
        height: 62px;
        border-radius: 28px 28px 14px 14px;
        background: #E78BAB;
    }}

    .boy .body {{
        background: #83B9D5;
    }}

    .boy {{
        animation-delay: .2s;
    }}

    .character-name {{
        position: absolute;
        top: 112px;
        width: 100%;
        font-weight: 700;
        font-size: .82rem;
    }}

    .floating {{
        position: absolute;
        font-size: 24px;
        animation: float 2s ease-in-out infinite;
    }}

    .heart-one {{ top: 15px; left: 18%; }}
    .heart-two {{ top: 35px; right: 20%; animation-delay: .4s; }}
    .heart-three {{ bottom: 48px; left: 28%; animation-delay: .7s; }}

    .mood-message {{
        font-size: 1.12rem;
        font-weight: 700;
        margin-top: 8px;
    }}

    .mood-caption {{
        font-size: .88rem;
        margin-top: 4px;
    }}

    .mood-hug .girl {{
        animation: hug-girl .7s ease-in-out infinite alternate;
    }}

    .mood-hug .boy {{
        animation: hug-boy .7s ease-in-out infinite alternate;
    }}

    .mood-sleepy .character {{
        animation: sleepy 2s ease-in-out infinite alternate;
    }}

    .mood-party .character {{
        animation: dance .45s ease-in-out infinite alternate;
    }}

    @keyframes bob {{
        from {{ transform: translateY(2px); }}
        to {{ transform: translateY(-6px); }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0) rotate(-5deg); }}
        50% {{ transform: translateY(-12px) rotate(8deg); }}
    }}

    @keyframes hug-girl {{
        from {{ transform: translateX(0) rotate(-4deg); }}
        to {{ transform: translateX(15px) rotate(5deg); }}
    }}

    @keyframes hug-boy {{
        from {{ transform: translateX(0) rotate(4deg); }}
        to {{ transform: translateX(-15px) rotate(-5deg); }}
    }}

    @keyframes sleepy {{
        from {{ transform: translateY(2px) rotate(-2deg); }}
        to {{ transform: translateY(8px) rotate(2deg); }}
    }}

    @keyframes dance {{
        from {{ transform: translateY(0) rotate(-8deg); }}
        to {{ transform: translateY(-12px) rotate(8deg); }}
    }}

    @media (max-width: 768px) {{
        .block-container {{
            padding: .8rem .8rem 2rem !important;
        }}

        h1 {{ font-size: 1.85rem !important; }}

        .hero {{
            padding: 18px;
            border-radius: 16px;
        }}

        .metric-card {{
            min-height: auto;
            padding: 14px;
            margin-bottom: 8px;
        }}

        .couple-scene {{ padding: 12px; }}

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] button {{
            min-height: 46px;
            white-space: normal;
        }}
    }}

    @media (prefers-reduced-motion: reduce) {{
        .character, .floating {{
            animation: none !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------- NAVIGATION --------------------

st.markdown("## 🏡 Our Family Hub")
st.caption("A little more organised, a little less stressed.")

pages = [
    "✨ Home",
    "✅ To-do list",
    "🛒 Groceries",
    "📅 Appointments",
    "💌 Family Notes & Messages",
    "🧾 Shopping History",
]

page = st.selectbox(
    "📍 Where would you like to go?",
    pages,
    key="main_page_navigation",
)

st.divider()

# -------------------- HOME --------------------

if page == "✨ Home":
    st.markdown(
        """
        <div class="hero">
            <p>YOUR FAMILY DASHBOARD</p>
            <h1>A calmer kind of busy. 💗</h1>
            <p>Little things, big love, one family at a time.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    mood, emoji, message = family_mood()
    show_couple(mood, message)

    tasks = st.session_state.tasks
    groceries = st.session_state.groceries
    appointments = st.session_state.appointments

    open_tasks = sum(not x["checked"] for x in tasks)
    open_groceries = sum(not x["checked"] for x in groceries)
    upcoming = sum(x["date"] >= date.today() for x in appointments)

    c1, c2, c3 = st.columns(3)

    metrics = [
        (c1, "✅ Tasks left", open_tasks),
        (c2, "🛒 Items to buy", open_groceries),
        (c3, "📅 Upcoming events", upcoming),
    ]

    for col, label, value in metrics:
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div>{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    total = len(tasks) + len(groceries)
    completed = sum(x["checked"] for x in tasks + groceries)

    st.markdown("### 🌈 Family progress")

    st.progress(
        completed / total if total else 0.0,
        text=(
            f"{completed} of {total} checklist items completed"
            if total else "Add your first item to begin!"
        ),
    )

    if total and completed == total:
        st.success("🎉 Family victory! Everything is checked off!")
        # Avoid triggering balloons on every unrelated rerun.
        if st.session_state.celebration_id != "all-done":
            st.session_state.celebration_id = "all-done"
            st.balloons()

    left, right = st.columns(2)

    with left:
        st.markdown("### 🌿 Quick-add a task")

        with st.form("home_task_form", clear_on_submit=True):
            task_name = st.text_input(
                "Task",
                placeholder="e.g. Book the dentist",
            )
            priority = st.selectbox(
                "Priority",
                ["Normal", "High", "Whenever"],
            )
            due = st.date_input(
                "Due date",
                value=None,
                key="home_due_date",
            )
            add_task = st.form_submit_button("＋ Add task")

        if add_task and task_name.strip():
            st.session_state.tasks.append(
                make_item(task_name, priority, due)
            )
            st.rerun()

    with right:
        st.markdown("### 🥑 Quick-add groceries")

        with st.form("home_grocery_form", clear_on_submit=True):
            grocery_name = st.text_input(
                "Grocery",
                placeholder="e.g. Milk and bananas",
            )
            add_grocery = st.form_submit_button("＋ Add grocery")

        if add_grocery and grocery_name.strip():
            st.session_state.groceries.append(
                make_item(grocery_name)
            )
            st.rerun()

    st.markdown("### 📅 Coming up")

    upcoming_events = sorted(
        [
            event for event in appointments
            if event["date"] >= date.today()
        ],
        key=lambda event: event["date"],
    )

    if upcoming_events:
        for event in upcoming_events[:5]:
            days = (event["date"] - date.today()).days

            if days == 0:
                when = "Today 🎉"
            elif days == 1:
                when = "Tomorrow 🌷"
            else:
                when = f"In {days} days"

            st.markdown(
                f"**{html.escape(event['name'])}** · "
                f"{event['date'].strftime('%d %b %Y')} · {when}"
            )
    else:
        st.caption("No upcoming appointments yet.")

    if st.session_state.last_celebration:
        st.success(st.session_state.last_celebration)

# -------------------- TO-DO LIST --------------------

elif page == "✅ To-do list":
    st.title("One thing at a time. 🌱")

    with st.form("task_form", clear_on_submit=True):
        task_name = st.text_input(
            "New task",
            placeholder="e.g. Water the plants",
        )
        col1, col2 = st.columns(2)

        with col1:
            priority = st.selectbox(
                "Priority",
                ["Normal", "High", "Whenever"],
                key="task_priority",
            )

        with col2:
            due = st.date_input(
                "Due date",
                value=None,
                key="task_due",
            )

        add_task = st.form_submit_button("＋ Add task")

    if add_task and task_name.strip():
        st.session_state.tasks.append(
            make_item(task_name, priority, due)
        )
        st.rerun()

    filter_mode = st.radio(
        "Show tasks",
        ["All", "Open", "Completed"],
        horizontal=True,
    )

    tasks = st.session_state.tasks

    visible_tasks = [
        item for item in tasks
        if filter_mode == "All"
        or (filter_mode == "Open" and not item["checked"])
        or (filter_mode == "Completed" and item["checked"])
    ]

    if not visible_tasks:
        st.success("No tasks in this view. Take a little breather! 💛")

    for item in visible_tasks:
        item_id = item["id"]

        left, middle, right = st.columns([0.09, 0.69, 0.22])

        with left:
            checked = st.checkbox(
                "Done",
                value=item["checked"],
                key=f"task_check_{item_id}",
                label_visibility="collapsed",
            )

        if checked != item["checked"]:
            item["checked"] = checked
            item["checked_at"] = datetime.now() if checked else None

            if checked:
                st.session_state.total_completed += 1
                celebrate(f"Well done! Task completed: {item['name']} 💗")

            st.rerun()

        with middle:
            label = html.escape(item["name"])

            if item["checked"]:
                st.markdown(
                    f"<div class='item-name completed'>{label}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='item-name'>{label}</div>",
                    unsafe_allow_html=True,
                )

            details = []

            if item["priority"] != "Normal":
                details.append(f"Priority: {item['priority']}")

            if item["due"]:
                details.append(
                    f"Due: {item['due'].strftime('%d %b %Y')}"
                )

            if item["checked"]:
                details.append("Completed ✓")
            elif age_days(item) >= 3:
                details.append(f"Waiting {age_days(item)} days")

            if details:
                st.caption(" · ".join(details))

            if not item["checked"] and age_days(item) >= 3:
                st.markdown(
                    "<div class='gentle-nudge'>"
                    "🥺 This task has been waiting a while. "
                    "Could you tackle it today or update its due date?"
                    "</div>",
                    unsafe_allow_html=True,
                )

            if (
                not item["checked"]
                and item["due"]
                and item["due"] < date.today()
            ):
                st.warning("This task is past its due date.")

        with right:
            if st.button("Remove", key=f"task_remove_{item_id}"):
                st.session_state.tasks = [
                    x for x in st.session_state.tasks
                    if x["id"] != item_id
                ]
                st.rerun()

        st.divider()

    if st.button("Clear completed tasks"):
        st.session_state.tasks = [
            item for item in st.session_state.tasks
            if not item["checked"]
        ]
        st.rerun()

# -------------------- GROCERIES --------------------

elif page == "🛒 Groceries":
    st.title("A little list, a smoother shop. 🥑")
    st.write("Tick an item after buying it to celebrate with Suchi and Abi!")

    with st.form("grocery_form", clear_on_submit=True):
        grocery_name = st.text_input(
            "Grocery item",
            placeholder="e.g. Oats",
        )
        add_grocery = st.form_submit_button("＋ Add item")

    if add_grocery and grocery_name.strip():
        st.session_state.groceries.append(
            make_item(grocery_name)
        )
        st.rerun()

    groceries = st.session_state.groceries

    if groceries:
        bought = sum(item["checked"] for item in groceries)

        st.progress(
            bought / len(groceries),
            text=f"{bought} of {len(groceries)} items bought",
        )

        if bought == len(groceries):
            show_couple(
                "party",
                "Shopping mission complete! Suchi & Abi celebrate! 🎉",
            )

        for item in groceries:
            item_id = item["id"]
            left, middle, right = st.columns([0.09, 0.69, 0.22])

            with left:
                checked = st.checkbox(
                    "Bought",
                    value=item["checked"],
                    key=f"grocery_check_{item_id}",
                    label_visibility="collapsed",
                )

            if checked != item["checked"]:
                item["checked"] = checked
                item["checked_at"] = datetime.now() if checked else None

                if checked:
                    add_shopping_record(item)
                    celebrate(
                        f"Suchi and Abi hug! You bought {item['name']}! 💗",
                        event_id=str(uuid4()),
                    )

                st.rerun()

            with middle:
                label = html.escape(item["name"])

                if item["checked"]:
                    st.markdown(
                        f"<div class='item-name completed'>{label}</div>",
                        unsafe_allow_html=True,
                    )
                    st.caption("Bought ✓")
                else:
                    st.markdown(
                        f"<div class='item-name'>{label}</div>",
                        unsafe_allow_html=True,
                    )

                    if age_days(item) >= 3:
                        st.markdown(
                            "<div class='gentle-nudge'>"
                            "🥺 This item has been on the list for a while."
                            "</div>",
                            unsafe_allow_html=True,
                        )

            with right:
                if st.button("Remove", key=f"grocery_remove_{item_id}"):
                    st.session_state.groceries = [
                        x for x in st.session_state.groceries
                        if x["id"] != item_id
                    ]
                    st.rerun()

            st.divider()

        if st.button("Clear bought items"):
            st.session_state.groceries = [
                item for item in st.session_state.groceries
                if not item["checked"]
            ]
            st.rerun()

    else:
        st.info("Your shopping list is empty. Add your first item! 🛒")

    if st.session_state.last_celebration:
        st.markdown("### 💞 Latest celebration")
        show_couple("hug", st.session_state.last_celebration)

    if st.button("Reset celebration"):
        st.session_state.last_celebration = None
        st.rerun()

# -------------------- APPOINTMENTS --------------------

elif page == "📅 Appointments":
    st.title("The important dates. 🌷")

    with st.form("appointment_form", clear_on_submit=True):
        name = st.text_input(
            "Appointment or event",
            placeholder="e.g. Dentist appointment",
        )
        event_date = st.date_input(
            "Date",
            value=date.today(),
            key="event_date",
        )
        save_event = st.form_submit_button("＋ Save appointment")

    if save_event and name.strip():
        st.session_state.appointments.append({
            "id": str(uuid4()),
            "name": name.strip(),
            "date": event_date,
        })
        st.rerun()

    events = sorted(
        st.session_state.appointments,
        key=lambda event: event["date"],
    )

    if not events:
        st.info("No appointments yet. Add one above.")

    for event in events:
        days = (event["date"] - date.today()).days

        if days < 0:
            status = f"{abs(days)} day(s) ago"
        elif days == 0:
            status = "Today 🎉"
        elif days == 1:
            status = "Tomorrow 🌷"
        else:
            status = f"In {days} days"

        col1, col2 = st.columns([0.78, 0.22])

        with col1:
            st.markdown(f"**{html.escape(event['name'])}**")
            st.caption(
                f"{event['date'].strftime('%A, %d %B %Y')} · {status}"
            )

        with col2:
            if st.button("Remove", key=f"event_remove_{event['id']}"):
                st.session_state.appointments = [
                    x for x in st.session_state.appointments
                    if x["id"] != event["id"]
                ]
                st.rerun()

        st.divider()

# -------------------- FAMILY NOTES --------------------

elif page == "💌 Family Notes & Messages":
    st.title("Notes from the heart. 💌")
    st.write("Leave a kind message or a little reminder for the family.")

    with st.form("note_form", clear_on_submit=True):
        author = st.text_input(
            "From",
            placeholder="e.g. Suchi",
        )
        note = st.text_area(
            "Message",
            placeholder="Remember to take a break today 💛",
        )
        save_note = st.form_submit_button("＋ Pin a note")

    if save_note and note.strip():
        st.session_state.family_notes.insert(0, {
            "id": str(uuid4()),
            "author": author.strip() or "Someone in the family",
            "note": note.strip(),
            "created_at": datetime.now(),
        })
        st.rerun()

    if not st.session_state.family_notes:
        st.info("The family noticeboard is waiting for its first note. 🌷")

    for note in st.session_state.family_notes:
        st.markdown(
            f"""
            <div class="metric-card" style="margin:10px 0;min-height:auto">
                <strong>💌 {html.escape(note['author'])}</strong>
                <p>{html.escape(note['note']).replace(chr(10), '<br>')}</p>
                <small>
                    {note['created_at'].strftime('%d %b %Y · %H:%M')}
                </small>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Remove note", key=f"note_remove_{note['id']}"):
            st.session_state.family_notes = [
                x for x in st.session_state.family_notes
                if x["id"] != note["id"]
            ]
            st.rerun()

# -------------------- SHOPPING HISTORY --------------------

elif page == "🧾 Shopping History":
    st.title("Little shopping memories. 🛍️")
    st.write("Every checked-off grocery is recorded here for this session.")

    history = st.session_state.shopping_history

    if not history:
        st.info("No purchases recorded yet. Your first shopping win goes here!")
    else:
        st.metric("Items purchased", len(history))

        for index, purchase in enumerate(history):
            st.markdown(
                f"**🛍️ {html.escape(purchase['name'])}**"
            )
            st.caption(
                purchase["bought_at"].strftime("%d %B %Y · %H:%M")
            )
            st.divider()

        if st.button("Clear shopping history"):
            st.session_state.shopping_history = []
            st.rerun()

# -------------------- FOOTER --------------------

st.divider()

st.markdown(
    """
    <p style="text-align:center;opacity:.7;font-size:.82rem">
        Made with care · Suchi & Abi's Family Hub 🏡💗
    </p>
    """,
    unsafe_allow_html=True,
)

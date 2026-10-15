
import html
import textwrap
from datetime import date, datetime
import streamlit as st

# =========================================================
# CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Our Family Hub | Suchi & Abi",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# THEMES
# =========================================================
THEMES = {
    "Dark": {
        "bg": "#15171B",
        "sidebar": "#1C1F24",
        "card": "#20242A",
        "text": "#F2F3F5",
        "muted": "#B4BBC6",
        "border": "#373D46",
        "accent": "#B5CDE9",
        "accent_soft": "#303D4B",
        "input": "#252A31",
        "shadow": "0 4px 20px rgba(0, 0, 0, 0.12)",
    },
}
# =========================================================
# SESSION STATE
# =========================================================
DEFAULTS = {
    "theme": "Dark",
    "tasks": [],
    "groceries": [],
    "appointments": [],
    "notes": [],
    "shopping_history": [],
    "mood": "Happy",
    "task_filter": "All",
}

for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value

C = THEMES["Dark"]


# =========================================================
# UTILITIES
# =========================================================
def safe(value):
    """Escape user-entered text before displaying it in HTML."""
    return html.escape(str(value))


def pretty_date(value):
    if isinstance(value, (date, datetime)):
        return value.strftime("%d %b %Y")
    return str(value)


def record_history(action, item):
    st.session_state.shopping_history.append({
        "action": action,
        "item": item,
        "date": datetime.now().strftime("%d %b %Y · %H:%M"),
    })


def card(title, description="", icon="✨", eyebrow=None):
    """Reusable information card rendered with native Streamlit elements.

    Using native widgets here avoids HTML being displayed as literal code
    when Markdown indentation or Streamlit rendering behavior changes.
    """
    with st.container(border=True):
        if eyebrow:
            st.caption(str(eyebrow).upper())
        st.markdown(f"### {safe(icon)}  {safe(title)}")
        if description:
            st.write(description)


def metric_card(label, value, icon, detail):
    st.markdown(
        textwrap.dedent(f"""
        <div class="metric-card">
            <div class="metric-top">
                <span>{safe(label)}</span>
                <span class="metric-icon">{safe(icon)}</span>
            </div>
            <div class="metric-value">{safe(value)}</div>
            <div class="metric-detail">{safe(detail)}</div>
        </div>
        """),
        unsafe_allow_html=True,
    )


def section_title(title, subtitle=None):
    st.markdown(f'<div class="section-title">{safe(title)}</div>',
                unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{safe(subtitle)}</div>',
            unsafe_allow_html=True,
        )


# =========================================================
# GLOBAL PREMIUM STYLING
# =========================================================
st.markdown(
    textwrap.dedent(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    :root {{
        --bg: {C["bg"]};
        --sidebar: {C["sidebar"]};
        --card: {C["card"]};
        --text: {C["text"]};
        --muted: {C["muted"]};
        --border: {C["border"]};
        --accent: {C["accent"]};
        --accent-soft: {C["accent_soft"]};
        --input: {C["input"]};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background: var(--bg);
        color: var(--text);
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMainBlockContainer"] {{
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    section[data-testid="stSidebar"] {{
        background: var(--sidebar);
        border-right: 1px solid var(--border);
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.8rem;
    }}

    .stApp p,
    .stApp label,
    .stApp li,
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp [data-testid="stMarkdownContainer"],
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: var(--text);
    }}

    h1, h2, h3 {{
        letter-spacing: -0.035em;
    }}

    h1, .brand-title {{
        font-family: 'Playfair Display', Georgia, serif !important;
    }}

    .brand-title {{
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--text);
        line-height: 1.2;
    }}

    .brand-subtitle {{
        font-size: 0.84rem;
        color: var(--muted);
        margin-top: 0.35rem;
        line-height: 1.5;
    }}

    .sidebar-label {{
        color: var(--muted);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 1.5rem 0 0.5rem 0;
    }}

    .hero {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: clamp(22px, 4vw, 38px);
        box-shadow: {C["shadow"]};
        margin-bottom: 1.35rem;
    }}

    .hero-kicker {{
        color: var(--accent);
        text-transform: uppercase;
        letter-spacing: 0.14em;
        font-size: 0.72rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
    }}

    .hero-title {{
        font-family: 'Playfair Display', Georgia, serif;
        font-size: clamp(2rem, 4vw, 3.1rem);
        line-height: 1.15;
        letter-spacing: -0.045em;
        color: var(--text);
        margin: 0;
    }}

    .hero-copy {{
        color: var(--muted);
        font-size: 1rem;
        margin-top: 0.8rem;
        line-height: 1.8;
        max-width: 650px;
    }}

    .hero-footer {{
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 1.2rem;
        padding-top: 1rem;
        border-top: 1px solid var(--border);
    }}

    .section-title {{
        font-family: 'Playfair Display', Georgia, serif;
        color: var(--text);
        font-size: 1.55rem;
        font-weight: 600;
        letter-spacing: -0.025em;
        margin: 1.25rem 0 0.25rem 0;
    }}

    .section-subtitle {{
        color: var(--muted);
        font-size: 0.9rem;
        margin-bottom: 1rem;
        line-height: 1.65;
    }}

    .metric-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 19px;
        min-height: 142px;
        box-shadow: {C["shadow"]};
        margin-bottom: 0.7rem;
    }}

    .metric-top {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        color: var(--muted);
        font-size: 0.85rem;
        font-weight: 500;
    }}

    .metric-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 11px;
        background: var(--accent-soft);
        font-size: 1.05rem;
    }}

    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.04em;
        margin-top: 12px;
        color: var(--text);
    }}

    .metric-detail {{
        color: var(--muted);
        font-size: 0.78rem;
        margin-top: 3px;
    }}

    .premium-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 20px;
        box-shadow: {C["shadow"]};
        margin-bottom: 0.75rem;
    }}

    .eyebrow {{
        color: var(--accent);
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }}

    .card-heading {{
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text);
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.6rem;
    }}

    .card-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 35px;
        height: 35px;
        border-radius: 11px;
        background: var(--accent-soft);
        flex-shrink: 0;
    }}

    .card-description {{
        color: var(--muted);
        font-size: 0.88rem;
        line-height: 1.7;
        overflow-wrap: anywhere;
    }}

    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--card);
        border-color: var(--border);
        border-radius: 16px;
        box-shadow: {C["shadow"]};
    }}

    [data-testid="stExpander"] {{
        background: var(--card);
        border-color: var(--border);
        border-radius: 14px;
    }}

    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="select"] > div {{
        background-color: var(--input);
        color: var(--text);
        border-color: var(--border);
        border-radius: 10px;
    }}

    .stApp [data-baseweb="select"] * {{
        color: var(--text);
    }}

    [data-baseweb="popover"],
    [data-baseweb="menu"],
    [role="listbox"] {{
        background-color: var(--card);
        color: var(--text);
    }}

    .stApp .stButton > button,
    .stApp .stDownloadButton > button {{
        background: var(--card);
        color: var(--text);
        border: 1px solid var(--border);
        border-radius: 11px;
        min-height: 42px;
        font-weight: 600;
        transition: border-color 0.15s ease;
    }}

    .stApp .stButton > button:hover,
    .stApp .stDownloadButton > button:hover {{
        border-color: var(--accent);
        color: var(--accent);
    }}

    .stApp [data-testid="stCaptionContainer"] p,
    .stApp small {{
        color: var(--muted);
    }}

    .stApp hr {{
        border-color: var(--border);
        margin: 1.5rem 0;
    }}

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    div[data-testid="stMetric"] {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 15px;
    }}

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
        color: var(--text);
    }}

    a {{
        color: var(--accent);
    }}


    /* Native Streamlit shortcut cards */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: {C["shadow"]};
        padding: 0.25rem;
    }}

    /* Strong overrides for Streamlit/BaseWeb controls in light themes */
    .stApp [data-testid="stExpander"] details,
    .stApp [data-testid="stExpander"] summary,
    .stApp [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"],
    .stApp [data-testid="stExpander"] details > summary {{
        background: var(--card) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
    }}

    .stApp [data-testid="stExpander"] summary *,
    .stApp [data-testid="stExpander"] summary p,
    .stApp [data-testid="stExpander"] summary span {{
        color: var(--text) !important;
        opacity: 1 !important;
    }}

    .stApp [data-testid="stExpander"] > details > div,
    .stApp [data-testid="stExpander"] [data-testid="stExpanderDetails"],
    .stApp [data-testid="stForm"],
    .stApp [data-testid="stVerticalBlockBorderWrapper"] {{
        background-color: var(--card) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
    }}

    .stApp input,
    .stApp textarea,
    .stApp [data-baseweb="input"] input,
    .stApp [data-baseweb="textarea"] textarea {{
        background-color: var(--input) !important;
        color: var(--text) !important;
        -webkit-text-fill-color: var(--text) !important;
        caret-color: var(--text) !important;
        border-color: var(--border) !important;
        opacity: 1 !important;
    }}

    .stApp input::placeholder,
    .stApp textarea::placeholder,
    .stApp [data-baseweb="input"] input::placeholder,
    .stApp [data-baseweb="textarea"] textarea::placeholder {{
        color: var(--muted) !important;
        -webkit-text-fill-color: var(--muted) !important;
        opacity: 1 !important;
    }}

    .stApp [data-baseweb="input"] > div,
    .stApp [data-baseweb="textarea"] > div {{
        background-color: var(--input) !important;
        border-color: var(--border) !important;
    }}

    .stApp [data-testid="stFormSubmitButton"] button,
    .stApp [data-testid="stForm"] button[kind="primary"],
    .stApp button[kind="primary"] {{
        background: var(--accent) !important;
        color: #FFFFFF !important;
        border: 1px solid var(--accent) !important;
        opacity: 1 !important;
        box-shadow: none !important;
    }}

    .stApp [data-testid="stFormSubmitButton"] button *,
    .stApp button[kind="primary"] * {{
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }}

    .stApp .stButton > button,
    .stApp .stDownloadButton > button {{
        background: var(--card) !important;
        color: var(--text) !important;
        border-color: var(--border) !important;
        opacity: 1 !important;
    }}

    .stApp label,
    .stApp [data-testid="stWidgetLabel"] *,
    .stApp [data-testid="stMarkdownContainer"] p,
    .stApp [data-testid="stMarkdownContainer"] span {{
        color: var(--text);
    }}

    /* Readable contrast, resilient cards, and touch-friendly controls */
    .card-heading, .card-description, .metric-value, .metric-detail,
    .hero-title, .hero-copy, .section-title, .section-subtitle,
    .brand-title, .brand-subtitle, .eyebrow {{
        overflow-wrap: anywhere;
        word-break: normal;
    }}

    .card-description, .metric-detail, .hero-copy, .section-subtitle,
    .brand-subtitle, .stApp [data-testid="stCaptionContainer"] p {{
        color: var(--muted) !important;
    }}

    .card-heading, .metric-value, .hero-title, .section-title,
    .brand-title {{
        color: var(--text) !important;
    }}

    .stApp input, .stApp textarea,
    .stApp [data-baseweb="select"] > div {{
        min-height: 44px;
        font-size: 0.98rem;
    }}

    .stApp .stButton > button,
    .stApp .stDownloadButton > button,
    .stApp [data-testid="stFormSubmitButton"] > button {{
        min-height: 46px;
        padding: 0.55rem 1rem;
        white-space: normal;
        overflow-wrap: anywhere;
    }}

    .premium-card, .metric-card {{
        min-width: 0;
        overflow: hidden;
    }}

    [data-testid="stMarkdownContainer"] pre,
    [data-testid="stMarkdownContainer"] code {{
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }}

    @media (max-width: 700px) {{
        [data-testid="stMainBlockContainer"] {{
            padding-top: 1rem;
        }}

        .hero {{
            border-radius: 18px;
            padding: 22px;
        }}

        .metric-card {{
            padding: 14px;
            min-height: 120px;
        }}

        .card-heading {{
            font-size: 1rem;
            align-items: flex-start;
        }}

        .card-icon {{
            width: 32px;
            height: 32px;
        }}

        .section-title {{
            font-size: 1.35rem;
        }}

        .hero-title {{
            font-size: clamp(1.8rem, 8vw, 2.5rem);
        }}

        .stApp [data-testid="stMainBlockContainer"] {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}
    }}
    </style>
    """),
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="brand-title">Our Family Hub</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-subtitle">A calmer way to organise life, together.</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Appearance</div>',
                unsafe_allow_html=True)
    st.caption("Dark theme · Always on")

    st.markdown('<div class="sidebar-label">Your space</div>',
                unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        [
            "Home",
            "Tasks",
            "Groceries",
            "Appointments",
            "Family Notes",
            "Shopping History",
        ],
        format_func=lambda x: {
            "Home": "🏡   Home",
            "Tasks": "✓   Tasks",
            "Groceries": "🛒   Groceries",
            "Appointments": "▦   Appointments",
            "Family Notes": "♡   Family Notes",
            "Shopping History": "↗   Shopping History",
        }[x],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption("MADE FOR TWO")
    st.markdown("**Suchi & Abi** 💗")
    st.caption("Small steps, big love.")

# Recalculate after selecting the theme.
C = THEMES["Dark"]

# Streamlit reruns after a theme change; the CSS above uses the
# theme value available at the start of that rerun.


# =========================================================
# HERO
# =========================================================
today = date.today()

st.markdown(
    textwrap.dedent(f"""
    <div class="hero">
        <div class="hero-kicker">YOUR HOME · YOUR LITTLE WORLD</div>
        <div class="hero-title">A little more organised.<br>A little more together.</div>
        <div class="hero-copy">
            Welcome back, Suchi &amp; Abi. Keep track of everyday things,
            make space for the good moments, and take life one step at a time.
        </div>
        <div class="hero-footer">
            {today.strftime("%A, %d %B %Y")} &nbsp; · &nbsp; Made with love ♡
        </div>
    </div>
    """),
    unsafe_allow_html=True,
)

# =========================================================
# HOME
# =========================================================
if page == "Home":
    pending = sum(not t["done"] for t in st.session_state.tasks)
    bought = sum(g["bought"] for g in st.session_state.groceries)
    remaining_groceries = len(st.session_state.groceries) - bought

    upcoming = sum(
        a["date"] >= today for a in st.session_state.appointments
    )

    m1, m2, m3 = st.columns(3)

    with m1:
        metric_card("Open tasks", pending, "✓", "Little things, one step at a time")

    with m2:
        metric_card("Shopping list", remaining_groceries, "🛒", "Items still to pick up")

    with m3:
        metric_card("Coming up", upcoming, "▦", "Future appointments")

    section_title("Your day, at a glance", "A little overview of what needs your attention.")

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        card(
            "A gentle reminder",
            "You don't need to do everything today. Choose what matters, "
            "help each other where you can, and leave a little room to rest.",
            "♡",
            "A NOTE FOR US",
        )

        st.markdown("#### Tasks to tackle")

        open_tasks = [t for t in st.session_state.tasks if not t["done"]]

        if open_tasks:
            for task in open_tasks[:5]:
                with st.container(border=True):
                    st.markdown(f"**{safe(task['name'])}**")
                    st.caption(
                        f"{task['assigned']} · {task['priority']} priority"
                    )
        else:
            st.success("All caught up! Time for a little breathing room.")

        if st.button("Open task list →", use_container_width=True):
            st.session_state["_jump_page"] = "Tasks"
            st.rerun()

    with right:
        card(
            "Our daily mood",
            "Check in with yourselves. A tiny moment of reflection "
            "can make a busy day feel a little lighter.",
            "☀️",
            "HOW ARE WE FEELING?",
        )

        moods = [
            "Happy",
            "Relaxed",
            "Grateful",
            "Busy",
            "Tired",
            "Need a little love",
        ]

        st.selectbox(
            "Today's mood",
            moods,
            key="mood",
        )

        mood_copy = {
            "Happy": "Enjoy the lovely moments. ☀️",
            "Relaxed": "Keep that peaceful feeling close. 🌿",
            "Grateful": "Notice the little things that make life sweet. 💗",
            "Busy": "One thing at a time. You have got this. 🌸",
            "Tired": "Rest counts, too. Be kind to yourselves. ☁️",
            "Need a little love": "A kind word or a hug can go a long way. ♡",
        }

        st.info(mood_copy[st.session_state.mood])

        st.markdown("#### Next appointment")

        future_appointments = sorted(
            [a for a in st.session_state.appointments if a["date"] >= today],
            key=lambda a: (a["date"], a["time"]),
        )

        if future_appointments:
            a = future_appointments[0]
            card(
                a["title"],
                f"{pretty_date(a['date'])} · {a['time']}"
                + (f" · {a['location']}" if a["location"] else ""),
                "📅",
            )
        else:
            st.caption("Nothing scheduled just yet.")

    st.markdown("---")
    section_title("Little things to remember", "Your home hub, all in one place.")

    # Native Streamlit cards: reliable rendering (no raw HTML in Markdown).
    q1, q2, q3 = st.columns(3, gap="large")

    with q1:
        with st.container(border=True):
            st.markdown("### ✓  Tasks")
            st.write("Share responsibilities and celebrate each finished task.")
            if st.button("Open tasks →", key="home_open_tasks", use_container_width=True):
                st.session_state["_jump_page"] = "Tasks"
                st.rerun()

    with q2:
        with st.container(border=True):
            st.markdown("### 🛒  Groceries")
            st.write("Keep your shopping list simple and up to date.")
            if st.button("Open groceries →", key="home_open_groceries", use_container_width=True):
                st.session_state["_jump_page"] = "Groceries"
                st.rerun()

    with q3:
        with st.container(border=True):
            st.markdown("### ♡  Family notes")
            st.write("Save messages, reminders, and little memories.")
            if st.button("Open notes →", key="home_open_notes", use_container_width=True):
                st.session_state["_jump_page"] = "Family Notes"
                st.rerun()


# =========================================================
# TASKS
# =========================================================
elif page == "Tasks":
    section_title("Our tasks", "Plan together without making the day feel complicated.")

    with st.expander("＋ Add a new task", expanded=not st.session_state.tasks):
        with st.form("task_form", clear_on_submit=True):
            name = st.text_input("What needs doing?", placeholder="Tidy the living room")
            c1, c2 = st.columns(2)
            with c1:
                assigned = st.selectbox("Who's taking it?", ["Both", "Suchi", "Abi"])
            with c2:
                priority = st.selectbox("Priority", ["Normal", "High", "Low"])

            has_due = st.checkbox("Add a due date")
            due = st.date_input("Due date", value=today) if has_due else None

            if st.form_submit_button("Add task", use_container_width=True):
                if name.strip():
                    st.session_state.tasks.append({
                        "name": name.strip(),
                        "assigned": assigned,
                        "priority": priority,
                        "due": due,
                        "done": False,
                    })
                    st.rerun()
                else:
                    st.warning("Please enter a task name.")

    total = len(st.session_state.tasks)
    completed = sum(t["done"] for t in st.session_state.tasks)
    progress = completed / total if total else 0

    st.markdown("#### Your progress")
    st.progress(progress, text=f"{completed} of {total} tasks completed")

    selected_filter = st.segmented_control(
        "Filter tasks",
        options=["All", "Open", "Completed"],
        default="All",
        key="task_filter",
    )

    tasks = list(enumerate(st.session_state.tasks))

    if selected_filter == "Open":
        tasks = [(i, t) for i, t in tasks if not t["done"]]
    elif selected_filter == "Completed":
        tasks = [(i, t) for i, t in tasks if t["done"]]

    if not tasks:
        st.info("Nothing to show here. Add a task whenever you're ready.")
    else:
        for i, task in tasks:
            with st.container(border=True):
                c1, c2, c3 = st.columns([0.1, 0.68, 0.22])

                with c1:
                    checked = st.checkbox(
                        "Complete",
                        value=task["done"],
                        key=f"task_check_{i}",
                        label_visibility="collapsed",
                    )

                if checked != task["done"]:
                    st.session_state.tasks[i]["done"] = checked
                    st.rerun()

                with c2:
                    if task["done"]:
                        st.markdown(f"~~{safe(task['name'])}~~")
                    else:
                        st.markdown(f"**{safe(task['name'])}**")

                    due_text = (
                        pretty_date(task["due"]) if task["due"] else "No due date"
                    )
                    st.caption(
                        f"{task['assigned']} · {task['priority']} priority · {due_text}"
                    )

                with c3:
                    if st.button("Delete", key=f"task_delete_{i}"):
                        st.session_state.tasks.pop(i)
                        st.rerun()


# =========================================================
# GROCERIES
# =========================================================
elif page == "Groceries":
    section_title("Grocery list", "A calmer shopping trip starts with a simple list.")

    with st.expander("＋ Add grocery item", expanded=not st.session_state.groceries):
        with st.form("grocery_form", clear_on_submit=True):
            name = st.text_input("Item", placeholder="Fresh strawberries")
            quantity = st.text_input("Quantity", placeholder="2 packs")
            if st.form_submit_button("Add to list", use_container_width=True):
                if name.strip():
                    st.session_state.groceries.append({
                        "name": name.strip(),
                        "quantity": quantity.strip() or "As needed",
                        "bought": False,
                    })
                    record_history("Added", name.strip())
                    st.rerun()
                else:
                    st.warning("Please enter an item.")

    items = st.session_state.groceries
    remaining = sum(not item["bought"] for item in items)
    st.caption(f"{remaining} items left to pick up")

    if not items:
        card("Your list is clear", "Add groceries above whenever you need them.", "🛒")
    else:
        for i, item in enumerate(items):
            with st.container(border=True):
                c1, c2, c3 = st.columns([0.1, 0.68, 0.22])

                with c1:
                    checked = st.checkbox(
                        "Bought",
                        value=item["bought"],
                        key=f"grocery_check_{i}",
                        label_visibility="collapsed",
                    )

                if checked != item["bought"]:
                    st.session_state.groceries[i]["bought"] = checked
                    if checked:
                        record_history("Marked as bought", item["name"])
                    st.rerun()

                with c2:
                    st.markdown(
                        f"~~{safe(item['name'])}~~"
                        if item["bought"] else f"**{safe(item['name'])}**"
                    )
                    st.caption(f"Quantity: {safe(item['quantity'])}")

                with c3:
                    if st.button("Remove", key=f"grocery_delete_{i}"):
                        record_history("Removed", item["name"])
                        st.session_state.groceries.pop(i)
                        st.rerun()

        if st.button("Clear purchased items"):
            st.session_state.groceries = [
                item for item in items if not item["bought"]
            ]
            st.rerun()


# =========================================================
# APPOINTMENTS
# =========================================================
elif page == "Appointments":
    section_title("Appointments", "Keep the important dates close at hand.")

    with st.expander("＋ Add appointment", expanded=not st.session_state.appointments):
        with st.form("appointment_form", clear_on_submit=True):
            title = st.text_input("What's happening?", placeholder="Family dinner")
            c1, c2 = st.columns(2)
            with c1:
                appointment_date = st.date_input("Date", value=today)
            with c2:
                appointment_time = st.time_input("Time")

            location = st.text_input("Location", placeholder="Optional")
            details = st.text_area("Notes", placeholder="Anything to remember?")

            if st.form_submit_button("Save appointment", use_container_width=True):
                if title.strip():
                    st.session_state.appointments.append({
                        "title": title.strip(),
                        "date": appointment_date,
                        "time": appointment_time.strftime("%H:%M"),
                        "location": location.strip(),
                        "notes": details.strip(),
                    })
                    st.rerun()
                else:
                    st.warning("Please enter an appointment title.")

    appointments = sorted(
        enumerate(st.session_state.appointments),
        key=lambda x: (x[1]["date"], x[1]["time"]),
    )

    if not appointments:
        card("A little breathing room", "No appointments added yet.", "📅")
    else:
        for i, a in appointments:
            with st.container(border=True):
                c1, c2 = st.columns([0.78, 0.22])

                with c1:
                    st.markdown(f"### {safe(a['title'])}")
                    st.caption(f"📅 {pretty_date(a['date'])} · 🕒 {a['time']}")
                    if a["location"]:
                        st.write(f"**Location:** {safe(a['location'])}")
                    if a["notes"]:
                        st.write(a["notes"])

                    if a["date"] < today:
                        st.caption("Past appointment")

                with c2:
                    if st.button("Delete", key=f"appointment_delete_{i}"):
                        st.session_state.appointments.pop(i)
                        st.rerun()


# =========================================================
# FAMILY NOTES
# =========================================================
elif page == "Family Notes":
    section_title("Family notes", "Messages, reminders, and memories worth keeping.")

    with st.expander("＋ Write a note", expanded=not st.session_state.notes):
        with st.form("note_form", clear_on_submit=True):
            title = st.text_input("Title", placeholder="A little reminder")
            body = st.text_area(
                "Your note",
                placeholder="Write something you want to remember...",
                height=140,
            )

            if st.form_submit_button("Save note", use_container_width=True):
                if body.strip():
                    st.session_state.notes.append({
                        "title": title.strip() or "A little note",
                        "body": body.strip(),
                        "created": datetime.now().strftime("%d %b %Y · %H:%M"),
                    })
                    st.rerun()
                else:
                    st.warning("Write a note before saving.")

    if not st.session_state.notes:
        card("A space for your thoughts", "Your saved notes will appear here.", "♡")
    else:
        for i in range(len(st.session_state.notes) - 1, -1, -1):
            note = st.session_state.notes[i]
            with st.container(border=True):
                st.markdown(f"### ♡ {safe(note['title'])}")
                st.caption(note["created"])
                st.write(note["body"])

                if st.button("Delete note", key=f"note_delete_{i}"):
                    st.session_state.notes.pop(i)
                    st.rerun()


# =========================================================
# SHOPPING HISTORY
# =========================================================
elif page == "Shopping History":
    section_title("Shopping history", "A simple record of changes to your grocery list.")

    history = st.session_state.shopping_history

    if not history:
        card("Your history starts here", "Add or update grocery items to see activity.", "↗")
    else:
        st.caption(f"{len(history)} recorded actions")

        for entry in reversed(history):
            with st.container(border=True):
                st.markdown(f"**{safe(entry['action'])}**")
                st.write(safe(entry["item"]))
                st.caption(entry["date"])

        if st.button("Clear history"):
            st.session_state.shopping_history = []
            st.rerun()


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    textwrap.dedent(f"""
    <div style="
        text-align: center;
        color: {C["muted"]};
        padding: 14px 0 8px 0;
        font-size: 0.85rem;
        line-height: 1.9;
    ">
        <span style="color: {C["accent"]};">♡</span>
        &nbsp; Suchi &amp; Abi &nbsp; · &nbsp; Our little corner of the world
        <br>
        <span style="font-size: 0.78rem;">
            Small steps, big love.
        </span>
    </div>
    """),
    unsafe_allow_html=True,
)

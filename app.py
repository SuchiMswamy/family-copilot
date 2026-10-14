
import streamlit as st
from datetime import date
from supabase import create_client

# ---------- Page setup ----------
st.set_page_config(
    page_title="Our Family Hub",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Supabase connection ----------
try:
    if "supabase_client" not in st.session_state:
        st.session_state.supabase_client = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"],
        )
    supabase = st.session_state.supabase_client
except Exception:
    st.error(
        "Unable to connect to Supabase. Please check "
        "SUPABASE_URL and SUPABASE_KEY in Streamlit Secrets."
    )
    st.stop()

# ---------- Login ----------
if "family_user" not in st.session_state:
    st.markdown("# 🏡 Our Family Hub")
    st.subheader("Welcome back 💛")
    st.write("Sign in to access your family's private space.")

    with st.form("family_login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button(
            "Sign in",
            use_container_width=True,
        )

    if submitted:
        try:
            response = supabase.auth.sign_in_with_password({
                "email": email.strip(),
                "password": password,
            })
            if response.user:
                st.session_state.family_user = response.user
                st.rerun()
            else:
                st.error("Sign-in failed. Please check your details.")
        except Exception:
            st.error(
                "Sign-in failed. Check your email and password. "
                "If your account requires email confirmation, "
                "confirm your email first."
            )

    st.stop()

# ---------- Theme palettes ----------
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

# ---------- Sidebar and theme selector ----------
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

# ---------- Dynamic design ----------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

    .stApp {{
        background: {bg} !important;
        color: {text_color} !important;
        font-family: 'DM Sans', sans-serif;
    }}

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"] {{
        background: {bg} !important;
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

    h1 {{ font-size: 2.6rem !important; }}

    p, label, [data-testid="stMarkdownContainer"] {{
        color: {text_color};
    }}

    .eyebrow {{
        color: {text_color};
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.75rem;
        font-weight: 700;
    }}

    .hero {{
        background: linear-gradient(120deg, {a0}, {a3});
        padding: 30px 32px;
        border-radius: 22px;
        border: 1px solid {a1};
        margin: 12px 0 24px 0;
    }}

    .hero h1, .hero p, .hero .eyebrow {{
        color: {text_color} !important;
    }}

    .hero h1 {{ margin: 8px 0 4px 0; }}
    .hero p {{ font-size: 1.05rem; margin-bottom: 0; }}

    .metric-card {{
        background: {surface};
        border: 1px solid {a1};
        border-radius: 18px;
        padding: 20px;
        min-height: 115px;
    }}

    .metric-label, .small-note {{
        color: {text_color};
        font-size: 0.9rem;
    }}

    .metric-value {{
        color: {text_color};
        font-family: 'Playfair Display', Georgia, serif;
        font-size: 2rem;
        font-weight: 600;
        margin-top: 6px;
    }}

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] button {{
        background: {a2} !important;
        color: {button_text} !important;
        border: 1px solid {a1} !important;
        border-radius: 11px;
        padding: 0.55rem 1rem;
        font-weight: 600;
    }}

    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] button:hover {{
        filter: brightness(0.94);
    }}

    div[data-testid="stForm"] {{
        background: {surface};
        border: 1px solid {a1};
        border-radius: 16px;
        padding: 18px;
    }}

    input, textarea,
    [data-baseweb="input"],
    [data-baseweb="select"] {{
        border-radius: 10px !important;
    }}

    [data-testid="stCheckbox"] label,
    [data-testid="stCheckbox"] p {{
        color: {text_color} !important;
    }}

    [data-testid="stAlert"] {{
        background: {a0};
        color: {text_color};
    }}

    hr {{
        border-color: {a1} !important;
    }}

    .small-note {{ font-size: 0.85rem; }}
</style>
""", unsafe_allow_html=True)

# ---------- Temporary data ----------
# Tasks, groceries, and appointments are currently session-only.
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "groceries" not in st.session_state:
    st.session_state.groceries = []
if "appointments" not in st.session_state:
    st.session_state.appointments = []

# ---------- Main navigation ----------
with st.sidebar:
    st.divider()
    st.caption(f"Signed in as {st.session_state.family_user.email}")

    if st.button("Sign out", use_container_width=True):
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        st.session_state.pop("family_user", None)
        st.rerun()

    page = st.radio(
        "YOUR FAMILY SPACE",
        [
            "✨ Home",
            "✅ To-do list",
            "🛒 Groceries",
            "📅 Appointments",
            "💌 Family Notes & Messages",
        ],
        label_visibility="visible",
    )

    st.divider()
    st.markdown("**Made for your family**")
    st.caption("One place for the little things that keep life moving.")

# ---------- Home ----------
if page == "✨ Home":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">YOUR FAMILY DASHBOARD</div>
        <h1>A calmer kind of busy.</h1>
        <p>Keep track of the little things, so you have more time for the big things.</p>
    </div>
    """, unsafe_allow_html=True)

    pending = len(st.session_state.tasks)
    grocery_count = len(st.session_state.groceries)
    appointment_count = len(st.session_state.appointments)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">✅ Family tasks</div>
            <div class="metric-value">{pending}</div>
            <div class="small-note">On your list</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">🛒 Groceries</div>
            <div class="metric-value">{grocery_count}</div>
            <div class="small-note">Items to remember</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">📅 Appointments</div>
            <div class="metric-value">{appointment_count}</div>
            <div class="small-note">Saved in this session</div>
        </div>""", unsafe_allow_html=True)

    st.write("")
    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("### 🌿 Today's to-dos")

        with st.form("home_task_form", clear_on_submit=True):
            task = st.text_input(
                "What needs doing?",
                placeholder="e.g. Pick up a prescription",
            )
            submitted = st.form_submit_button(
                "＋ Add a task",
                use_container_width=True,
            )
            if submitted and task.strip():
                st.session_state.tasks.append(task.strip())
                st.rerun()

        if st.session_state.tasks:
            for i, item in enumerate(st.session_state.tasks):
                st.checkbox(item, key=f"home_task_{i}")
        else:
            st.info("Your list is clear. Add a task whenever you need to!")

    with right:
        st.markdown("### 🥑 Grocery notes")

        with st.form("home_grocery_form", clear_on_submit=True):
            grocery = st.text_input(
                "What are we running out of?",
                placeholder="e.g. Milk, bananas",
            )
            submitted = st.form_submit_button(
                "＋ Add groceries",
                use_container_width=True,
            )
            if submitted and grocery.strip():
                st.session_state.groceries.append(grocery.strip())
                st.rerun()

        if st.session_state.groceries:
            for i, item in enumerate(st.session_state.groceries):
                st.checkbox(item, key=f"home_grocery_{i}")
        else:
            st.info("Your shopping list is waiting for its first item.")

    st.markdown("### 📅 Coming up")

    if st.session_state.appointments:
        for item in sorted(
            st.session_state.appointments,
            key=lambda x: x["date"],
        ):
            st.markdown(
                f"**{item['name']}** · "
                f"{item['date'].strftime('%d %b %Y')}"
            )
    else:
        st.caption(
            "No appointments added yet. You can add one in Appointments."
        )

# ---------- To-do list ----------
elif page == "✅ To-do list":
    st.markdown(
        '<div class="eyebrow">THE FAMILY CHECKLIST</div>',
        unsafe_allow_html=True,
    )
    st.title("One thing at a time. 🌱")
    st.write("Get it out of your head and onto the list.")

    with st.form("task_form", clear_on_submit=True):
        task = st.text_input(
            "New task",
            placeholder="e.g. Book the dentist",
        )
        submitted = st.form_submit_button(
            "＋ Add task",
            use_container_width=True,
        )
        if submitted and task.strip():
            st.session_state.tasks.append(task.strip())
            st.rerun()

    st.write("")

    if st.session_state.tasks:
        for i, item in enumerate(st.session_state.tasks):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.checkbox(item, key=f"todo_page_{i}")
            with c2:
                if st.button("Remove", key=f"remove_task_{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()

        if st.button("Clear all tasks"):
            st.session_state.tasks = []
            st.rerun()
    else:
        st.success("Nothing on the list yet. Enjoy the breathing room!")

# ---------- Groceries ----------
elif page == "🛒 Groceries":
    st.markdown(
        '<div class="eyebrow">THE SHOPPING LIST</div>',
        unsafe_allow_html=True,
    )
    st.title("A little list, a smoother shop. 🥑")
    st.write("Add what you need as soon as you think of it.")

    with st.form("grocery_form", clear_on_submit=True):
        grocery = st.text_input(
            "Grocery item",
            placeholder="e.g. Oats",
        )
        submitted = st.form_submit_button(
            "＋ Add item",
            use_container_width=True,
        )
        if submitted and grocery.strip():
            st.session_state.groceries.append(grocery.strip())
            st.rerun()

    if st.session_state.groceries:
        st.markdown("### Your list")

        for i, item in enumerate(st.session_state.groceries):
            c1, c2 = st.columns([5, 1])
            with c1:
                st.checkbox(item, key=f"grocery_page_{i}")
            with c2:
                if st.button("Remove", key=f"remove_grocery_{i}"):
                    st.session_state.groceries.pop(i)
                    st.rerun()

        if st.button("Clear shopping list"):
            st.session_state.groceries = []
            st.rerun()
    else:
        st.info("Your list is empty. Add your first item above.")

# ---------- Appointments ----------
elif page == "📅 Appointments":
    st.markdown(
        '<div class="eyebrow">FAMILY CALENDAR</div>',
        unsafe_allow_html=True,
    )
    st.title("The important dates. 🌷")
    st.write("Keep appointments and family plans in one place.")

    with st.form("appointment_form", clear_on_submit=True):
        name = st.text_input(
            "Appointment or event",
            placeholder="e.g. Dentist appointment",
        )
        appointment_date = st.date_input("Date", value=date.today())
        submitted = st.form_submit_button(
            "＋ Save appointment",
            use_container_width=True,
        )

        if submitted and name.strip():
            st.session_state.appointments.append({
                "name": name.strip(),
                "date": appointment_date,
            })
            st.rerun()

    st.markdown("### Your appointments")

    if st.session_state.appointments:
        sorted_appointments = sorted(
            st.session_state.appointments,
            key=lambda x: x["date"],
        )

        for i, item in enumerate(sorted_appointments):
            c1, c2 = st.columns([5, 1])

            with c1:
                st.markdown(f"**{item['name']}**")
                st.caption(item["date"].strftime("%A, %d %B %Y"))

            with c2:
                if st.button(
                    "Remove",
                    key=f"remove_appointment_{i}_{item['name']}",
                ):
                    st.session_state.appointments.remove(item)
                    st.rerun()

            st.divider()
    else:
        st.info("No appointments yet. Add one above to get started.")

# ---------- Shared Family Notes & Messages ----------
elif page == "💌 Family Notes & Messages":
    st.markdown(
        '<div class="eyebrow">YOUR LITTLE FAMILY NOTICEBOARD</div>',
        unsafe_allow_html=True,
    )
    st.title("Notes from the heart. 💌")
    st.write(
        "Leave a note, share a reminder, or send each other a message."
    )

    with st.form("family_message_form", clear_on_submit=True):
        message_type = st.selectbox(
            "What would you like to leave?",
            ["Note", "Message"],
        )
        title = st.text_input(
            "Title",
            placeholder="e.g. Weekend plans",
        )
        body = st.text_area(
            "Your note or message",
            placeholder="Write something for your family...",
        )

        submitted = st.form_submit_button(
            "＋ Save to our family space",
            use_container_width=True,
        )

        if submitted:
            if not title.strip() or not body.strip():
                st.warning("Please enter both a title and a message.")
            else:
                try:
                    supabase.table("family_messages").insert({
                        "author": st.session_state.family_user.email,
                        "message_type": message_type,
                        "title": title.strip(),
                        "body": body.strip(),
                    }).execute()

                    st.success("Your note has been saved! 💛")
                    st.rerun()

                except Exception:
                    st.error(
                        "We couldn't save your note. Please check your "
                        "Supabase connection and database permissions."
                    )

    st.divider()
    st.subheader("Our family noticeboard")

    try:
        result = (
            supabase.table("family_messages")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        messages = result.data or []

        if not messages:
            st.info("No notes yet. Leave the first one!")
        else:
            for message in messages:
                with st.container(border=True):
                    st.caption(
                        f"{message['message_type']} · "
                        f"From {message['author']} · "
                        f"{message['created_at'][:16].replace('T', ' ')}"
                    )
                    st.markdown(f"**{message['title']}**")
                    st.write(message["body"])

    except Exception:
        st.error(
            "We couldn't load your family notes. Please check your "
            "Supabase connection and database permissions."
        )

# ---------- Footer ----------
st.divider()
st.markdown(
    '<p style="text-align:center;color:#849083;font-size:0.8rem;">'
    'Made with care · Our Family Hub 🏡</p>',
    unsafe_allow_html=True,
)

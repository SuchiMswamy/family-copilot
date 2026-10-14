import streamlit as st
from datetime import date, datetime, timedelta
from uuid import uuid4
import html

# ============================================================
# Our Family Hub — enhanced edition
# Features: persistent-in-session checkboxes, hug celebration
# when groceries are bought, gentle overdue nudges, priorities,
# due dates, progress, streak-like wins, notes, and appointments.
# ============================================================

st.set_page_config(
    page_title="Our Family Hub",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

# ---------- Session data ----------
for key, default in {
    "tasks": [],
    "groceries": [],
    "appointments": [],
    "family_notes": [],
    "recent_celebration": None,
    "completed_total": 0,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

def new_item(name, priority="Normal", due=None):
    now = datetime.now()
    return {
        "id": str(uuid4()),
        "name": name.strip(),
        "checked": False,
        "created_at": now,
        "checked_at": None,
        "priority": priority,
        "due": due,
    }

def age_days(item):
    created = item.get("created_at")
    if not created:
        return 0
    if isinstance(created, date) and not isinstance(created, datetime):
        created = datetime.combine(created, datetime.min.time())
    return max(0, (datetime.now() - created).days)

def render_hug(message="Shopping mission accomplished!"):
    st.markdown(f"""
    <div class="hug-scene">
      <div class="sparkle s1">✨</div><div class="sparkle s2">💗</div>
      <div class="hug-people">
        <div class="person girl"><span class="hair">●</span><span class="face">☺</span><span class="body">♥</span></div>
        <div class="person boy"><span class="hair">●</span><span class="face">☺</span><span class="body">♥</span></div>
        <div class="hug-heart">💞</div>
      </div>
      <div class="hug-message">{html.escape(message)}</div>
      <div class="hug-subtitle">Teamwork looks good on you two 🥹</div>
    </div>
    """, unsafe_allow_html=True)

def show_item_list(items, kind, prefix):
    """Checkboxes are keyed by stable item IDs, so checking one won't shift others."""
    if not items:
        st.info("Nothing here right now. Enjoy the breathing room! 🌿")
        return

    overdue_count = 0
    for item in sorted(items, key=lambda x: (x["checked"], x.get("due") or date.max, x["created_at"])):
        item_id = item["id"]
        label = item["name"]
        days_old = age_days(item)
        overdue = not item["checked"] and days_old >= 3
        due_date = item.get("due")
        past_due = not item["checked"] and due_date and due_date < date.today()
        if overdue or past_due:
            overdue_count += 1

        left, middle, right = st.columns([0.08, 0.72, 0.20])
        with left:
            checked_now = st.checkbox(
                "Done",
                value=item["checked"],
                key=f"{prefix}_check_{item_id}",
                label_visibility="collapsed",
            )
        if checked_now != item["checked"]:
            item["checked"] = checked_now
            item["checked_at"] = datetime.now() if checked_now else None
            if checked_now:
                st.session_state.completed_total += 1
                if kind == "grocery":
                    st.session_state.recent_celebration = f"You bought {label}!"
                st.rerun()
        with middle:
            safe_name = html.escape(label)
            if item["checked"]:
                st.markdown(f"<div class='item-name completed'>{safe_name}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='item-name'>{safe_name}</div>", unsafe_allow_html=True)
            details = []
            if item.get("priority") and item["priority"] != "Normal":
                details.append(f"Priority: {item['priority']}")
            if due_date:
                details.append(f"Due {due_date.strftime('%d %b')}")
            if item["checked"] and item.get("checked_at"):
                details.append("Done ✓")
            elif overdue:
                details.append(f"Waiting {days_old} days")
            if past_due:
                details.append("Past due")
            if details:
                st.caption(" · ".join(details))
            if overdue or past_due:
                st.markdown(
                    "<div class='gentle-nudge'>🥺 This has been waiting a while. "
                    "Could you tackle it today, or change its due date?</div>",
                    unsafe_allow_html=True,
                )
        with right:
            if st.button("Remove", key=f"{prefix}_remove_{item_id}"):
                items[:] = [x for x in items if x["id"] != item_id]
                st.rerun()
        st.divider()

    if overdue_count:
        st.caption(f"💛 A gentle nudge: {overdue_count} item(s) may need a little attention.")

# ---------- Theme selector ----------
with st.sidebar:
    st.markdown("# 🏡 Our Family Hub")
    st.caption("A little more organised, a little less stressed.")
    theme_name = st.selectbox("🎨 Choose your theme", list(THEMES.keys()), key="family_theme")

theme = THEMES[theme_name]
bg, text_color, surface = theme["bg"], theme["text"], theme["surface"]
a0, a1, a2, a3 = theme["accents"]
button_text = theme["button_text"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
    background: {bg} !important; color: {text_color} !important;
    font-family: 'DM Sans', sans-serif;
}}
[data-testid="stSidebar"] {{ background:{surface}!important; border-right:1px solid {a1}!important; }}
[data-testid="stSidebar"] * {{ color:{text_color}; }}
h1,h2,h3 {{ color:{text_color}!important; font-family:'Playfair Display',Georgia,serif!important; }}
h1 {{ font-size:2.5rem!important; }}
p,label,[data-testid="stMarkdownContainer"] {{ color:{text_color}; }}
.hero {{ background:linear-gradient(120deg,{a0},{a3}); padding:30px 32px; border-radius:22px; border:1px solid {a1}; margin:12px 0 24px; }}
.hero h1,.hero p,.hero .eyebrow {{ color:{text_color}!important; }}
.eyebrow {{ text-transform:uppercase; letter-spacing:2px; font-size:.75rem; font-weight:700; }}
.metric-card {{ background:{surface}; border:1px solid {a1}; border-radius:18px; padding:18px; min-height:112px; }}
.metric-label {{ font-size:.9rem; }} .metric-value {{ font:600 2rem 'Playfair Display',Georgia,serif; margin-top:6px; }}
div.stButton>button, div[data-testid="stFormSubmitButton"] button {{ background:{a2}!important; color:{button_text}!important; border:1px solid {a1}!important; border-radius:11px; min-height:44px; font-weight:600; }}
div[data-testid="stForm"] {{ background:{surface}; border:1px solid {a1}; border-radius:16px; padding:18px; }}
input,textarea,[data-baseweb="input"],[data-baseweb="select"] {{ border-radius:10px!important; }}
[data-testid="stCheckbox"] label,[data-testid="stCheckbox"] p {{ color:{text_color}!important; }}
hr {{ border-color:{a1}!important; }}
.item-name {{ font-size:1.02rem; font-weight:600; padding-top:4px; overflow-wrap:anywhere; }}
.completed {{ text-decoration:line-through; opacity:.55; }}
.gentle-nudge {{ display:inline-block; background:{a0}; border:1px solid {a1}; border-radius:10px; padding:7px 10px; font-size:.86rem; margin:3px 0 5px; }}
.hug-scene {{ position:relative; overflow:hidden; text-align:center; padding:18px; margin:12px 0 22px; border-radius:22px; background:linear-gradient(135deg,{a0},{a3}); border:1px solid {a1}; }}
.hug-people {{ height:120px; position:relative; display:flex; align-items:center; justify-content:center; gap:0; }}
.person {{ position:relative; width:82px; height:100px; animation:bounce 1.1s ease-in-out infinite alternate; }}
.person .hair {{ position:absolute; top:2px; left:27px; font-size:40px; color:#5b3a2e; }}
.person .face {{ position:absolute; top:17px; left:29px; font-size:29px; color:#5b3a2e; z-index:2; }}
.person .body {{ position:absolute; top:49px; left:17px; font-size:58px; color:#e78bab; }}
.boy .body {{ color:#83b9d5; }} .boy {{ animation-delay:.15s; }}
.hug-heart {{ position:absolute; left:calc(50% - 17px); top:35px; font-size:32px; animation:heartbeat .75s ease-in-out infinite; }}
.sparkle {{ position:absolute; font-size:24px; animation:floaty 2s ease-in-out infinite; }}
.s1 {{ left:18%; top:18px; }} .s2 {{ right:18%; top:24px; animation-delay:.4s; }}
.hug-message {{ font-size:1.2rem; font-weight:700; }} .hug-subtitle {{ font-size:.9rem; margin-top:3px; }}
@keyframes bounce {{ from {{ transform:translateY(2px) rotate(-3deg); }} to {{ transform:translateY(-5px) rotate(3deg); }} }}
@keyframes heartbeat {{ 0%,100% {{ transform:scale(1); }} 50% {{ transform:scale(1.25); }} }}
@keyframes floaty {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-10px); }} }}
@media(max-width:768px) {{
 .block-container {{ padding:.8rem .8rem 2rem!important; }}
 h1 {{ font-size:1.85rem!important; }}
 .hero {{ padding:20px 16px; border-radius:16px; }}
 .metric-card {{ padding:14px; margin-bottom:8px; min-height:auto; }}
 .metric-value {{ font-size:1.65rem; }}
 div[data-testid="stForm"] {{ padding:12px; }}
 div.stButton>button,div[data-testid="stFormSubmitButton"] button {{ min-height:46px; white-space:normal; }}
 [data-testid="stHorizontalBlock"] {{ gap:.5rem!important; }}
}}
@media(prefers-reduced-motion: reduce) {{
 .person,.hug-heart,.sparkle {{ animation:none!important; }}
}}
</style>
""", unsafe_allow_html=True)

# ---------- Header and navigation ----------
st.markdown("## 🏡 Our Family Hub")
st.caption("A little more organised, a little less stressed.")
pages = ["✨ Home", "✅ To-do list", "🛒 Groceries", "📅 Appointments", "💌 Family Notes & Messages"]
page = st.selectbox("📍 Where would you like to go?", pages, key="main_page_navigation")
st.divider()

# ---------- Home ----------
if page == "✨ Home":
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">YOUR FAMILY DASHBOARD</div>
      <h1>A calmer kind of busy.</h1>
      <p>Keep track of the little things, so you have more time for the big things.</p>
    </div>
    """, unsafe_allow_html=True)

    open_tasks = sum(not x["checked"] for x in st.session_state.tasks)
    open_groceries = sum(not x["checked"] for x in st.session_state.groceries)
    upcoming = sum(x["date"] >= date.today() for x in st.session_state.appointments)
    c1, c2, c3 = st.columns(3)
    for col, label, value, note in [
        (c1, "✅ Tasks left", open_tasks, "One step at a time"),
        (c2, "🛒 To buy", open_groceries, "Your shopping reminders"),
        (c3, "📅 Upcoming", upcoming, "Dates on the calendar"),
    ]:
        with col:
            st.markdown(f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div>{note}</div></div>", unsafe_allow_html=True)

    all_count = len(st.session_state.tasks) + len(st.session_state.groceries)
    done_count = sum(x["checked"] for x in st.session_state.tasks + st.session_state.groceries)
    st.markdown("### 🌈 Family progress")
    progress = done_count / all_count if all_count else 0
    st.progress(progress, text=f"{done_count} of {all_count} checklist items completed" if all_count else "Add your first item to start your family progress bar.")
    if all_count and progress == 1:
        st.success("Everything on your current lists is done. Tiny victory dance! 💃🕺")

    left, right = st.columns(2, gap="large")
    with left:
        st.markdown("### 🌿 Quick-add a task")
        with st.form("home_task_form", clear_on_submit=True):
            task = st.text_input("What needs doing?", placeholder="e.g. Pick up a prescription")
            priority = st.selectbox("Priority", ["Normal", "High", "Whenever"])
            due = st.date_input("Optional due date", value=None, key="home_task_due")
            submitted = st.form_submit_button("＋ Add task", use_container_width=True)
        if submitted and task.strip():
            st.session_state.tasks.append(new_item(task, priority, due))
            st.toast("Task added 🌱")
            st.rerun()
        with st.form("home_grocery_form", clear_on_submit=True):
            grocery = st.text_input("What are we running out of?", placeholder="e.g. Milk, bananas")
            submitted_grocery = st.form_submit_button("＋ Add grocery", use_container_width=True)
        if submitted_grocery and grocery.strip():
            st.session_state.groceries.append(new_item(grocery))
            st.rerun()
    with right:
        st.markdown("### 🥹 Little reminders")
        aged = sum(not x["checked"] and age_days(x) >= 3 for x in st.session_state.tasks + st.session_state.groceries)
        if aged:
            st.warning(f"{aged} item(s) have been waiting for 3 days or more. No guilt—just a gentle nudge to review them.")
        else:
            st.info("No lingering checklist items right now. You're doing fine. 💛")
        if st.session_state.recent_celebration:
            render_hug(st.session_state.recent_celebration)
            if st.button("Aww, thank you 💗", key="dismiss_hug"):
                st.session_state.recent_celebration = None
                st.rerun()

    st.markdown("### 📅 Coming up")
    upcoming_items = sorted([x for x in st.session_state.appointments if x["date"] >= date.today()], key=lambda x: x["date"])
    if upcoming_items:
        for event in upcoming_items[:5]:
            days = (event["date"] - date.today()).days
            timing = "Today 🎉" if days == 0 else "Tomorrow 🌷" if days == 1 else f"In {days} days"
            st.markdown(f"**{html.escape(event['name'])}** · {event['date'].strftime('%d %b %Y')}  \n<small>{timing}</small>", unsafe_allow_html=True)
    else:
        st.caption("No upcoming appointments yet.")

# ---------- To-do list ----------
elif page == "✅ To-do list":
    st.markdown("<div class='eyebrow'>THE FAMILY CHECKLIST</div>", unsafe_allow_html=True)
    st.title("One thing at a time. 🌱")
    st.write("Add a task, set a priority or due date, then check it off when it's done.")
    with st.form("task_form", clear_on_submit=True):
        task = st.text_input("New task", placeholder="e.g. Book the dentist")
        c1, c2 = st.columns(2)
        with c1:
            priority = st.selectbox("Priority", ["Normal", "High", "Whenever"])
        with c2:
            due = st.date_input("Due date (optional)", value=None, key="task_due")
        submitted = st.form_submit_button("＋ Add task", use_container_width=True)
    if submitted and task.strip():
        st.session_state.tasks.append(new_item(task, priority, due))
        st.toast("Task added 🌱")
        st.rerun()

    if st.session_state.tasks:
        filter_mode = st.radio("Show", ["All", "Open", "Completed"], horizontal=True, key="task_filter")
        visible = [x for x in st.session_state.tasks if filter_mode == "All" or (filter_mode == "Open" and not x["checked"]) or (filter_mode == "Completed" and x["checked"])]
        show_item_list(visible, "task", "todo")
        if st.button("Clear completed tasks"):
            st.session_state.tasks = [x for x in st.session_state.tasks if not x["checked"]]
            st.rerun()
    else:
        st.success("Nothing on the list yet. Enjoy the breathing room!")

# ---------- Groceries ----------
elif page == "🛒 Groceries":
    st.markdown("<div class='eyebrow'>THE SHOPPING LIST</div>", unsafe_allow_html=True)
    st.title("A little list, a smoother shop. 🥑")
    st.write("Tick an item when you've bought it and the couple will celebrate with a hug. 💗")
    with st.form("grocery_form", clear_on_submit=True):
        grocery = st.text_input("Grocery item", placeholder="e.g. Oats")
        submitted = st.form_submit_button("＋ Add item", use_container_width=True)
    if submitted and grocery.strip():
        st.session_state.groceries.append(new_item(grocery))
        st.rerun()

    if st.session_state.recent_celebration:
        render_hug(st.session_state.recent_celebration)
        if st.button("Dismiss celebration 💞", key="dismiss_grocery_hug"):
            st.session_state.recent_celebration = None
            st.rerun()

    if st.session_state.groceries:
        bought = sum(x["checked"] for x in st.session_state.groceries)
        st.progress(bought / len(st.session_state.groceries), text=f"{bought} of {len(st.session_state.groceries)} items bought")
        show_item_list(st.session_state.groceries, "grocery", "grocery")
        if st.button("Clear bought items"):
            st.session_state.groceries = [x for x in st.session_state.groceries if not x["checked"]]
            st.rerun()
    else:
        st.info("Your list is empty. Add your first item above.")

# ---------- Appointments ----------
elif page == "📅 Appointments":
    st.markdown("<div class='eyebrow'>FAMILY CALENDAR</div>", unsafe_allow_html=True)
    st.title("The important dates. 🌷")
    st.write("Keep appointments and family plans in one place.")
    with st.form("appointment_form", clear_on_submit=True):
        name = st.text_input("Appointment or event", placeholder="e.g. Dentist appointment")
        appointment_date = st.date_input("Date", value=date.today(), key="appointment_date")
        submitted = st.form_submit_button("＋ Save appointment", use_container_width=True)
    if submitted and name.strip():
        st.session_state.appointments.append({"id": str(uuid4()), "name": name.strip(), "date": appointment_date})
        st.rerun()

    if st.session_state.appointments:
        for item in sorted(st.session_state.appointments, key=lambda x: x["date"]):
            days = (item["date"] - date.today()).days
            if days < 0:
                status = f"Was {abs(days)} day(s) ago"
            elif days == 0:
                status = "Today 🎉"
            elif days == 1:
                status = "Tomorrow 🌷"
            else:
                status = f"In {days} days"
            col1, col2 = st.columns([0.78, 0.22])
            with col1:
                st.markdown(f"**{html.escape(item['name'])}**")
                st.caption(f"{item['date'].strftime('%A, %d %B %Y')} · {status}")
            with col2:
                if st.button("Remove", key=f"remove_event_{item['id']}"):
                    st.session_state.appointments = [x for x in st.session_state.appointments if x["id"] != item["id"]]
                    st.rerun()
            st.divider()
    else:
        st.info("No appointments yet. Add one above to get started.")

# ---------- Notes ----------
elif page == "💌 Family Notes & Messages":
    st.markdown("<div class='eyebrow'>YOUR LITTLE FAMILY NOTICEBOARD</div>", unsafe_allow_html=True)
    st.title("Notes from the heart. 💌")
    st.write("Leave a kind note, a reminder, or a little thank-you for the family.")
    with st.form("note_form", clear_on_submit=True):
        author = st.text_input("From", placeholder="e.g. Mum, Dad, Suchi…")
        note = st.text_area("Your message", placeholder="Remember to take a break today 💛")
        submitted = st.form_submit_button("＋ Pin a note", use_container_width=True)
    if submitted and note.strip():
        st.session_state.family_notes.insert(0, {
            "id": str(uuid4()), "author": author.strip() or "Someone in the family",
            "note": note.strip(), "created_at": datetime.now(),
        })
        st.rerun()
    if st.session_state.family_notes:
        for item in st.session_state.family_notes:
            st.markdown(f"""
            <div class="metric-card" style="margin:10px 0;min-height:auto">
              <div style="font-weight:700">💌 {html.escape(item['author'])}</div>
              <div style="margin:10px 0">{html.escape(item['note']).replace(chr(10), '<br>')}</div>
              <div style="font-size:.8rem;opacity:.7">{item['created_at'].strftime('%d %b %Y · %H:%M')}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Remove note", key=f"remove_note_{item['id']}"):
                st.session_state.family_notes = [x for x in st.session_state.family_notes if x["id"] != item["id"]]
                st.rerun()
    else:
        st.info("The noticeboard is blank. Add a little kindness to it. 🌷")

# ---------- Footer ----------
st.divider()
st.markdown(
    "<p style='text-align:center;opacity:.65;font-size:.82rem'>"
    "Made with care · Our Family Hub 🏡 · Small steps count.</p>",
    unsafe_allow_html=True,
)

from __future__ import annotations
import json, os, sqlite3, uuid, csv, io, html
from pathlib import Path
from datetime import date, datetime, time, timedelta
import streamlit as st

st.set_page_config(page_title="Our Family Hub", page_icon="🏡", layout="wide", initial_sidebar_state="expanded")

DATA_DIR = Path(os.environ.get("FAMILY_HUB_DATA_DIR", ".")).resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "family_hub.sqlite3"
COLLECTIONS = ["tasks", "routines", "groceries", "events", "notes", "memories", "transactions", "activity", "pantry"]
DARK = {"bg":"#111318","sidebar":"#171a21","card":"#1c2029","card2":"#242b37","text":"#f4f6fa","muted":"#b6bfce","border":"#343c4a","accent":"#a9c8f0","accent_bg":"#29384c","input":"#171b23","good":"#8ed7b1","warn":"#f0ca86"}

def stamp(): return datetime.now().isoformat(timespec="seconds")
def new_id(): return uuid.uuid4().hex
def connect():
    c=sqlite3.connect(DB_PATH, timeout=20, check_same_thread=False)
    c.row_factory=sqlite3.Row
    c.execute("PRAGMA journal_mode=WAL")
    return c
def init_db():
    with connect() as c:
        c.execute("CREATE TABLE IF NOT EXISTS data (name TEXT PRIMARY KEY, payload TEXT NOT NULL, updated TEXT NOT NULL)")
        c.execute("CREATE TABLE IF NOT EXISTS settings (name TEXT PRIMARY KEY, value TEXT NOT NULL)")
        for n in COLLECTIONS: c.execute("INSERT OR IGNORE INTO data VALUES (?,?,?)",(n,"[]",stamp()))
        c.execute("INSERT OR IGNORE INTO settings VALUES ('mood','Happy')")
def get(n):
    with connect() as c: row=c.execute("SELECT payload FROM data WHERE name=?",(n,)).fetchone()
    try:
        v=json.loads(row["payload"]) if row else []
        return v if isinstance(v,list) else []
    except (ValueError,TypeError): return []
def put(n, items):
    with connect() as c: c.execute("INSERT INTO data VALUES (?,?,?) ON CONFLICT(name) DO UPDATE SET payload=excluded.payload,updated=excluded.updated",(n,json.dumps(items,ensure_ascii=False,default=str),stamp()))
def add(n,item):
    item.setdefault("id",new_id()); item.setdefault("created_at",stamp()); items=get(n); items.append(item); put(n,items)
def edit(n, ident, **changes):
    items=get(n)
    for x in items:
        if x.get("id")==ident: x.update(changes); x["updated_at"]=stamp()
    put(n,items)
def remove(n, ident): put(n,[x for x in get(n) if x.get("id")!=ident])
def setting(k,default=""):
    with connect() as c: row=c.execute("SELECT value FROM settings WHERE name=?",(k,)).fetchone()
    return row["value"] if row else default
def set_setting(k,v):
    with connect() as c: c.execute("INSERT INTO settings VALUES (?,?) ON CONFLICT(name) DO UPDATE SET value=excluded.value",(k,str(v)))
def as_date(v):
    try: return date.fromisoformat(str(v)[:10])
    except (ValueError,TypeError): return date.today()
def fmt_date(v): return as_date(v).strftime("%a, %d %b %Y")
def safe(v): return html.escape(str(v if v is not None else ""))
def section(title,sub=""):
    st.markdown(f'<div class="section-title">{safe(title)}</div>',unsafe_allow_html=True)
    if sub: st.markdown(f'<div class="section-subtitle">{safe(sub)}</div>',unsafe_allow_html=True)
def metric(label,value,detail,icon):
    st.markdown(f'<div class="metric"><div class="metric-head">{safe(label)} <span>{safe(icon)}</span></div><div class="metric-value">{safe(value)}</div><div class="muted">{safe(detail)}</div></div>',unsafe_allow_html=True)
def go(page):
    # Update app navigation state, not a widget-owned session-state key.
    # This avoids Streamlit's StreamlitWidgetAlreadyInstantiatedError.
    st.session_state["current_page"] = page
    st.rerun()

def sync_navigation():
    # Called by the sidebar radio when the user changes pages.
    st.session_state["current_page"] = st.session_state["navigation_radio"]
def activity(action,item):
    add("activity",{"action":action,"item":item,"when":stamp()})

def is_recent(item, hours=24):
    raw=item.get("created_at") or item.get("created") or item.get("updated_at") or ""
    try: return (datetime.now()-datetime.fromisoformat(str(raw))).total_seconds() <= hours*3600
    except (ValueError,TypeError): return False

def task_is_overdue(item):
    return bool(not item.get("done") and item.get("due") and as_date(item["due"]) < today)

init_db()
st.markdown(f"""
<style>
:root{{--bg:{DARK['bg']};--side:{DARK['sidebar']};--card:{DARK['card']};--card2:{DARK['card2']};--text:{DARK['text']};--muted:{DARK['muted']};--border:{DARK['border']};--accent:{DARK['accent']};--accentbg:{DARK['accent_bg']};--input:{DARK['input']};--good:{DARK['good']};--warn:{DARK['warn']};}}
/* Helvetica-first typography throughout; mobile-friendly sizing */
html,body,[class*="css"],button,input,textarea,select{{font-family:Helvetica,Arial,sans-serif!important}}
.stApp{{background:var(--bg);color:var(--text);font-size:17px}}
[data-testid="stHeader"]{{background:transparent}}
[data-testid="stMainBlockContainer"]{{max-width:1500px;padding:1.2rem 1.25rem 3rem}}
section[data-testid="stSidebar"]{{background:var(--side);border-right:1px solid var(--border)}}
section[data-testid="stSidebar"]>div{{padding:1.3rem .85rem}}
.stApp p,.stApp label,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp h4,.stApp [data-testid="stMarkdownContainer"],section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] label{{color:var(--text)}}
h1,h2,h3,.brand,.hero-title,.section-title{{font-family:Helvetica,Arial,sans-serif!important;letter-spacing:-.02em;font-weight:700}}
.stApp p,.stApp li,.stApp label,.stApp [data-testid="stMarkdownContainer"]{{font-size:1rem;line-height:1.6}}
.brand{{font-size:1.55rem;font-weight:750}} .muted,.stApp [data-testid="stCaptionContainer"] p{{color:var(--muted)!important;font-size:.95rem}}
.hero{{background:linear-gradient(135deg,var(--card),#202a39);border:1px solid var(--border);border-radius:24px;padding:clamp(22px,4vw,38px);margin-bottom:1.2rem;animation:rise-in .45s ease-out both}}
.hero-kicker{{color:var(--accent);text-transform:uppercase;letter-spacing:.1em;font-size:.82rem;font-weight:700;margin-bottom:.8rem}}
.hero-title{{font-size:clamp(2rem,4vw,3.1rem);line-height:1.15;color:var(--text)}} .hero-copy{{color:var(--muted);font-size:1.08rem;line-height:1.7;max-width:720px;margin-top:.7rem}}
.section-title{{font-size:1.65rem;margin:1.2rem 0 .2rem;color:var(--text)}} .section-subtitle{{color:var(--muted);font-size:1rem;margin-bottom:1rem;line-height:1.6}}
.metric{{background:var(--card);border:1px solid var(--border);border-radius:17px;padding:17px;min-height:125px;margin-bottom:.65rem;animation:rise-in .45s ease-out both}}
.metric-head{{display:flex;justify-content:space-between;gap:8px;color:var(--muted);font-weight:600;font-size:.98rem}} .metric-head span{{background:var(--accentbg);padding:5px 9px;border-radius:9px;color:var(--accent)}}
.metric-value{{font-size:2rem;font-weight:750;margin-top:8px;overflow-wrap:anywhere}}
[data-testid="stVerticalBlockBorderWrapper"]{{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:16px!important;animation:rise-in .32s ease-out both}}
.stApp input,.stApp textarea,.stApp [data-baseweb="input"] input,.stApp [data-baseweb="textarea"] textarea{{background:var(--input)!important;color:var(--text)!important;-webkit-text-fill-color:var(--text)!important;caret-color:var(--text)!important;border-color:var(--border)!important;opacity:1!important;font-size:16px!important;min-height:44px}}
.stApp input::placeholder,.stApp textarea::placeholder{{color:var(--muted)!important;-webkit-text-fill-color:var(--muted)!important;opacity:1!important}}
.stApp [data-baseweb="select"]>div,.stApp [data-baseweb="select"] *{{background-color:var(--input);color:var(--text)!important;border-color:var(--border)!important;font-size:16px!important}}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"]{{background:var(--card)!important;color:var(--text)!important}}
.stApp .stButton>button,.stApp .stDownloadButton>button{{background:var(--card2)!important;color:var(--text)!important;border:1px solid var(--border)!important;border-radius:12px!important;min-height:48px;padding:.55rem .85rem;font-size:1rem!important;font-weight:650;white-space:normal;transition:transform .16s ease,border-color .16s ease,background .16s ease}}
.stApp .stButton>button:hover,.stApp .stDownloadButton>button:hover{{border-color:var(--accent)!important;color:var(--accent)!important;transform:translateY(-1px)}}
.stApp [data-testid="stFormSubmitButton"] button,.stApp button[kind="primary"]{{background:var(--accent)!important;color:#111722!important;border:1px solid var(--accent)!important;border-radius:12px!important;min-height:50px;font-size:1rem!important;font-weight:750}}
.stApp [data-testid="stFormSubmitButton"] button *,.stApp button[kind="primary"] *{{color:#111722!important;-webkit-text-fill-color:#111722!important}}
.stApp hr{{border-color:var(--border)}} a{{color:var(--accent)!important}}
/* Small visual feedback for updates, reminders, and completed work */
@keyframes rise-in{{from{{opacity:0;transform:translateY(7px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes gentle-pulse{{0%,100%{{box-shadow:0 0 0 0 rgba(240,202,134,0)}}50%{{box-shadow:0 0 0 4px rgba(240,202,134,.12)}}}}
@keyframes done-pop{{0%{{transform:scale(.97)}}60%{{transform:scale(1.015)}}100%{{transform:scale(1)}}}}
.status-pill{{display:inline-block;border-radius:999px;padding:3px 9px;font-size:.82rem;font-weight:750;margin:2px 4px 2px 0;letter-spacing:.01em}}
.status-new{{background:#263e32;color:#a8f0c8;border:1px solid #426c55;animation:done-pop .55s ease-out both}}
.status-overdue{{background:#493322;color:#ffdb9c;border:1px solid #89633b;animation:gentle-pulse 2.2s ease-in-out infinite}}
.status-done{{background:#263e32;color:#a8f0c8;border:1px solid #426c55;animation:done-pop .35s ease-out both}}
.stAlert{{border-radius:13px;animation:rise-in .3s ease-out both}}
@media(max-width:760px){{
 [data-testid="stMainBlockContainer"]{{padding:.65rem .65rem 1.6rem}}
 .hero{{border-radius:17px;padding:19px 17px;margin-bottom:.9rem}}
 .hero-title{{font-size:clamp(1.8rem,8vw,2.35rem)}} .hero-copy{{font-size:1rem;line-height:1.65}}
 .hero-kicker{{font-size:.78rem}} .section-title{{font-size:1.45rem}}
 .metric{{padding:12px;min-height:104px;border-radius:14px}}
 .metric-head{{font-size:.9rem}} .metric-value{{font-size:1.55rem}}
 .stApp p,.stApp li,.stApp label,.stApp [data-testid="stMarkdownContainer"]{{font-size:16px;line-height:1.55}}
 .stApp [data-testid="stCaptionContainer"] p{{font-size:14px!important;line-height:1.45}}
 .stApp .stButton>button,.stApp .stDownloadButton>button{{min-height:50px;font-size:16px!important;padding:.65rem .75rem}}
 .stApp input,.stApp textarea,.stApp [data-baseweb="input"] input,.stApp [data-baseweb="textarea"] textarea{{font-size:16px!important}}
 /* Stack content columns on phones so labels and controls stay readable. */
 [data-testid="stHorizontalBlock"]{{flex-wrap:wrap!important;gap:.6rem!important}}
 [data-testid="stHorizontalBlock"]>[data-testid="column"]{{flex:1 1 100%!important;min-width:100%!important;width:100%!important}}
 section[data-testid="stSidebar"]>div{{padding:.9rem .75rem}}
}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}}}
</style>""",unsafe_allow_html=True)

today=date.today(); now=datetime.now()
pages=["Home","Tasks & Routines","Groceries","What's in My Fridge?","Calendar & Reminders","Family Notes","Memories","Household Budget","Activity & Greetings","Backups & Settings"]
labels={"Home":"🏡 Home","Tasks & Routines":"✓ Tasks & routines","Groceries":"🛒 Groceries","What's in My Fridge?":"🍳 What's in my fridge?","Calendar & Reminders":"▦ Calendar & reminders","Family Notes":"♡ Family notes","Memories":"✦ Memories timeline","Household Budget":"€ Household budget","Activity & Greetings":"☀ Greetings & activity","Backups & Settings":"⚙ Backups & settings"}

# Initialise app-level navigation separately from the radio widget's state.
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"
# Sync the radio's value BEFORE the widget is instantiated. Never assign to
# navigation_radio later in the same run.
st.session_state["navigation_radio"] = st.session_state["current_page"]

with st.sidebar:
    st.markdown('<div class="brand">Our Family Hub</div>',unsafe_allow_html=True)
    st.caption("A calmer way to organise life, together.")
    st.caption("🌙 Dark theme · Always on")
    st.radio(
        "Navigate",
        pages,
        key="navigation_radio",
        on_change=sync_navigation,
        format_func=lambda p: labels[p],
        label_visibility="collapsed",
    )
    st.divider(); st.caption("MADE FOR TWO"); st.markdown("**Suchi & Abi** 💙")
    st.caption("Small steps, big love.")

page = st.session_state["current_page"]
tasks=get("tasks"); groceries=get("groceries"); events=get("events"); notes=get("notes"); memories=get("memories"); tx=get("transactions")
st.markdown(f'<div class="hero"><div class="hero-kicker">YOUR HOME · YOUR LITTLE WORLD</div><div class="hero-title">A little more organised.<br>A little more together.</div><div class="hero-copy">Welcome back, Suchi &amp; Abi. Keep track of everyday things, make space for the good moments, and take life one step at a time.</div><div class="muted">{today.strftime("%A, %d %B %Y")} · Made with love ♡</div></div>',unsafe_allow_html=True)

if page=="Home":
    pending=sum(not x.get("done") for x in tasks); left=sum(not x.get("bought") for x in groceries)
    upcoming=sum(as_date(x["date"])>=today for x in events if x.get("date"))
    month= today.strftime("%Y-%m")
    spent=sum(float(x.get("amount",0) or 0) for x in tx if x.get("kind")=="Expense" and str(x.get("date",""))[:7]==month)
    cols=st.columns(4)
    for c,args in zip(cols,[("Open tasks",pending,"Little steps to take","✓"),("Shopping list",left,"Items still to pick up","🛒"),("Coming up",upcoming,"Upcoming events","▦"),("Monthly spend",f"€{spent:,.2f}","Recorded expenses","€")]):
        with c: metric(*args)
    greet="Good morning" if now.hour<12 else ("Good afternoon" if now.hour<18 else "Good evening")
    st.markdown(f"### {greet}, Suchi & Abi 💙")
    mood_options=["Happy","Relaxed","Grateful","Busy","Tired","Need a little love"]
    mood=setting("mood","Happy")
    st.write({"Happy":"Enjoy the lovely moments. ☀️","Relaxed":"Keep that peaceful feeling close. 🌿","Grateful":"Notice the little things that make life sweet. 💗","Busy":"One thing at a time. You have got this. 🌸","Tired":"Rest counts, too. Be kind to yourselves. ☁️","Need a little love":"A kind word or a hug can go a long way. ♡"}.get(mood,"One step at a time. 💙"))
    selected=st.selectbox("Today's shared mood",mood_options,index=mood_options.index(mood) if mood in mood_options else 0)
    if selected!=mood: set_setting("mood",selected); st.rerun()
    due=[x for x in tasks if not x.get("done") and x.get("due") and as_date(x["due"])<=today]
    today_events=[x for x in events if x.get("date") and as_date(x["date"])==today]
    if due or today_events: st.warning(f"Reminder: {len(due)} task(s) due/overdue · {len(today_events)} event(s) today")
    else: st.success("You're all caught up on today's reminders. Make a little room to breathe.")
    with st.container(border=True):
        st.markdown("### 🍳 What's in your fridge?")
        st.write("Turn the ingredients you already have into easy meal ideas, then send anything missing to your shared grocery list.")
        if st.button("Find something to cook →", key="home_fridge_finder", use_container_width=True): go("What's in My Fridge?")
    section("Quick actions","Add something in just a tap.")
    q=st.columns(4)
    for c,label,target in zip(q,["＋ Add task","🛒 Add groceries","📅 Add event","♡ Write a note"],["Tasks & Routines","Groceries","Calendar & Reminders","Family Notes"]):
        with c:
            if st.button(label,key="quick_"+target,use_container_width=True): st.session_state["quick_open"]=target; go(target)
    section("Your day, at a glance","Your home hub, all in one place.")
    leftc,rightc=st.columns([1.15,.85],gap="large")
    with leftc:
        with st.container(border=True):
            st.markdown("### ♡ A gentle reminder"); st.write("You don't need to do everything today. Choose what matters, help each other where you can, and leave a little room to rest.")
        st.markdown("#### Tasks to tackle")
        opened=sorted([x for x in tasks if not x.get("done")],key=lambda x:(x.get("due") or "9999",x.get("priority")!="High"))
        if opened:
            for x in opened[:5]:
                with st.container(border=True):
                    st.markdown(f"**{safe(x.get('name','Task'))}**"); st.caption(f"{safe(x.get('assigned','Both'))} · {safe(x.get('priority','Normal'))} priority"+(f" · Due {fmt_date(x['due'])}" if x.get("due") else ""))
        else: st.success("All caught up! Time for a little breathing room.")
        if st.button("Open task list →",use_container_width=True): go("Tasks & Routines")
    with rightc:
        future=sorted([x for x in events if x.get("date") and as_date(x["date"])>=today],key=lambda x:(x.get("date",""),x.get("time","")))
        with st.container(border=True):
            st.markdown("### 📅 Next appointment")
            if future: st.write(f"{future[0].get('title','Event')} · {fmt_date(future[0]['date'])} · {future[0].get('time','')}")
            else: st.write("Nothing scheduled just yet.")
        with st.container(border=True):
            st.markdown("### ✦ Our little moments"); st.write(f"{len(memories)} memories saved so far. Keep the good things close.")
            if st.button("Add a memory →",use_container_width=True): go("Memories")
    st.markdown("---"); section("Little things to remember","Your home hub, all in one place.")
    c1,c2,c3=st.columns(3,gap="large")
    for c,icon,title,desc,target in [(c1,"✓","Tasks","Share responsibilities and celebrate each finished task.","Tasks & Routines"),(c2,"🛒","Groceries","Keep your shopping list simple and up to date.","Groceries"),(c3,"♡","Family notes","Save messages, reminders, and little memories.","Family Notes")]:
        with c:
            with st.container(border=True):
                st.markdown(f"### {icon}  {title}"); st.write(desc)
                if st.button(f"Open {title.lower()} →",key="home_"+target,use_container_width=True): go(target)

elif page=="Tasks & Routines":
    section("Our tasks & routines","Share the load, and let recurring chores return automatically.")
    with st.expander("＋ Add a task",expanded=bool(st.session_state.get("quick_open")==page or not tasks)):
        with st.form("task_form",clear_on_submit=True):
            name=st.text_input("What needs doing?",placeholder="Tidy the living room")
            a,b=st.columns(2)
            with a: assigned=st.selectbox("Who's taking it?",["Both","Suchi","Abi"])
            with b: priority=st.selectbox("Priority",["Normal","High","Low"])
            due_on=st.checkbox("Add due date"); due=st.date_input("Due date",value=today) if due_on else None
            repeat=st.selectbox("Repeat",["Does not repeat","Daily","Weekly","Monthly"])
            if st.form_submit_button("Add task",use_container_width=True):
                if name.strip(): add("tasks",{"name":name.strip(),"assigned":assigned,"priority":priority,"due":due.isoformat() if due else None,"done":False,"repeat":repeat,"next_generated":None}); st.rerun()
                else: st.warning("Please enter a task name.")
    # Generate the next recurring instance after a completed task reaches its next cycle.
    for x in list(get("tasks")):
        repeat=x.get("repeat","Does not repeat")
        if x.get("done") and repeat!="Does not repeat" and x.get("due") and x.get("next_generated")!=today.isoformat():
            d=as_date(x["due"])
            due_next=d+timedelta(days=1 if repeat=="Daily" else 7) if repeat in ("Daily","Weekly") else date(d.year+((d.month)//12),((d.month)%12)+1,min(d.day,28))
            if due_next<=today:
                add("tasks",{"name":x["name"],"assigned":x.get("assigned","Both"),"priority":x.get("priority","Normal"),"due":due_next.isoformat(),"done":False,"repeat":repeat,"next_generated":None})
                edit("tasks",x["id"],next_generated=today.isoformat())
    tasks=get("tasks"); completed=sum(bool(x.get("done")) for x in tasks)
    st.progress(completed/len(tasks) if tasks else 0,text=f"{completed} of {len(tasks)} tasks completed")
    filt=st.segmented_control("Show tasks",["All","Open","Completed"],default="All")
    shown=[x for x in tasks if filt=="All" or (filt=="Open" and not x.get("done")) or (filt=="Completed" and x.get("done"))]
    for x in shown:
        with st.container(border=True):
            a,b,c=st.columns([.1,.68,.22])
            with a: checked=st.checkbox("Complete",value=bool(x.get("done")),key="done_"+x["id"],label_visibility="collapsed")
            if checked!=bool(x.get("done")):
                edit("tasks",x["id"],done=checked)
                if checked: activity("Completed task",x.get("name",""))
                st.rerun()
            with b:
                st.markdown(f"~~{safe(x.get('name','Task'))}~~" if x.get("done") else f"**{safe(x.get('name','Task'))}**")
                badges=[]
                if x.get("done"): badges.append('<span class="status-pill status-done">✓ Done</span>')
                elif task_is_overdue(x): badges.append('<span class="status-pill status-overdue">⚠ Overdue</span>')
                if is_recent(x): badges.append('<span class="status-pill status-new">✦ New</span>')
                if badges: st.markdown(" ".join(badges),unsafe_allow_html=True)
                st.caption(f"{x.get('assigned','Both')} · {x.get('priority','Normal')} priority"+(f" · Due {fmt_date(x['due'])}" if x.get("due") else "")+(f" · Repeats {x['repeat'].lower()}" if x.get("repeat") not in (None,"Does not repeat") else ""))
            with c:
                if st.button("Delete",key="del_task_"+x["id"],use_container_width=True): remove("tasks",x["id"]); st.rerun()
    section("Reusable routines","Save a recurring checklist or household rhythm.")
    with st.expander("＋ Create routine"):
        with st.form("routine_form",clear_on_submit=True):
            rn=st.text_input("Routine name",placeholder="Sunday reset"); desc=st.text_input("What's included?",placeholder="Laundry, tidy kitchen, plan the week")
            freq=st.selectbox("Frequency",["Daily","Weekly","Monthly"]); who=st.selectbox("Responsible",["Both","Suchi","Abi"])
            if st.form_submit_button("Save routine"):
                if rn.strip(): add("routines",{"name":rn.strip(),"description":desc.strip(),"frequency":freq,"assigned":who,"last_done":None}); st.rerun()
                else: st.warning("Add a routine name.")
    for r in get("routines"):
        with st.container(border=True):
            a,b,c=st.columns([.62,.2,.18])
            with a:
                st.markdown(f"**{safe(r['name'])}**"); st.caption(f"{r.get('frequency','Weekly')} · {r.get('assigned','Both')}"+(f" · {safe(r.get('description',''))}" if r.get("description") else ""))
                if r.get("last_done"): st.caption("Last completed: "+fmt_date(r["last_done"]))
            with b:
                if st.button("Done today",key="routine_done_"+r["id"],use_container_width=True): edit("routines",r["id"],last_done=today.isoformat()); activity("Completed routine",r["name"]); st.rerun()
            with c:
                if st.button("Delete",key="routine_del_"+r["id"],use_container_width=True): remove("routines",r["id"]); st.rerun()

elif page=="Groceries":
    section("Grocery list","A shared, categorised list that stays up to date.")
    with st.expander("＋ Add grocery item",expanded=bool(st.session_state.get("quick_open")==page or not groceries)):
        with st.form("grocery_form",clear_on_submit=True):
            a,b=st.columns([.62,.38])
            with a: name=st.text_input("Item",placeholder="Fresh strawberries")
            with b: qty=st.text_input("Quantity",placeholder="2 packs")
            category=st.selectbox("Category",["Produce","Bakery","Dairy & eggs","Meat & fish","Pantry","Frozen","Household","Other"])
            if st.form_submit_button("Add to list",use_container_width=True):
                if name.strip():
                    if not any(g.get("name","").casefold()==name.strip().casefold() and not g.get("bought") for g in get("groceries")): add("groceries",{"name":name.strip(),"quantity":qty.strip() or "As needed","category":category,"bought":False}); activity("Added grocery",name.strip())
                    else: st.info("That item is already on your open list.")
                    st.rerun()
                else: st.warning("Please enter an item.")
    groceries=get("groceries"); bought=[g for g in groceries if g.get("bought")]
    st.caption(f"{len(groceries)-len(bought)} items left · {len(bought)} picked up")
    filt=st.selectbox("Show",["All items","Still to buy","Purchased"])
    shown=[g for g in groceries if filt=="All items" or (filt=="Still to buy" and not g.get("bought")) or (filt=="Purchased" and g.get("bought"))]
    shown.sort(key=lambda g:(g.get("bought",False),g.get("category",""),g.get("name","").lower()))
    if not shown: st.info("Your list is clear. Add groceries whenever you need them.")
    for g in shown:
        with st.container(border=True):
            a,b,c=st.columns([.1,.67,.23])
            with a: checked=st.checkbox("Bought",value=bool(g.get("bought")),key="bought_"+g["id"],label_visibility="collapsed")
            if checked!=bool(g.get("bought")):
                edit("groceries",g["id"],bought=checked)
                if checked: activity("Bought grocery",g["name"])
                st.rerun()
            with b:
                st.markdown(f"~~{safe(g['name'])}~~" if g.get("bought") else f"**{safe(g['name'])}**")
                if g.get("bought"): st.markdown('<span class="status-pill status-done">✓ Picked up</span>',unsafe_allow_html=True)
                elif is_recent(g): st.markdown('<span class="status-pill status-new">✦ New</span>',unsafe_allow_html=True)
                st.caption(f"{safe(g.get('category','Other'))} · Quantity: {safe(g.get('quantity','As needed'))}")
            with c:
                if st.button("Remove",key="remove_g_"+g["id"],use_container_width=True): activity("Removed grocery",g["name"]); remove("groceries",g["id"]); st.rerun()
    a,b=st.columns(2)
    with a:
        if st.button("Add previous items back",use_container_width=True):
            for g in bought: add("groceries",{"name":g["name"],"quantity":g.get("quantity","As needed"),"category":g.get("category","Other"),"bought":False})
            st.rerun()
    with b:
        if st.button("Clear purchased items",use_container_width=True):
            for g in bought: remove("groceries",g["id"])
            st.rerun()

elif page=="What's in My Fridge?":
    section("What's in My Fridge?", "Tell us what you have, and discover meals you can make without another shopping trip.")
    st.markdown("### 🥕 What's in your fridge, freezer, or cupboards?")
    saved_pantry=get("pantry")
    saved_names=[x.get("name","").strip() for x in saved_pantry if x.get("name","").strip()]
    if saved_names:
        st.caption("Saved pantry items: " + " · ".join(saved_names))
    with st.form("fridge_recipe_form"):
        ingredients_text=st.text_area("List your ingredients", placeholder="eggs, spinach, tomatoes, cheese, leftover rice", height=110, help="Separate ingredients with commas or put each on a new line.")
        a,b=st.columns(2)
        with a: max_time=st.selectbox("Cooking time", ["Any time", "15 minutes or less", "30 minutes or less", "45 minutes or less"])
        with b: diet=st.selectbox("Preference", ["Anything", "Vegetarian", "Vegan"])
        include_pantry=st.checkbox("Include my saved pantry items", value=True)
        find_recipes=st.form_submit_button("✨ Find recipes", use_container_width=True)
    # A built-in recipe collection works without an API key. Matching is based on
    # ingredients and clearly identifies missing items rather than claiming AI certainty.
    recipe_book=[
      {"name":"Spinach & cheese omelette","time":15,"diet":"Vegetarian","ingredients":["eggs","spinach","cheese","milk","butter"],"steps":["Whisk eggs with a splash of milk, salt and pepper.","Wilt spinach in a lightly buttered pan.","Pour in eggs, cook gently, add cheese, fold and serve."],"tip":"Use any leafy greens in place of spinach."},
      {"name":"Tomato & cheese toasties","time":15,"diet":"Vegetarian","ingredients":["bread","tomatoes","cheese","butter"],"steps":["Slice tomatoes and grate or slice the cheese.","Layer on bread and butter the outside lightly.","Toast in a pan or sandwich press until golden and melted."],"tip":"Add spinach or herbs if you have them."},
      {"name":"Creamy tomato spinach pasta","time":25,"diet":"Vegetarian","ingredients":["pasta","tomatoes","spinach","garlic","cream","cheese","olive oil"],"steps":["Cook pasta according to its packet.","Sauté garlic and tomatoes in olive oil; stir in spinach and cream.","Toss with pasta and finish with cheese."],"tip":"Milk plus a little extra cheese can stand in for cream."},
      {"name":"Vegetable fried rice","time":20,"diet":"Vegan","ingredients":["cooked rice","eggs","carrots","peas","spring onions","soy sauce","oil"],"steps":["Use cold cooked rice if possible; break up any clumps.","Stir-fry chopped vegetables in a little oil.","Add rice and soy sauce; stir-fry until hot. Add scrambled egg if using."],"tip":"For vegan fried rice, leave out the egg."},
      {"name":"Chickpea tomato curry","time":30,"diet":"Vegan","ingredients":["chickpeas","canned tomatoes","onion","garlic","curry powder","oil","rice"],"steps":["Cook chopped onion and garlic in oil until soft.","Stir in curry powder, chickpeas and canned tomatoes.","Simmer for 15–20 minutes and serve with rice."],"tip":"Use any beans instead of chickpeas."},
      {"name":"Cheesy baked potatoes","time":45,"diet":"Vegetarian","ingredients":["potatoes","cheese","butter","yogurt","spring onions"],"steps":["Prick potatoes and bake at 200°C until tender.","Split open and fluff the insides with butter.","Top with cheese and return to the oven until melted; add yogurt or spring onions."],"tip":"Microwave the potatoes first to reduce oven time."},
      {"name":"Banana oat pancakes","time":20,"diet":"Vegetarian","ingredients":["banana","eggs","oats","milk","oil"],"steps":["Mash banana and mix with eggs, oats and a splash of milk.","Rest the batter for five minutes.","Cook small pancakes in a lightly oiled pan until golden on both sides."],"tip":"Add cinnamon if available."},
      {"name":"Garlic butter mushrooms on toast","time":15,"diet":"Vegetarian","ingredients":["mushrooms","garlic","butter","bread","parsley"],"steps":["Slice mushrooms and mince garlic.","Sauté mushrooms in butter until browned; add garlic near the end.","Season and spoon over toasted bread; finish with parsley if available."],"tip":"A splash of soy sauce adds savoury flavour."},
      {"name":"Simple lentil soup","time":35,"diet":"Vegan","ingredients":["lentils","carrots","onion","garlic","vegetable stock","canned tomatoes"],"steps":["Soften chopped onion, carrot and garlic in a pot.","Add lentils, stock and tomatoes.","Simmer until lentils are tender, adding water if needed."],"tip":"Use any suitable stock or water with seasoning."},
      {"name":"Tomato egg rice bowl","time":15,"diet":"Vegetarian","ingredients":["eggs","tomatoes","cooked rice","oil","spring onions"],"steps":["Scramble eggs gently in a pan and set aside.","Cook chopped tomatoes until juicy and soft.","Return eggs to the pan and serve over hot rice."],"tip":"Season with soy sauce, salt or pepper to taste."},
    ]
    def norm_ingredient(value):
        value=value.lower().strip()
        for prefix in ("some ","fresh ","frozen ","leftover ","a little ","a few "):
            if value.startswith(prefix): value=value[len(prefix):]
        aliases={"tomato":"tomatoes","potato":"potatoes","egg":"eggs","mushroom":"mushrooms","chickpea":"chickpeas","green onion":"spring onions","scallions":"spring onions","rice":"cooked rice","oat":"oats","lentil":"lentils"}
        return aliases.get(value,value)
    if find_recipes:
        supplied=[norm_ingredient(v) for v in ingredients_text.replace("\n",",").split(",") if v.strip()]
        if include_pantry: supplied += [norm_ingredient(v) for v in saved_names]
        # Treat already listed grocery items as available too.
        supplied += [norm_ingredient(x.get("name","")) for x in get("groceries") if not x.get("bought")]
        available=set(supplied)
        st.session_state["fridge_available"] = sorted(available)
        matches=[]
        max_minutes={"Any time":999,"15 minutes or less":15,"30 minutes or less":30,"45 minutes or less":45}[max_time]
        for recipe in recipe_book:
            if recipe["time"]>max_minutes or (diet!="Anything" and recipe["diet"] not in (diet,"Vegan" if diet=="Vegetarian" else diet)): continue
            have=[i for i in recipe["ingredients"] if norm_ingredient(i) in available or (i=="cooked rice" and "rice" in available) or (i=="canned tomatoes" and "tomatoes" in available)]
            missing=[i for i in recipe["ingredients"] if i not in have]
            if have:
                matches.append((len(have)/len(recipe["ingredients"]),len(missing),recipe,have,missing))
        st.session_state["fridge_recipe_results"]=[{"score":x[0],"missing":x[4],"recipe":x[2],"have":x[3]} for x in sorted(matches,key=lambda x:(x[1],-x[0],x[2]["time"]))[:8]]
        if not supplied: st.session_state["fridge_recipe_results"]=[]
    results=st.session_state.get("fridge_recipe_results",[])
    if find_recipes and not ingredients_text.strip() and not (include_pantry and saved_names):
        st.info("Enter a few ingredients first so I can find matching recipes.")
    elif results:
        st.markdown("### 🍽️ Recipes you could make")
        st.caption("Matches use a built-in recipe collection. Check ingredient labels and quantities before cooking.")
        for idx,item in enumerate(results):
            r=item["recipe"]; missing=item["missing"]
            with st.container(border=True):
                a,b=st.columns([.76,.24])
                with a:
                    st.markdown(f"### {r['name']}")
                    st.caption(f"⏱️ {r['time']} min · {r['diet']} · {len(item['have'])}/{len(r['ingredients'])} ingredients matched")
                    st.progress(item["score"])
                with b:
                    st.metric("Need to buy",len(missing))
                st.markdown("**You have:** " + (", ".join(item["have"]) if item["have"] else "No listed ingredients matched"))
                st.markdown("**Missing:** " + (", ".join(missing) if missing else "Nothing from this recipe list — lovely!") )
                with st.expander("View ingredients & cooking steps"):
                    st.markdown("**Ingredients**")
                    st.write(", ".join(r["ingredients"]))
                    st.markdown("**How to make it**")
                    for n,step in enumerate(r["steps"],1): st.write(f"{n}. {step}")
                    st.caption("Tip: "+r["tip"])
                if missing:
                    if st.button("🛒 Add missing ingredients to Groceries",key=f"recipe_missing_{idx}",use_container_width=True):
                        existing={g.get("name","").casefold() for g in get("groceries") if not g.get("bought")}
                        added=[]
                        for ingredient in missing:
                            if ingredient.casefold() not in existing:
                                add("groceries",{"name":ingredient.title(),"quantity":"For recipe: "+r["name"],"category":"Produce" if ingredient in ["tomatoes","spinach","carrots","onion","garlic","mushrooms"] else ("Dairy & eggs" if ingredient in ["eggs","cheese","milk","cream","butter","yogurt"] else "Pantry"),"bought":False}); added.append(ingredient)
                        activity("Added recipe ingredients",r["name"])
                        st.success("Added: "+(", ".join(added) if added else "All missing items were already on your list."))
                        st.rerun()
    elif find_recipes:
        st.info("I couldn't find a close match yet. Try adding a few more ingredients, or choose a longer cooking time.")
    st.divider()
    section("Save pantry staples", "Keep ingredients you usually have at home, so recipe matching is faster next time.")
    with st.form("pantry_form",clear_on_submit=True):
        pantry_text=st.text_input("Add pantry items",placeholder="olive oil, pasta, rice, flour, salt")
        if st.form_submit_button("Save pantry items",use_container_width=True):
            existing={x.get("name","").casefold() for x in get("pantry")}
            added=0
            for value in pantry_text.split(","):
                name=value.strip()
                if name and name.casefold() not in existing:
                    add("pantry",{"name":name}); existing.add(name.casefold()); added+=1
            if added: st.success(f"Saved {added} pantry item(s).")
            else: st.info("No new pantry items to save.")
            st.rerun()
    if saved_pantry:
        with st.expander("Manage saved pantry items"):
            for item in saved_pantry:
                a,b=st.columns([.8,.2])
                with a: st.write("🥫 "+item.get("name",""))
                with b:
                    if st.button("Remove",key="remove_pantry_"+item["id"]): remove("pantry",item["id"]); st.rerun()
    st.info("This version uses built-in recipes and ingredient matching, so it works without an AI key or internet recipe service. Recipe suggestions are a starting point; confirm quantities, allergies, and food safety before cooking.")

elif page=="Calendar & Reminders":
    section("Calendar & reminders","Shared plans, important dates, and gentle reminders.")
    with st.expander("＋ Add an event",expanded=bool(st.session_state.get("quick_open")==page or not events)):
        with st.form("event_form",clear_on_submit=True):
            title=st.text_input("What's happening?",placeholder="Family dinner")
            a,b=st.columns(2)
            with a: event_date=st.date_input("Date",value=today)
            with b: event_time=st.time_input("Time",value=time(18,0))
            location=st.text_input("Location (optional)"); details=st.text_area("Notes (optional)")
            reminder=st.selectbox("Reminder",["On the day","1 day before","3 days before","1 week before","No reminder"])
            if st.form_submit_button("Save event",use_container_width=True):
                if title.strip(): add("events",{"title":title.strip(),"date":event_date.isoformat(),"time":event_time.strftime("%H:%M"),"location":location.strip(),"notes":details.strip(),"reminder":reminder}); activity("Added event",title.strip()); st.rerun()
                else: st.warning("Please enter an event title.")
    events=get("events"); month=st.date_input("Browse month",value=today)
    month_events=[e for e in events if e.get("date") and as_date(e["date"]).year==month.year and as_date(e["date"]).month==month.month]
    st.markdown(f"### {month.strftime('%B %Y')}")
    for e in sorted(month_events,key=lambda x:(x.get("date",""),x.get("time",""))):
        with st.container(border=True):
            a,b=st.columns([.78,.22])
            with a:
                st.markdown(f"### 📅 {safe(e.get('title','Event'))}"); st.caption(f"{fmt_date(e['date'])} · {safe(e.get('time',''))}")
                if e.get("location"): st.write("Location: "+safe(e["location"]))
                if e.get("notes"): st.write(e["notes"])
                st.caption("Reminder: "+safe(e.get("reminder","On the day")))
            with b:
                if st.button("Delete",key="del_event_"+e["id"],use_container_width=True): remove("events",e["id"]); st.rerun()
    if not month_events: st.info("No events in this month yet.")
    section("Reminder centre","Reminders are calculated when the app is opened or refreshed.")
    reminders=[]
    for t in get("tasks"):
        if not t.get("done") and t.get("due") and as_date(t["due"])<=today: reminders.append(("Task",t.get("name","Task"),t["due"]))
    for e in events:
        if e.get("date"):
            days=(as_date(e["date"])-today).days
            lead={"On the day":0,"1 day before":1,"3 days before":3,"1 week before":7}.get(e.get("reminder","On the day"))
            if lead is not None and days==lead: reminders.append(("Event",e.get("title","Event"),e["date"]))
    if reminders:
        for kind,title,due in reminders: st.warning(f"{kind}: {title} · {fmt_date(due)}")
    else: st.success("No reminders due right now.")
    st.info("These are in-app reminders. Automatic push notifications or scheduled email require a separately configured scheduler/service.")

elif page=="Family Notes":
    section("Family notes","A shared place for messages, reminders, and little thoughts.")
    with st.expander("＋ Write a note",expanded=bool(st.session_state.get("quick_open")==page or not notes)):
        with st.form("note_form",clear_on_submit=True):
            title=st.text_input("Title",placeholder="A little reminder"); body=st.text_area("Your note",placeholder="Write something you want to remember...",height=130)
            author=st.selectbox("From",["Both","Suchi","Abi"])
            if st.form_submit_button("Save note",use_container_width=True):
                if body.strip(): add("notes",{"title":title.strip() or "A little note","body":body.strip(),"author":author,"created":stamp()}); activity("Added note",title.strip() or "A little note"); st.rerun()
                else: st.warning("Write a note before saving.")
    notes=get("notes")
    if not notes: st.info("Your saved notes will appear here.")
    for n in reversed(notes):
        with st.container(border=True):
            st.markdown(f"### ♡ {safe(n.get('title','A little note'))}"); st.caption(f"{safe(n.get('created',''))} · From {safe(n.get('author','Both'))}"); st.write(n.get("body",""))
            if st.button("Delete note",key="del_note_"+n["id"]): remove("notes",n["id"]); st.rerun()

elif page=="Memories":
    section("Our memories","A little timeline of moments you want to keep.")
    with st.expander("＋ Add a memory",expanded=not memories):
        with st.form("memory_form",clear_on_submit=True):
            title=st.text_input("Memory title",placeholder="Our lovely Sunday"); mem_date=st.date_input("When did it happen?",value=today)
            story=st.text_area("What do you want to remember?",placeholder="Write down the little details...")
            tags=st.text_input("Tags (optional)",placeholder="date night, trip, family"); photo=st.text_input("Photo URL (optional)",placeholder="https://...")
            if st.form_submit_button("Save memory",use_container_width=True):
                if title.strip() or story.strip():
                    add("memories",{"title":title.strip() or "A little moment","date":mem_date.isoformat(),"story":story.strip(),"tags":[t.strip() for t in tags.split(",") if t.strip()],"photo_url":photo.strip()}); activity("Saved memory",title.strip() or "A little moment"); st.rerun()
                else: st.warning("Add a title or a few words to remember.")
    memories=get("memories")
    if not memories: st.info("Your story starts here. Save a celebration or a small moment.")
    for m in sorted(memories,key=lambda x:x.get("date",""),reverse=True):
        with st.container(border=True):
            st.caption("✦  "+fmt_date(m.get("date",today.isoformat()))); st.markdown(f"### {safe(m.get('title','A little moment'))}")
            if str(m.get("photo_url","")).startswith(("https://","http://")): st.image(m["photo_url"],use_container_width=True)
            if m.get("story"): st.write(m["story"])
            if m.get("tags"): st.caption(" · ".join("#"+str(t) for t in m["tags"]))
            if st.button("Delete memory",key="del_mem_"+m["id"]): remove("memories",m["id"]); st.rerun()

elif page=="Household Budget":
    section("Household budget","A simple shared view of household spending and income.")
    tx=get("transactions"); month=today.strftime("%Y-%m"); month_tx=[x for x in tx if str(x.get("date",""))[:7]==month]
    income=sum(float(x.get("amount",0) or 0) for x in month_tx if x.get("kind")=="Income")
    expense=sum(float(x.get("amount",0) or 0) for x in month_tx if x.get("kind")=="Expense")
    a,b,c=st.columns(3)
    with a: metric("Income",f"€{income:,.2f}","This month","↗")
    with b: metric("Expenses",f"€{expense:,.2f}","This month","€")
    with c: metric("Balance",f"€{income-expense:,.2f}","Income minus expenses","◎")
    with st.expander("＋ Add transaction",expanded=not tx):
        with st.form("tx_form",clear_on_submit=True):
            desc=st.text_input("Description",placeholder="Groceries, electricity bill...")
            a,b,c=st.columns(3)
            with a: kind=st.selectbox("Type",["Expense","Income"])
            with b: amount=st.number_input("Amount (€)",min_value=0.0,step=1.0,format="%.2f")
            with c: trans_date=st.date_input("Date",value=today)
            category=st.selectbox("Category",["Groceries","Bills","Rent / mortgage","Transport","Home","Eating out","Income","Other"])
            paid=st.selectbox("Paid by",["Shared","Suchi","Abi"])
            if st.form_submit_button("Save transaction",use_container_width=True):
                if desc.strip() and amount>0: add("transactions",{"description":desc.strip(),"kind":kind,"amount":round(amount,2),"date":trans_date.isoformat(),"category":category,"paid_by":paid}); activity("Added transaction",desc.strip()); st.rerun()
                else: st.warning("Enter a description and amount greater than zero.")
    for x in sorted(get("transactions"),key=lambda z:z.get("date",""),reverse=True):
        with st.container(border=True):
            a,b=st.columns([.78,.22])
            with a:
                sign="+" if x.get("kind")=="Income" else "−"; st.markdown(f"**{safe(x.get('description','Transaction'))}** · {sign}€{float(x.get('amount',0)):,.2f}")
                st.caption(f"{fmt_date(x.get('date',today.isoformat()))} · {safe(x.get('category','Other'))} · Paid by {safe(x.get('paid_by','Shared'))}")
            with b:
                if st.button("Delete",key="del_tx_"+x["id"],use_container_width=True): remove("transactions",x["id"]); st.rerun()
    if tx:
        buf=io.StringIO(); writer=csv.writer(buf); writer.writerow(["date","description","kind","amount","category","paid_by"])
        for x in tx: writer.writerow([x.get("date"),x.get("description"),x.get("kind"),x.get("amount"),x.get("category"),x.get("paid_by")])
        st.download_button("Export transactions as CSV",buf.getvalue().encode("utf-8"),file_name="family_hub_budget.csv",mime="text/csv")

elif page=="Activity & Greetings":
    section("Greetings & activity","A small daily hello, plus a shared record of things you've done.")
    hour=now.hour; greeting="Good morning" if hour<12 else ("Good afternoon" if hour<18 else "Good evening")
    st.markdown(f"### {greeting}, Suchi & Abi ☀️")
    st.write("A fresh day, a fresh start. Thank each other for the little things, and remember that being a team matters more than a perfect to-do list.")
    with st.container(border=True):
        st.markdown("### 🎉 Celebrations & special dates")
        with st.form("celebration_form",clear_on_submit=True):
            title=st.text_input("Celebration or special date",placeholder="Anniversary, birthday, first date...")
            d=st.date_input("Date",value=today); person=st.selectbox("For",["Both","Suchi","Abi"])
            if st.form_submit_button("Save celebration"):
                if title.strip(): add("events",{"title":"🎉 "+title.strip(),"date":d.isoformat(),"time":"All day","location":"","notes":"Celebration · "+person,"reminder":"On the day"}); activity("Added celebration",title.strip()); st.rerun()
                else: st.warning("Enter a celebration name.")
    upcoming=sorted([e for e in get("events") if e.get("date") and as_date(e["date"])>=today],key=lambda e:e["date"])
    if upcoming:
        st.markdown("#### Coming up")
        for e in upcoming[:8]:
            with st.container(border=True): st.markdown(f"**{safe(e.get('title','Event'))}**"); st.caption(fmt_date(e["date"]))
    section("Recent shared activity","The latest changes made in this hub.")
    log=get("activity")
    if not log: st.info("Your shared activity will show here as you add tasks, notes, groceries, and memories.")
    for item in reversed(log[-40:]):
        with st.container(border=True):
            st.markdown(f"**{safe(item.get('action','Update'))}** · {safe(item.get('item',''))}")
            st.caption(item.get("when",""))

elif page=="Backups & Settings":
    section("Backups & settings","Keep your household information safe and portable.")
    st.markdown("### Persistent storage")
    st.write(f"Database file: `{DB_PATH}`")
    st.info("Both users share the same data only when they access the same deployed app connected to this same persistent database. A local database file does not sync across separate computers. For multiple app instances, configure a shared database.")
    backup={"app":"Our Family Hub","exported_at":stamp(),"collections":{n:get(n) for n in COLLECTIONS},"settings":{"mood":setting("mood","Happy")}}
    st.download_button("⬇ Download full JSON backup",json.dumps(backup,ensure_ascii=False,indent=2).encode("utf-8"),file_name=f"family_hub_backup_{today.isoformat()}.json",mime="application/json",use_container_width=True)
    st.markdown("### Restore backup")
    upload=st.file_uploader("Choose a Family Hub JSON backup",type=["json"])
    confirm=st.checkbox("I understand restoring replaces current data.")
    if st.button("Restore backup",disabled=not(upload and confirm),use_container_width=True):
        try:
            data=json.loads(upload.getvalue().decode("utf-8")); imported=data.get("collections",{})
            if not isinstance(imported,dict): raise ValueError("Backup is missing its collections.")
            for n in COLLECTIONS:
                vals=imported.get(n,[])
                if not isinstance(vals,list) or any(not isinstance(x,dict) for x in vals): raise ValueError(f"Invalid collection: {n}")
            for n in COLLECTIONS: put(n,imported.get(n,[]))
            set_setting("mood",data.get("settings",{}).get("mood","Happy"))
            st.success("Backup restored successfully."); st.rerun()
        except (ValueError,TypeError,UnicodeDecodeError,AttributeError) as exc: st.error(f"Could not restore backup: {exc}")
    st.markdown("### Notifications")
    st.write("In-app reminders show when you open or refresh the app. Scheduled email, push, or phone notifications need a separately configured scheduler or notification provider.")
    st.markdown("### Shared setup checklist")
    st.markdown("- Deploy one shared app URL for both users.\n- Keep the SQLite database on a persistent disk/volume.\n- Restrict access if notes and household finances are private.\n- Download backups regularly.")
    st.markdown("### Export all data")
    st.download_button("Download data as JSON",json.dumps(backup,ensure_ascii=False,indent=2).encode("utf-8"),file_name="family_hub_export.json",mime="application/json")

st.markdown("---")
st.markdown(f'<div style="text-align:center;color:{DARK["muted"]};padding:14px 0 8px;font-size:.85rem;line-height:1.9;"><span style="color:{DARK["accent"]};">♡</span> &nbsp; Suchi &amp; Abi &nbsp; · &nbsp; Our little corner of the world<br><span style="font-size:.78rem;">Small steps, big love.</span></div>',unsafe_allow_html=True)

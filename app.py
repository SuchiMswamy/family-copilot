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

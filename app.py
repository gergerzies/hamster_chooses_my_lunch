import streamlit as st
import os
import json
import random
import time
import base64
from datetime import datetime, timedelta

from streamlit_extras.let_it_rain import rain

# --- AI SETUP ---
AI_AVAILABLE = True
AI_ERROR_MSG = None

try:
    import google.generativeai as genai
    genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    AI_AVAILABLE = False
    AI_ERROR_MSG = str(e)


# --- AI HELPERS ---
def get_ai_horoscope():
    if not AI_AVAILABLE:
        return random.choice([
            "Chicken rice is calling your name.",
            "Avoid queues today. Eat early.",
            "That stall with the long line? Worth it.",
            "Today is a mala day."
        ])
    prompt = "Give a funny one-line food horoscope for a hungry NUS student."
    return model.generate_content(prompt).text.strip()


def get_ai_girl_math(cost):
    if not AI_AVAILABLE:
        return f"${cost:.2f} divided by happiness = basically free."
    prompt = f"Use girl math to justify spending ${cost:.2f} on food."
    return model.generate_content(prompt).text.strip()


def get_ai_pep_talk():
    if not AI_AVAILABLE:
        return "You got this. Just order confidently."
    prompt = "Give a funny but encouraging pep talk to someone ordering food."
    return model.generate_content(prompt).text.strip()

# ==========================================
# MAIN CONTROLLER
# ==========================================
setup_ui_styling()
show_sidebar()

if st.session_state.current_view == 'home':
    show_home_view()
elif st.session_state.current_view == 'canteen':
    show_canteen_view()
elif st.session_state.current_view == 'stall':
    show_stall_view()
    st.sidebar.divider()
    st.sidebar.subheader("🛠️ Dev Tools")
    if st.sidebar.button("⚠️ SIMULATE ACTIVITY"):
        canteen = st.session_state.selected_canteen
        stall = st.session_state.selected_stall
        current_stall_data = st.session_state.votes[canteen][stall]
        if 'queue_reports' not in current_stall_data: current_stall_data['queue_reports'] = []
        for i in range(10):
            fake_time = (datetime.now() - timedelta(minutes=1)).isoformat()
            current_stall_data['queue_reports'].append(fake_time)
        fake_users = ["HungryStudent22", "NUS_Foodie", "LateNightCoder", "ExchangeStudent_US", "AuntieKiller"]
        fake_comments = ["Solid 10/10!", "Queue was insane.", "A bit salty today.", "Cheap and good.", "Don't come at 12pm!"]
        for i in range(3):
            new_fake_review = {
                "user": random.choice(fake_users),
                "stars": random.randint(3, 5),
                "friendliness": random.randint(40, 100),
                "comment": random.choice(fake_comments),
                "timestamp": datetime.now().isoformat()
            }
            current_stall_data['reviews'].append(new_fake_review)
        save_data(st.session_state.votes)
        st.toast(f"💥 BOOM! Added 10 reports & 3 reviews to {stall}!")
        time.sleep(1)
        st.rerun()
        
elif st.session_state.current_view == 'add stall':
    show_add_stall_view()
elif st.session_state.current_view == 'leaderboard':
    show_leaderboard_view()
elif st.session_state.current_view == 'heatmap': 
    show_heatmap_view()
elif st.session_state.current_view == 'fun_zone':
    show_fun_zone()   
elif st.session_state.current_view == 'admin': 
    show_admin_view()

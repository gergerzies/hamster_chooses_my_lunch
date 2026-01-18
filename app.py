import streamlit as st
import json
import os
import time
import random
from datetime import datetime, timedelta, date
from streamlit_extras.let_it_rain import rain
import base64
import google.generativeai as genai

# --- CONSTANTS & CONFIG ---
st.set_page_config(
    page_title="NUS Foodie", 
    page_icon="assets/hamster.jpg", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- AI CONFIGURATION (ROBUST SETUP) ---
# 1. Try to get key from Streamlit Secrets (Best for Git/Cloud)
# 2. If not found, use the hardcoded key (Best for Local)
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    # ⚠️ REPLACE THIS WITH YOUR KEY FOR LOCAL TESTING
    api_key = "AIzaSyAGRc9LewU2pqOHgYh97MaIp9ymsd5CWHw" 

AI_AVAILABLE = False
AI_ERROR_MSG = None

try:
    genai.configure(api_key=api_key)
    # Switched to 1.5-flash (Faster, Newer, More Reliable)
    model = genai.GenerativeModel('gemini-2.0-flash')

    AI_AVAILABLE = True
except Exception as e:
    AI_AVAILABLE = False
    AI_ERROR_MSG = str(e)
    print(f"AI Setup Failed: {e}")

# --- MOCK DATA ---
GIRL_MATH_QUOTES = [
    "If you pay in cash, it's free because your bank account didn't go down.",
    "It's on sale, so you're actually making money.",
    "Calories don't count if you eat it standing up.",
    "Buying food is investing in your future energy.",
    "It's cheaper than therapy."
]

CONFIDENCE_TIPS = [
    "Don't make eye contact. Just point and nod.",
    "If Auntie asks 'Hah?', just say 'Yes' confidently.",
    "Have your card ready. Speed is respect.",
    "Call her 'Jie Jie' (Sister) for +10% portion size.",
    "Never hesitate. The queue smells fear."
]

HOROSCOPES = [
    "Avoid the Chicken Rice queue today. Bad vibes.",
    "Your lucky color is Mala Red.",
    "The Auntie at the drinks stall is thinking about you.",
    "Today is a good day to try something spicy.",
    "Mercury is in retrograde: Expect sold out Nasi Lemak."
]

# --- UI STYLING (CLEAN PEACH THEME 🍑) ---
def setup_ui_styling():
    st.markdown("""
        <style>
        /* 1. MAIN BACKGROUND */
        .stApp { 
            background-color: #FFF6EC; 
            color: #5A3A2E; 
        }
        
        h1, h2, h3, h4, h5, h6, p, li, span, div {
            color: #5A3A2E !important;
        }

        /* 2. SIDEBAR */
        section[data-testid="stSidebar"] { 
            background-color: #FFF6EC; 
            border-right: 3px solid #FFD1C1; 
        }
        
        /* 3. CARDS */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: #FFFFFF;
            border: 2px solid #FFD1C1;
            border-radius: 20px; 
            padding: 20px;
            box-shadow: 0 6px 15px rgba(90, 58, 46, 0.05);
        }
        
        /* 4. BUTTONS */
        div.stButton > button {
            background: linear-gradient(135deg, #FFB87A 0%, #FFC38B 100%);
            color: #5A3A2E !important; 
            border: none;
            border-radius: 12px; 
            padding: 0.5rem 1rem; 
            font-weight: bold;
            box-shadow: 0 4px 10px rgba(255, 184, 122, 0.4);
            transition: all 0.3s ease;
        }
        
        div.stButton > button:hover { 
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 184, 122, 0.6);
        }
        
        /* 5. METRICS */
        [data-testid="stMetric"] { 
            background-color: #FFFFFF; 
            border: 2px solid #FFD1C1; 
        }
        
        /* 6. ANIMATION */
        .main .block-container { 
            animation: fadeInAnimation 0.5s ease-in-out; 
        }
        
        @keyframes fadeInAnimation { 
            0% { opacity: 0; transform: translateY(10px); } 
            100% { opacity: 1; transform: translateY(0); } 
        }
        </style>
    """, unsafe_allow_html=True)

# --- HELPER: IMAGE LOADER ---
def show_header_image(image_name):
    image_path = os.path.join("assets", image_name)
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            encoded_image = base64.b64encode(f.read()).decode()
        st.markdown(f"""
            <div style="width: 100%; height: 200px; background-image: url('data:image/jpeg;base64,{encoded_image}');
            background-size: cover; background-position: center; border-radius: 15px;
            border: 4px solid #FFB87A; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(90,58,46,0.1);"></div>
            """, unsafe_allow_html=True)

def show_thumbnail(image_name):
    image_path = os.path.join("assets", image_name)
    if not os.path.exists(image_path): return
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <div style="width: 100%; height: 150px; background-image: url('data:image/jpeg;base64,{encoded_image}');
        background-size: cover; background-position: center; border-radius: 12px; margin-bottom: 10px;
        border: 2px solid #FFD1C1;"></div>
        """, unsafe_allow_html=True)

def show_popout_hamster(image_name, caption_text):
    image_path = os.path.join("assets", image_name)
    if os.path.exists(image_path):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(image_path, caption=caption_text)

# --- AI HELPER FUNCTIONS ---
def get_ai_girl_math(price):
    if not AI_AVAILABLE: return f"Math is hard. (Error: {AI_ERROR_MSG})"
    try:
        prompt = f"Using 'Girl Math' logic, explain why spending ${price} on food/drink is actually free. Be funny and concise."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"AI Error: {e}"

def get_ai_pep_talk():
    if not AI_AVAILABLE: return f"You got this! (Error: {AI_ERROR_MSG})"
    try:
        prompt = "Give a short, funny pep talk to a socially anxious student ordering food at a Singapore hawker center using Singlish."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"AI Error: {e}"

def get_ai_horoscope():
    if not AI_AVAILABLE: return f"The stars are silent. (Error: {AI_ERROR_MSG})"
    try:
        prompt = "Give a one-sentence, funny, food-related horoscope for a university student in Singapore."
        response = model.generate_content(prompt)
        return response.text
    except Exception as e: return f"AI Error: {e}"

# --- BACKEND FUNCTIONS ---
def save_pending(data):
    with open('pending.json', 'w') as f: json.dump(data, f)

def save_data(data):
    with open('votes.json', 'w') as f: json.dump(data, f)

def load_data():
    if os.path.exists('votes.json'):
        with open('votes.json', 'r') as f: return json.load(f)
    else:
        return {
            "Yusof Ishak House": {"Wok Express": {"reviews": [], "queue_reports": []}},
            "Techno Edge": {"Western Food": {"reviews": [], "queue_reports": []}},
            "The Terrace": {"Drinks & Hot Foods": {"reviews": [], "queue_reports": []}},
            "The Deck": {"Western": {"reviews": [], "queue_reports": []}},
            "PGPR": {"Mala Hotpot": {"reviews": [], "queue_reports": []}},
            "The Summit": {"Noodles": {"reviews": [], "queue_reports": []}},
            "Frontier": {"Gong Cha": {"reviews": [], "queue_reports": []}},
            "Fine Food": {"Italian": {"reviews": [], "queue_reports": []}},
            "Flavours": {"Ban Mian": {"reviews": [], "queue_reports": []}}
        }

def load_pending():
    if os.path.exists('pending.json'):
        with open('pending.json', 'r') as f: return json.load(f)
    else: return []

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f: return json.load(f)
    else: return {}

def save_users(data):
    with open('users.json', 'w') as f: json.dump(data, f)

def add_points(username, points):
    users = load_users()
    clean_name = username.strip()
    if clean_name in users: users[clean_name] += points
    else: users[clean_name] = points
    save_users(users)
    return users[clean_name]

# --- INIT STATE ---
if 'votes' not in st.session_state: st.session_state.votes = load_data()
if 'current_view' not in st.session_state: st.session_state.current_view = 'home'
if 'selected_canteen' not in st.session_state: st.session_state.selected_canteen = None
if 'selected_stall' not in st.session_state: st.session_state.selected_stall = None
if 'show_angry_popup' not in st.session_state: st.session_state.show_angry_popup = False

# --- NAVIGATION HELPERS ---
def go_to_home():
    st.session_state.current_view = 'home'
    st.rerun()

def go_to_canteen(canteen_name):
    st.session_state.selected_canteen = canteen_name
    st.session_state.current_view = 'canteen'
    st.rerun()

def go_to_stall(stall_name):
    st.session_state.selected_stall = stall_name
    st.session_state.current_view = 'stall'
    st.rerun()

def go_to_add_stall():
    st.session_state.current_view = 'add stall'
    st.rerun()

# --- LOGIC FUNCTIONS ---
def get_queue_status(stall_data):
    reports = stall_data.get('queue_reports', [])
    now = datetime.now()
    recent_reports = [t for t in reports if now - datetime.fromisoformat(t) < timedelta(minutes=10)]
    if len(recent_reports) >= 5: return "🔴 CROWDED", f"High alert! {len(recent_reports)} reports."
    elif len(recent_reports) >= 1: return "🟡 BUILDING UP", f"{len(recent_reports)} recent reports."
    else: return "🟢 CLEAR", "Looks chill. Go eat."

def protect_auntie_feelings():
    if st.session_state.user_rating < 3:
        st.session_state.user_rating = random.choice([4, 5])
        st.session_state.show_angry_popup = True 
        st.toast("The auntie saw that. 5 Stars only!", icon="😡")

def calculate_scolding_risk(reviews):
    if not reviews: return "🟡 Risky (No Data)"
    avg_friendliness = sum(r.get('friendliness', 50) for r in reviews) / len(reviews)
    anger_score = 100 - avg_friendliness
    now_str = int(datetime.now().strftime("%H%M"))
    if 1130 <= now_str <= 1330: anger_score += 20 
    if anger_score > 80: return "🔴 CONFIRM KENA"
    elif anger_score > 40: return "🟡 Risky"
    else: return "🟢 Safe Zone"

def get_indecision_killer():
    all_stalls = []
    for canteen in st.session_state.votes:
        for stall in st.session_state.votes[canteen]:
            all_stalls.append(f"{stall} ({canteen})")
    return random.choice(all_stalls)

# ==========================================
# VIEWS
# ==========================================

def show_sidebar():
    with st.sidebar:
        image_path = "assets/hamster.jpg"
        icon_html = "🐹" 
        
        if os.path.exists(image_path):
            with open(image_path, "rb") as f:
                encoded_image = base64.b64encode(f.read()).decode()
            icon_html = f'<img src="data:image/jpeg;base64,{encoded_image}" style="width: 190px; height: auto; border-radius: 15px; border: 3px solid #EF7C00;">'
            
        st.markdown(f"""
            <div style="display: flex; flex-direction: column; align-items: flex-start; gap: 10px; margin-bottom: 20px;">
                <h1 style="margin: 0; padding: 0; font-size: 38px; line-height: 1.2; color: #003D7C;">
                    NUS Foodie
                </h1>
                {icon_html} 
            </div>
            """, unsafe_allow_html=True)

        st.caption("Your survival guide.")
        st.divider()
        
        if st.button("🏠 Home", use_container_width=True): go_to_home()
        if st.button("🗺️ Hunger Heatmap", use_container_width=True):
            st.session_state.current_view = 'heatmap'
            st.rerun()
        if st.button("🎡 Fun Zone", use_container_width=True):
            st.session_state.current_view = 'fun_zone'
            st.rerun()
        if st.button("🏆 Leaderboard", use_container_width=True):
            st.session_state.current_view = 'leaderboard'
            st.rerun()
        
        st.divider()
        
        with st.expander("🔐 Admin Access"):
            password = st.text_input("Password:", type="password")
            
            if password == "nus123": 
                st.success("Access Granted")
                st.divider()
                st.write("**🛠️ Admin Tools**")
                
                if st.button("💣 RESET ALL DATA", use_container_width=True):
                    if os.path.exists('votes.json'): os.remove('votes.json')
                    if os.path.exists('pending.json'): os.remove('pending.json')
                    if os.path.exists('users.json'): os.remove('users.json')
                    for key in list(st.session_state.keys()): del st.session_state[key]
                    st.toast("System Reset! Reloading...")
                    time.sleep(1)
                    st.rerun()
                
                st.write("**📊 Dashboard**")
                if st.button("Enter Dashboard", use_container_width=True):
                    st.session_state.current_view = 'admin'
                    st.rerun()
        
        st.caption("Hack & Roll 2026")

def show_home_view():
    show_header_image("nus_campus.jpg") 
    st.title("HAMSTER CHOOSES YOUR FOOD 🍜")
    st.write("Where are you eating today?")
    st.divider()
    canteens = list(st.session_state.votes.keys())
    use_default_image = ["PGPR", "Fine Food", "Flavours", "The Deck"]

    cols = st.columns(2)
    for i, canteen in enumerate(canteens):
        with cols[i % 2]:
            with st.container(border=True):
                if canteen in use_default_image:
                    show_thumbnail("Default.jpg")
                else:
                    show_thumbnail(f"{canteen}.jpg")
                
                st.markdown(f"""
                    <div style="height: 60px; display: flex; align-items: center; margin-bottom: 10px;">
                        <h3 style="margin: 0; padding: 0; line-height: 1.2;">{canteen}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.button(f"Visit ➡️", key=f"btn_{canteen}", use_container_width=True):
                    with st.spinner(f"Walking to {canteen}..."):
                        time.sleep(0.3)
                        go_to_canteen(canteen)

def show_canteen_view():
    canteen = st.session_state.selected_canteen
    custom_images = {
        "PGPR": "Default.jpg", "Fine Food": "Default.jpg",
        "Flavours": "Default.jpg", "The Deck": "Default.jpg"
    }
    
    if canteen in custom_images: show_header_image(custom_images[canteen])
    else: show_header_image(f"{canteen}.jpg")

    if st.button("⬅️ Back to Map"): go_to_home()
    st.title(f"Welcome to {canteen}")
    st.divider()
    stall_data = st.session_state.votes[canteen]
    for stall_name in stall_data.keys():
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader(stall_name)
                status_label, _ = get_queue_status(stall_data[stall_name])
                st.caption(f"Status: {status_label}")
            with col2:
                st.write("###") 
                if st.button("View ➡️", key=stall_name, use_container_width=True):
                    with st.spinner("Checking queue..."):
                        time.sleep(0.3)
                        go_to_stall(stall_name)
    st.divider()
    if st.button("➕ Add Missing Stall", use_container_width=True, key="add_missing_btn"):
        go_to_add_stall()

def show_add_stall_view():
    canteen = st.session_state.selected_canteen
    show_header_image(f"{canteen}.jpg")
    st.title("➕ Add a New Stall")
    st.write(f"Help us update **{canteen}**! What is missing?")
    st.divider()
    with st.container(border=True):
        new_stall_name = st.text_input("Stall Name:", placeholder="e.g., Western Food (Halal)")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("❌ Cancel", use_container_width=True): go_to_canteen(canteen)
        with col2:
            if st.button("✅ Add Stall", use_container_width=True):
                if new_stall_name.strip() == "": st.error("Please type a name!")
                elif new_stall_name in st.session_state.votes[canteen]: st.error("This stall already exists!")
                else:
                    pending_list = load_pending()
                    new_request = {
                        "canteen": canteen, "stall_name": new_stall_name,
                        "timestamp": datetime.now().isoformat()
                    }
                    pending_list.append(new_request)
                    save_pending(pending_list)
                    st.success("Submission received! An admin will review it shortly. 🛡️")
                    time.sleep(2)
                    go_to_canteen(canteen)

def show_stall_view():
    canteen = st.session_state.selected_canteen
    stall = st.session_state.selected_stall
    stall_data = st.session_state.votes[canteen][stall]
    reviews_list = stall_data['reviews']
    show_header_image(f"{stall}.jpg")
    if st.button(f"⬅️ Back to {canteen}"): go_to_canteen(canteen)
    st.title(stall)
    
    col_q1, col_q2 = st.columns([2, 1])
    with col_q1:
        status_label, status_msg = get_queue_status(stall_data)
        if "CLEAR" in status_label:
            bg_color = "#E3FCEC"; border_color = "#0DF2C9"; text_color = "#004D40"
        elif "BUILDING" in status_label:
            bg_color = "#FFF4E5"; border_color = "#FFA421"; text_color = "#E65100"
        else: 
            bg_color = "#FFEBEE"; border_color = "#FF4B4B"; text_color = "#B71C1C"
            
        st.markdown(f"""
        <div style="background-color: {bg_color}; padding: 15px; border-radius: 10px; border: 2px solid {border_color}; text-align: center; margin-bottom: 10px;">
            <p style="margin:0; font-size: 14px; font-weight: bold; color: {text_color}; opacity: 0.8;">LIVE TRAFFIC</p>
            <h2 style="margin:0; font-size: 32px; color: {text_color};">{status_label}</h2>
            <p style="margin:0; font-size: 14px; color: {text_color}; margin-top: 5px;">{status_msg}</p>
        </div>
        """, unsafe_allow_html=True)

    with col_q2:
        st.write("###") 
        if st.button("😤 Report Queue", use_container_width=True):
            if 'queue_reports' not in stall_data: stall_data['queue_reports'] = []
            stall_data['queue_reports'].append(datetime.now().isoformat())
            save_data(st.session_state.votes)
            st.toast("Queue reported! 🚨")
            st.rerun()
    st.divider()
    
    col_input, col_stats = st.columns([1, 1])
    with col_input:
        with st.container(border=True): 
            st.subheader("✍️ Rate & Review")
            
            if st.session_state.show_angry_popup:
                show_popout_hamster("hamster5.jpg", "Auntie is watching you...")

            reviewer_name = st.text_input("Your Nickname:", placeholder="e.g. FoodKing99")
            if "user_rating" not in st.session_state: st.session_state.user_rating = 5
            st.slider("Food Rating:", 1, 5, key="user_rating", on_change=protect_auntie_feelings)
            mood = st.slider("Auntie's Mood:", 0, 100, 50, key="mood_slider")
            comment = st.text_input("Comment:", placeholder="Any scolding involved?")
            
            if st.button("Submit Review 🚀", use_container_width=True):
                if not reviewer_name.strip(): st.error("Please enter a nickname to get points!")
                else:
                    new_review = {
                        "user": reviewer_name, "stars": st.session_state.user_rating,
                        "friendliness": mood, "comment": comment, "timestamp": datetime.now().isoformat()
                    }
                    stall_data['reviews'].append(new_review)
                    save_data(st.session_state.votes)
                    new_total = add_points(reviewer_name, 10)
                    
                    show_popout_hamster("hamster1.jpg", "Thank you for the review!")
                    rain(emoji="🏆", font_size=54, falling_speed=5, animation_length=1)
                    st.toast(f"Review Saved! +10 Points ({new_total} total) 🪙")
                    
                    st.session_state.show_angry_popup = False
                    time.sleep(2)
                    st.rerun()
                    
    with col_stats:
        with st.container(border=True):
            st.subheader("📊 Statistics")
            if reviews_list:
                avg_stars = sum(r['stars'] for r in reviews_list) / len(reviews_list)
                avg_mood = sum(r.get('friendliness', 50) for r in reviews_list) / len(reviews_list)
                badge = calculate_scolding_risk(reviews_list)
                st.info(f"Forecast: {badge}")
                st.write(f"**Auntie's Mood:** {avg_mood:.0f}%")
                st.progress(avg_mood / 100)
                st.caption("0% = 👿 Demon | 100% = 😇 Angel")
                st.divider()
                st.write(f"**Rating:** {avg_stars:.1f} / 5.0 ⭐")
                st.caption(f"Based on {len(reviews_list)} reviews")
                st.write("---")
                st.caption("Recent Chatter:")
                for r in reversed(reviews_list[-3:]):
                    st.text(f"⭐ {r['stars']} | {r.get('comment', '-')}")
            else: st.info("No reviews yet.")

# --- HEATMAP LOGIC ---
def show_heatmap_view():
    st.title("NUS Hunger Heatmap 🗺️")
    st.caption("Live crowd monitoring across campus. Data updates every 15 mins.")
    col1, col2 = st.columns([3, 1])
    with col1: st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    with col2:
        if st.button("🔄 Refresh Map"): st.rerun()

    canteen_positions = {
        "Yusof Ishak House": {"left": 35, "top": 60}, 
        "Techno Edge": {"left": 20, "top": 58},       
        "The Terrace": {"left": 27, "top": 82},       
        "The Deck": {"left": 22, "top": 72},          
        "PGPR": {"left": 75, "top": 78},                     
        "Frontier": {"left": 65, "top": 60},          
        "Fine Food": {"left": 25, "top": 40},         
        "Flavours": {"left": 18, "top": 28},          
    }

    canteen_status = {}
    if 'votes' in st.session_state:
        for canteen_name in st.session_state.votes.keys():
            if canteen_name not in canteen_positions: continue
            total_reports = 0
            stall_dict = st.session_state.votes[canteen_name]
            now = datetime.now()
            for stall in stall_dict.values():
                reports = stall.get('queue_reports', [])
                for time_str in reports:
                    if now - datetime.fromisoformat(time_str) < timedelta(minutes=15):
                        total_reports += 1
            if total_reports >= 5: canteen_status[canteen_name] = {"color": "#ff4b4b", "text": f"🔥 BUSY ({total_reports})"}
            elif total_reports >= 2: canteen_status[canteen_name] = {"color": "#ffa421", "text": f"⚠️ WARM ({total_reports})"}
            else: canteen_status[canteen_name] = {"color": "#0df2c9", "text": "🟢 CLEAR"}

    map_path = os.path.join("assets", "nus_map.jpg")
    if os.path.exists(map_path):
        with open(map_path, "rb") as f: encoded_map = base64.b64encode(f.read()).decode()
    else:
        st.error("⚠️ Missing 'nus_map.jpg' in assets folder!")
        return

    markers_html = ""
    for name, pos in canteen_positions.items():
        if name in canteen_status:
            data = canteen_status[name]
            markers_html += f"""
            <div class="map-marker" style="left: {pos['left']}%; top: {pos['top']}%;">
                <div class="pulsating-circle" style="background-color: {data['color']};"></div>
                <div class="marker-label"><strong>{name}</strong><br>{data['text']}</div>
            </div>"""

    st.markdown(f"""
        <style>
        .map-container {{ position: relative; width: 100%; height: 600px; background-image: url('data:image/jpeg;base64,{encoded_map}'); background-size: contain; background-repeat: no-repeat; background-position: center; border-radius: 15px; box-shadow: 0 4px 10px rgba(90,58,46,0.1); margin-bottom: 20px; background-color: #f0f8ff; }}
        .map-marker {{ position: absolute; transform: translate(-50%, -50%); display: flex; flex-direction: column; align-items: center; cursor: pointer; z-index: 5; }}
        .map-marker:hover .marker-label {{ opacity: 1; transform: translateY(0); }}
        .pulsating-circle {{ width: 20px; height: 20px; border-radius: 50%; box-shadow: 0 0 0 rgba(0, 0, 0, 0.2); animation: pulse 2s infinite; border: 2px solid white; }}
        .marker-label {{ margin-top: 5px; background: rgba(255, 255, 255, 0.95); padding: 5px 10px; border-radius: 8px; font-size: 0.8em; text-align: center; box-shadow: 0 2px 5px rgba(90,58,46,0.2); opacity: 0; transition: all 0.2s; transform: translateY(5px); white-space: nowrap; pointer-events: none; z-index: 10; color: #5A3A2E; }}
        @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7); transform: scale(0.95); }} 70% {{ box-shadow: 0 0 0 10px rgba(255, 255, 255, 0); transform: scale(1); }} 100% {{ box-shadow: 0 0 0 0 rgba(255, 255, 255, 0); transform: scale(0.95); }} }}
        </style>
        <div class="map-container">{markers_html}</div>
        """, unsafe_allow_html=True)
    if st.button("🏠 Back Home"): go_to_home()

def show_fun_zone():
    show_header_image("fun_zone.jpg")
    st.title("🎡 The Hawker Playground")
    st.write("Too stressed to choose? Let the AI decide.")
    st.divider()
    
    if not AI_AVAILABLE and AI_ERROR_MSG:
        st.error(f"⚠️ AI Services Unavailable. Reason: {AI_ERROR_MSG}")
        st.caption("Falling back to random quotes.")

    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("🔮 Daily Horoscope")
            if st.button("Reveal Food Fortune"):
                with st.spinner("Consulting the ancestors..."):
                    fortune = get_ai_horoscope()
                    st.info(f"✨ {fortune}")
        
        with st.container(border=True):
            st.subheader("💸 Girl/Boy Math")
            cost = st.number_input("Meal Cost ($):", value=5.0, step=0.5)
            if st.button("Justify Purchase"):
                with st.spinner("Calculating delusion..."):
                    justification = get_ai_girl_math(cost)
                    st.toast("Math checked out! ✅", icon="💅")
                    st.success(f"**Analysis:** {justification}")

    with col2:
        with st.container(border=True):
            st.subheader("⚡ Indecision Killer")
            if st.button("Spin the Wheel 🎡"):
                chosen = get_indecision_killer()
                st.success(f"🛑 GO EAT: **{chosen}**")
        
        with st.container(border=True):
            st.subheader("🦁 Social Anxiety Coach")
            if st.button("Give me a pep talk"):
                with st.spinner("Channeling confidence..."):
                    tip = get_ai_pep_talk()
                    st.warning(f"📢 COACH SAYS: {tip}")

    if st.button("🏠 Back Home"): go_to_home()

def show_leaderboard_view():
    show_header_image("leaderboard.jpg") 
    st.title("🏆 Hall of Fame")
    st.write("Top contributors saving hungry students.")
    st.divider()
    users = load_users()
    if not users:
        st.info("No points yet. Be the first to review!")
        return
    sorted_users = sorted(users.items(), key=lambda item: item[1], reverse=True)
    top_5 = sorted_users[:5]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("### 🥇 Top 1")
        if len(top_5) > 0:
            winner, score = top_5[0]
            st.metric(label=winner, value=f"{score} pts")
            st.markdown(f"**The Food God** 👑")
    with col2:
        st.write("### 🥈 Runners Up")
        for i, (name, score) in enumerate(top_5[1:], start=2):
            st.write(f"**#{i} {name}** - {score} pts")
            st.progress(min(score / (top_5[0][1] + 1), 1.0))
    with st.expander("See All Rankings"):
        st.table({"User": [u[0] for u in sorted_users], "Points": [u[1] for u in sorted_users]})
    if st.button("🏠 Back Home"): go_to_home()

def show_admin_view():
    st.title("🛡️ Admin Dashboard")
    st.write("Review user submissions here.")
    st.divider()
    pending_list = load_pending()
    if not pending_list:
        st.success("✅ No pending submissions. You are all caught up!")
        if st.button("🏠 Back Home"): go_to_home()
        return
    for i, request in enumerate(reversed(pending_list)):
        canteen = request['canteen']
        stall = request['stall_name']
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.subheader(stall)
                st.caption(f"Location: {canteen}")
            with col2:
                if st.button("✅ Approve", key=f"app_{i}", use_container_width=True):
                    if stall not in st.session_state.votes[canteen]:
                        st.session_state.votes[canteen][stall] = {"reviews": [], "queue_reports": []}
                        save_data(st.session_state.votes)
                        st.toast(f"Approved {stall}!")
                    pending_list.remove(request)
                    save_pending(pending_list)
                    time.sleep(0.5)
                    st.rerun()
            with col3:
                if st.button("❌ Reject", key=f"rej_{i}", use_container_width=True):
                    pending_list.remove(request)
                    save_pending(pending_list)
                    st.toast("Submission rejected.")
                    time.sleep(0.5)
                    st.rerun()

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

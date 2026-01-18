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

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

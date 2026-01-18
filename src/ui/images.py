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

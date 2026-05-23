import streamlit as st

st.set_page_config(page_title="About · SnackScanKH", page_icon="👨‍💻", layout="centered")

if "accent" not in st.session_state:
    st.session_state.accent = "#7c3aed"

acc = st.session_state.accent

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}
.stApp {{ background: #f7f7f7; min-height: 100vh; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2.5rem; max-width: 600px; }}

.about-card {{
    background: white;
    border-radius: 24px;
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #ebebeb;
    margin-bottom: 1rem;
}}

.avatar-ring {{
    width: 90px; height: 90px; border-radius: 50%;
    margin: 0 auto 1.2rem;
    display: flex; align-items: center; justify-content: center;
    position: relative; font-size: 2.4rem;
    background: #f5f5f5;
    border: 3px solid {acc};
}}

.about-name {{ font-size: 1.5rem; font-weight: 700; color: #111; margin: 0 0 0.4rem; }}
.about-bio  {{ font-size: 0.92rem; color: #aaa; margin: 0 0 1.8rem; line-height: 1.7; }}

.about-stats {{
    display: flex; justify-content: center; gap: 2.5rem;
    padding: 1.4rem 0;
    border-top: 1px solid #f0f0f0;
    border-bottom: 1px solid #f0f0f0;
    margin-bottom: 1.8rem;
}}
.stat-val   {{ font-size: 1.2rem; font-weight: 700; color: {acc}; display: block; }}
.stat-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px; color: #bbb; }}

.gh-link {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {acc};
    border-radius: 99px; padding: 10px 24px;
    font-size: 0.88rem; font-weight: 600;
    color: white; text-decoration: none;
    transition: opacity 0.2s;
}}
.gh-link:hover {{ opacity: 0.85; text-decoration: none; color: white; }}
.about-footer {{ margin-top: 1.5rem; font-size: 0.72rem; color: #ccc; }}

.color-card {{
    background: white;
    border-radius: 20px;
    padding: 1.6rem 2rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    border: 1px solid #ebebeb;
    text-align: center;
}}
.section-label {{
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: #bbb; margin-bottom: 1rem; display: block;
}}
.preview-bar {{
    height: 6px;
    border-radius: 99px;
    background: {acc};
    margin: 1rem auto 0;
    max-width: 200px;
    transition: background 0.3s;
}}

/* Style the color picker */
[data-testid="stColorPicker"] {{
    display: flex;
    justify-content: center;
}}
[data-testid="stColorPicker"] > div {{
    width: 56px !important;
    height: 56px !important;
    border-radius: 50% !important;
    border: 3px solid #eee !important;
    overflow: hidden !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    cursor: pointer !important;
}}
</style>
""", unsafe_allow_html=True)

# ── About card ──
st.markdown(f"""
<div class="about-card">
    <div class="avatar-ring">👨‍💻</div>
    <div class="about-name">Than Vireakseth</div>
    <div class="about-bio">
        A student developer from Cambodia 🇰🇭<br>
        Building things with AI, one scan at a time.
    </div>
    <div class="about-stats">
        <div class="stat-item"><span class="stat-val">Gemini</span><span class="stat-label">AI Model</span></div>
        <div class="stat-item"><span class="stat-val">2</span><span class="stat-label">Languages</span></div>
        <div class="stat-item"><span class="stat-val">6</span><span class="stat-label">Nutrients</span></div>
    </div>
    <a class="gh-link" href="https://github.com/ReaX3ops" target="_blank">⌥ github.com/ReaX3ops</a>
    <div class="about-footer">Made with ♥ in Phnom Penh · SnackScanKH © 2026</div>
</div>
""", unsafe_allow_html=True)

# ── Color picker card ──
st.markdown("""
<div class="color-card">
    <span class="section-label">✦ Accent Color</span>
</div>
""", unsafe_allow_html=True)

picked = st.color_picker(
    "Accent",
    value=st.session_state.accent,
    label_visibility="collapsed"
)

st.markdown(f'<div class="preview-bar" style="background:{picked};"></div>', unsafe_allow_html=True)

if picked != st.session_state.accent:
    st.session_state.accent = picked
    st.rerun()
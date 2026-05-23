import streamlit as st

st.set_page_config(page_title="About · SnackScanKH", page_icon="👨‍💻", layout="centered")

if "accent" not in st.session_state:
    st.session_state.accent = "#7c3aed"

acc = st.session_state.accent

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}

.stApp {{
    background: linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%);
    min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2.5rem; max-width: 600px; }}

.glass {{
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.75);
    box-shadow: 0 8px 32px rgba(0,0,0,0.07), 0 1px 0 rgba(255,255,255,0.9) inset;
    border-radius: 24px;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}
@keyframes floatOrb {{
    0%,100% {{ transform: translate(0,0); }}
    50%     {{ transform: translate(12px,16px); }}
}}
@keyframes spinRing {{
    from {{ transform: rotate(0deg); }}
    to   {{ transform: rotate(360deg); }}
}}

.about-card {{
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.55s ease both;
}}
.about-card::before {{
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 300%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
    animation: shimmer 4s linear infinite;
}}
.orb {{
    position: absolute; border-radius: 50%; pointer-events: none;
}}
.orb1 {{
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(124,58,237,0.07) 0%, transparent 70%);
    top: -70px; left: -70px;
    animation: floatOrb 7s ease-in-out infinite;
}}
.orb2 {{
    width: 160px; height: 160px;
    background: radial-gradient(circle, rgba(14,165,233,0.06) 0%, transparent 70%);
    bottom: -50px; right: -50px;
    animation: floatOrb 8s ease-in-out infinite reverse;
}}

.avatar-wrap {{
    width: 92px; height: 92px;
    margin: 0 auto 1.3rem;
    position: relative;
}}
.avatar-inner {{
    width: 92px; height: 92px; border-radius: 50%;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(12px);
    border: 2px solid rgba(255,255,255,0.9);
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}}
.avatar-ring-spin {{
    position: absolute; inset: -4px; border-radius: 50%;
    border: 2px solid transparent;
    border-top-color: {acc};
    border-right-color: rgba(124,58,237,0.3);
    animation: spinRing 3s linear infinite;
}}

.about-name {{ font-size: 1.5rem; font-weight: 700; color: #1a1a2e; margin: 0 0 0.4rem; }}
.about-bio  {{ font-size: 0.92rem; color: rgba(0,0,0,0.4); margin: 0 0 1.8rem; line-height: 1.7; }}

.about-stats {{
    display: flex; justify-content: center; gap: 2.5rem;
    padding: 1.4rem 0;
    border-top: 1px solid rgba(255,255,255,0.6);
    border-bottom: 1px solid rgba(255,255,255,0.6);
    margin-bottom: 1.8rem;
}}
.stat-val   {{ font-size: 1.2rem; font-weight: 700; color: {acc}; display: block; }}
.stat-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px; color: rgba(0,0,0,0.35); }}

.gh-link {{
    display: inline-flex; align-items: center; gap: 8px;
    background: {acc};
    border-radius: 99px; padding: 10px 26px;
    font-size: 0.88rem; font-weight: 600;
    color: white; text-decoration: none;
    box-shadow: 0 6px 20px rgba(124,58,237,0.28);
    transition: all 0.25s;
}}
.gh-link:hover {{
    opacity: 0.88; text-decoration: none; color: white;
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(124,58,237,0.38);
}}
.about-footer {{ margin-top: 1.5rem; font-size: 0.72rem; color: rgba(0,0,0,0.25); }}

.color-card {{
    padding: 1.6rem 2rem 1.8rem;
    text-align: center;
    animation: fadeUp 0.6s ease 0.1s both;
}}
.section-label {{
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: rgba(0,0,0,0.3); margin-bottom: 1.2rem; display: block;
}}
.preview-bar {{
    height: 5px; border-radius: 99px;
    background: {acc};
    margin: 1rem auto 0; max-width: 180px;
    transition: background 0.35s ease;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25);
}}

[data-testid="stColorPicker"] {{ display: flex; justify-content: center; }}
[data-testid="stColorPicker"] > div {{
    width: 58px !important; height: 58px !important;
    border-radius: 50% !important;
    border: 3px solid rgba(255,255,255,0.85) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
    cursor: pointer !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stColorPicker"] > div:hover {{
    transform: scale(1.08) !important;
    box-shadow: 0 6px 20px rgba(0,0,0,0.16) !important;
}}
</style>
""", unsafe_allow_html=True)

# ── About card ──
st.markdown(f"""
<div class="glass about-card">
    <div class="orb orb1"></div>
    <div class="orb orb2"></div>
    <div class="avatar-wrap">
        <div class="avatar-inner">👨‍💻</div>
        <div class="avatar-ring-spin"></div>
    </div>
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

# ── Color picker ──
st.markdown("""
<div class="glass color-card">
    <span class="section-label">✦ Accent Color</span>
</div>
""", unsafe_allow_html=True)

picked = st.color_picker("Accent", value=st.session_state.accent, label_visibility="collapsed")
st.markdown(f'<div class="preview-bar" style="background:{picked};"></div>', unsafe_allow_html=True)

if picked != st.session_state.accent:
    st.session_state.accent = picked
    st.rerun()
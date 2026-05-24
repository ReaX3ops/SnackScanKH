import streamlit as st

st.set_page_config(page_title="Welcome · AhaLaor AI", page_icon="favicon.png", layout="centered")

if "accent" not in st.session_state:
    st.session_state.accent = "#7c3aed"
if "bg" not in st.session_state:
    st.session_state.bg = "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)"
if "onboarding_step" not in st.session_state:
    st.session_state.onboarding_step = 0

acc = st.session_state.accent
bg  = st.session_state.bg

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}
.stApp, html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {bg} !important; min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 4rem; max-width: 500px; }}

.frost {{
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(40px) saturate(200%);
    -webkit-backdrop-filter: blur(40px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.85);
    box-shadow: 0 20px 60px rgba(0,0,0,0.07), 0 2px 0 rgba(255,255,255,0.9) inset;
    border-radius: 28px;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(24px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.ob-card {{
    padding: 3rem 2.5rem;
    text-align: center;
    animation: fadeUp 0.5s ease both;
    position: relative; overflow: hidden;
}}
.ob-icon {{ font-size: 4rem; margin-bottom: 1.2rem; line-height: 1; }}
.ob-title {{
    font-size: 1.9rem; font-weight: 800;
    color: #1a1a2e; letter-spacing: -0.5px;
    margin: 0 0 0.6rem; line-height: 1.2;
}}
.ob-title span {{ color: {acc}; }}
.ob-desc {{
    font-size: 0.95rem; color: rgba(0,0,0,0.45);
    line-height: 1.7; margin: 0 0 2rem; font-weight: 400;
}}
.dots {{
    display: flex; justify-content: center; gap: 8px; margin-bottom: 1.5rem;
}}
.dot {{
    width: 8px; height: 8px; border-radius: 50%;
    background: rgba(0,0,0,0.12); transition: all 0.3s ease;
}}
.dot.active {{
    width: 24px; border-radius: 99px;
    background: {acc};
}}

.stButton > button {{
    background: {acc} !important;
    border: none !important; border-radius: 14px !important;
    color: white !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 0.75rem !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.3) !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important; transform: translateY(-2px) !important;
}}

.skip-btn > div > button {{
    background: transparent !important;
    border: none !important;
    color: rgba(0,0,0,0.3) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    width: auto !important;
    padding: 0.3rem 0.5rem !important;
}}
.skip-btn > div > button:hover {{
    color: rgba(0,0,0,0.5) !important;
    transform: none !important;
    background: transparent !important;
}}
</style>
""", unsafe_allow_html=True)

steps = [
    {
        "icon": "🍱",
        "title": "Welcome to <span>AhaLaor AI</span>",
        "desc": "Your smart food companion. Scan any meal and instantly get the food name, calories, and full nutrition breakdown — in English or Khmer."
    },
    {
        "icon": "📸",
        "title": "Snap. <span>Scan.</span> Know.",
        "desc": "Just upload a photo of your food, optionally tell us more about it, then hit Scan. Our AI powered by Gemini identifies everything in seconds."
    },
    {
        "icon": "📊",
        "title": "Track your <span>Goals</span>",
        "desc": "Set a daily calorie goal, rate your meals as 🟢 Healthy, 🟡 Okay or 🔴 Indulgent, and view your full scan history. Stay on top of what you eat every day."
    },
]

step = st.session_state.onboarding_step
s = steps[step]

# Skip button
st.markdown('<div class="skip-btn">', unsafe_allow_html=True)
if st.button("Skip →"):
    st.session_state.onboarding_done = True
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# Dots
dots_html = '<div class="dots">' + "".join(
    f'<div class="dot {"active" if i == step else ""}"></div>'
    for i in range(len(steps))
) + '</div>'

st.markdown(f"""
<div class="frost ob-card">
    <div class="ob-icon">{s["icon"]}</div>
    <div class="ob-title">{s["title"]}</div>
    <div class="ob-desc">{s["desc"]}</div>
    {dots_html}
</div>
""", unsafe_allow_html=True)

if step < len(steps) - 1:
    if st.button("Next →"):
        st.session_state.onboarding_step += 1
        st.rerun()
else:
    if st.button("Get Started 🚀"):
        st.session_state.onboarding_done = True
        st.session_state.onboarding_step = 0
        st.switch_page("app.py")
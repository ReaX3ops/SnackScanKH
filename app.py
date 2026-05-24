import streamlit as st
from google import genai
from PIL import Image
import json
import time
import firebase_admin
from firebase_admin import credentials, firestore as fs
from datetime import datetime, date

st.set_page_config(
    page_title="AhaLaor AI",
    page_icon="favicon.png",
    layout="centered"
)

for k, v in {
    "lang": "en",
    "result": None,
    "image": None,
    "accent": "#7c3aed",
    "bg": "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)",
    "bg_custom": "#dde8f5",
    "show_settings": False,
    "onboarding_done": False,
    "cal_goal": 2000,
    "cal_today": 0,
    "cal_date": "",
    "last_rating": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def t(en, km):
    return km if st.session_state.lang == "km" else en

acc = st.session_state.accent
bg  = st.session_state.bg

# ── Firestore ──
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        fa = dict(st.secrets["firebase_admin"])
        fa["private_key"] = fa["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fa)
        firebase_admin.initialize_app(cred)
    return fs.client()

db = get_db()

# ── Onboarding check ──
if st.session_state.get("user") and not st.session_state.get("onboarding_done"):
    uid = st.session_state.user["uid"]
    try:
        doc = db.collection("users").document(uid).get()
        if not doc.exists or not doc.to_dict().get("onboarding_done"):
            db.collection("users").document(uid).set({"onboarding_done": True}, merge=True)
            st.session_state.onboarding_done = True
            st.switch_page("pages/onboarding.py")
    except:
        pass
    st.session_state.onboarding_done = True

# ── Daily calorie reset ──
today = str(date.today())
if st.session_state.cal_date != today:
    st.session_state.cal_today = 0
    st.session_state.cal_date  = today

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {bg} !important;
}}
.stApp {{
    background: {bg} !important;
    min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    padding-top: 1.5rem !important;
    max-width: 680px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}}

.frost {{
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(40px) saturate(200%) brightness(105%);
    -webkit-backdrop-filter: blur(40px) saturate(200%) brightness(105%);
    border: 1px solid rgba(255,255,255,0.85);
    box-shadow:
        0 2px 0 rgba(255,255,255,0.9) inset,
        0 -1px 0 rgba(0,0,0,0.04) inset,
        0 20px 60px rgba(0,0,0,0.07),
        0 4px 16px rgba(0,0,0,0.04);
    border-radius: 28px;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px) scale(0.98); }}
    to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes shimmerLine {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(400%); }}
}}

.navbar {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.75rem 1.4rem; margin-bottom: 1.2rem;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    position: relative; overflow: hidden;
}}
.navbar::before {{
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}
.nav-title {{ font-size: 1.05rem; font-weight: 800; color: #1a1a2e; letter-spacing: -0.4px; }}
.nav-title span {{ color: {acc}; }}

.stButton > button {{
    background: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    color: rgba(0,0,0,0.5) !important;
    border-radius: 99px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important; font-size: 0.84rem !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05), 0 1px 0 rgba(255,255,255,0.9) inset !important;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1) !important;
}}
.stButton > button:hover {{
    background: rgba(255,255,255,0.85) !important;
    border-color: rgba(124,58,237,0.25) !important;
    color: {acc} !important;
    transform: translateY(-2px) scale(1.02) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.09), 0 1px 0 rgba(255,255,255,0.9) inset !important;
}}
.stButton > button:active {{ transform: translateY(0) scale(0.98) !important; }}

div.scan-btn > div > button {{
    background: {acc} !important;
    border: none !important; border-radius: 18px !important;
    color: white !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.2) inset, 0 8px 28px rgba(124,58,237,0.35) !important;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1) !important;
    backdrop-filter: none !important;
}}
div.scan-btn > div > button:hover {{
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.2) inset, 0 12px 36px rgba(124,58,237,0.45) !important;
}}

.g-card {{
    padding: 1.5rem 1.8rem; margin-bottom: 0.9rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.55s cubic-bezier(0.34,1.56,0.64,1) both;
}}
.g-card::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}
.g-card::after {{
    content: ''; position: absolute; inset: 0; border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.35) 0%, transparent 55%);
    pointer-events: none;
}}
.g-card-accent {{ border-left: 3px solid {acc} !important; }}
.g-card-green  {{ border-left: 3px solid #10b981 !important; }}

.chip-label {{
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: {acc}; margin-bottom: 0.45rem; display: block; opacity: 0.7;
}}
.chip-label-green {{ color: #10b981; opacity: 1; }}

.food-name {{ font-size: 1.95rem; font-weight: 700; color: #1a1a2e; letter-spacing: -0.5px; line-height: 1.2; }}
.cal-number {{ font-size: 3.2rem; font-weight: 800; color: #10b981; letter-spacing: -2px; line-height: 1; }}
.cal-unit {{ font-size: 0.95rem; color: rgba(0,0,0,0.28); margin-left: 5px; font-weight: 300; }}

.nut-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; margin-top: 0.9rem; }}
.nut-cell {{
    background: rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px; padding: 1rem 0.4rem; text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.9) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
}}
.nut-cell:hover {{
    background: rgba(255,255,255,0.82); transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 28px rgba(0,0,0,0.09), 0 1px 0 rgba(255,255,255,0.9) inset;
}}
.nut-icon {{ font-size: 1.4rem; line-height: 1; }}
.nut-val {{ font-size: 1.05rem; font-weight: 700; color: #1a1a2e; margin: 5px 0 3px; }}
.nut-name {{ font-size: 0.58rem; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(0,0,0,0.32); }}

.tag-wrap {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 0.75rem; }}
.tag {{
    background: rgba(255,255,255,0.55); border: 1px solid rgba(255,255,255,0.8);
    border-radius: 99px; padding: 6px 16px; font-size: 0.83rem; color: rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.9) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
}}
.tag:hover {{ background: rgba(255,255,255,0.9); color: {acc}; transform: translateY(-2px); }}

.donut-wrap {{ display: flex; align-items: center; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap; }}
.donut-legend {{ display: flex; flex-direction: column; gap: 9px; }}
.legend-item {{ display: flex; align-items: center; gap: 9px; font-size: 0.83rem; color: rgba(0,0,0,0.5); }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.legend-pct {{ font-weight: 700; color: #1a1a2e; margin-left: auto; padding-left: 12px; }}

[data-testid="stFileUploadDropzone"] {{
    background: rgba(255,255,255,0.4) !important;
    border: 1.5px dashed rgba(255,255,255,0.7) !important;
    border-radius: 20px !important; backdrop-filter: blur(20px) !important;
    transition: all 0.25s ease !important;
}}
[data-testid="stFileUploadDropzone"]:hover {{
    background: rgba(255,255,255,0.65) !important;
    border-color: rgba(124,58,237,0.4) !important;
}}
[data-testid="stFileUploadDropzone"] p {{ color: rgba(0,0,0,0.28) !important; }}

[data-testid="stImage"] img {{
    border-radius: 22px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
}}

.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.88) !important;
    border-radius: 14px !important; color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: all 0.2s ease !important; padding: 0.65rem 1rem !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(0,0,0,0.22) !important; }}
.stTextInput > div > div > input:focus {{
    border-color: rgba(124,58,237,0.4) !important;
    background: rgba(255,255,255,0.88) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 0 0 3px rgba(124,58,237,0.1) !important;
}}
.stTextInput label {{
    color: rgba(0,0,0,0.38) !important; font-size: 0.67rem !important;
    font-weight: 700 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}}

.stNumberInput > div > div > input {{
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.88) !important;
    border-radius: 14px !important; color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    backdrop-filter: blur(20px) !important;
}}

.stProgress > div > div {{ background: {acc} !important; border-radius: 99px !important; transition: width 0.4s ease !important; }}
.stProgress > div {{ background: rgba(255,255,255,0.45) !important; border-radius: 99px !important; height: 5px !important; }}

.stAlert {{
    background: rgba(255,245,245,0.75) !important;
    border: 1px solid rgba(254,226,226,0.85) !important;
    border-radius: 16px !important; color: #dc2626 !important;
    backdrop-filter: blur(16px) !important;
}}

.settings-wrap {{
    padding: 1.8rem 2rem 2rem; margin-bottom: 1rem;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    position: relative; overflow: hidden;
}}
.settings-wrap::before {{
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}
.settings-title {{ font-size: 1.1rem; font-weight: 700; color: #1a1a2e; margin: 0 0 1.4rem; }}
.settings-section {{
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: rgba(0,0,0,0.28); margin-bottom: 0.8rem; display: block;
}}
.gradient-swatch {{
    height: 54px; border-radius: 16px;
    border: 2px solid rgba(255,255,255,0.85); cursor: pointer;
    box-shadow: 0 3px 12px rgba(0,0,0,0.09), 0 1px 0 rgba(255,255,255,0.6) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 600; color: rgba(0,0,0,0.5); margin-bottom: 4px;
}}
.gradient-swatch:hover {{ transform: translateY(-4px) scale(1.02); box-shadow: 0 10px 24px rgba(0,0,0,0.13); }}
.gradient-swatch.active {{ border-color: {acc} !important; box-shadow: 0 0 0 3px rgba(124,58,237,0.18), 0 8px 24px rgba(0,0,0,0.12); }}
.s-divider {{ height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.7), transparent); margin: 1.3rem 0; }}
.preview-bar {{ height: 5px; border-radius: 99px; margin: 0.8rem auto 0; max-width: 160px; transition: background 0.35s ease; }}

[data-testid="stColorPicker"] {{ display: flex; justify-content: center; }}
[data-testid="stColorPicker"] > div {{
    width: 58px !important; height: 58px !important; border-radius: 50% !important;
    border: 3px solid rgba(255,255,255,0.9) !important; overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important; cursor: pointer !important;
    transition: transform 0.2s !important;
}}
[data-testid="stColorPicker"] > div:hover {{ transform: scale(1.1) !important; }}

.rating-card {{
    padding: 1.4rem 1.8rem; margin-bottom: 0.9rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.55s cubic-bezier(0.34,1.56,0.64,1) both;
    text-align: center;
}}
.cal-goal-card {{
    padding: 1.4rem 1.8rem; margin-bottom: 0.9rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.55s cubic-bezier(0.34,1.56,0.64,1) both;
}}

.page-footer {{
    text-align: center; margin-top: 2.5rem; padding-bottom: 1.2rem;
    font-size: 0.72rem; color: rgba(0,0,0,0.22); letter-spacing: 0.3px;
}}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# ── Navbar ──
# ══════════════════════════════════════
col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])

with col1:
    try:
        ic, tx = st.columns([1, 5])
        with ic:
            st.image("favicon.png", width=34)
        with tx:
            st.markdown(f"""
            <div style="display:flex;align-items:center;height:100%;margin-top:2px;">
                <span class="nav-title">AhaLaor <span>AI</span></span>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f'<span class="nav-title">AhaLaor <span style="color:{acc};">AI</span></span>', unsafe_allow_html=True)

with col2:
    if st.button("📋", help="Scan History"):
        st.switch_page("pages/history.py")

with col3:
    if st.button("⚙️", help="Settings"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

with col4:
    if st.button("🇰🇭" if st.session_state.lang == "en" else "🇬🇧"):
        st.session_state.lang = "km" if st.session_state.lang == "en" else "en"
        st.rerun()

with col5:
    if st.session_state.get("user"):
        email_short = st.session_state.user.get("email", "").split("@")[0]
        if st.button(f"👤", help=f"Signed in as {email_short} — click to sign out"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔐", help="Sign In"):
            st.switch_page("pages/login.py")

# ══════════════════════════════════════
# ── Settings panel ──
# ══════════════════════════════════════
if st.session_state.show_settings:
    st.markdown('<div class="frost settings-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="settings-title">⚙️ Settings</div>', unsafe_allow_html=True)

    st.markdown('<span class="settings-section">✦ Background</span>', unsafe_allow_html=True)
    gradients = {
        "🫐 Frost":    "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)",
        "🌸 Blush":    "linear-gradient(135deg, #fde8f0 0%, #fdf2fb 40%, #f0e8fd 100%)",
        "🌿 Sage":     "linear-gradient(135deg, #d8f0e8 0%, #eefbf2 40%, #e8f5d8 100%)",
        "🌅 Sunset":   "linear-gradient(135deg, #fde8d8 0%, #fdf5eb 40%, #fdf0d8 100%)",
        "🌊 Ocean":    "linear-gradient(135deg, #d8eef5 0%, #ebf7fd 40%, #d8e8f5 100%)",
        "🌑 Midnight": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
    }
    cols = st.columns(3)
    for i, (name, grad) in enumerate(gradients.items()):
        with cols[i % 3]:
            active = "active" if st.session_state.bg == grad else ""
            st.markdown(f'<div class="gradient-swatch {active}" style="background:{grad};">{name}</div>', unsafe_allow_html=True)
            if st.button("✓" if st.session_state.bg == grad else "Select", key=f"grad_{name}"):
                st.session_state.bg = grad
                st.rerun()

    st.markdown('<div class="s-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="settings-section">✦ Custom Background</span>', unsafe_allow_html=True)
    picked_bg = st.color_picker("bg", value=st.session_state.bg_custom, label_visibility="collapsed", key="bg_picker")
    if picked_bg != st.session_state.bg_custom:
        st.session_state.bg_custom = picked_bg
        st.session_state.bg = f"linear-gradient(135deg, {picked_bg} 0%, {picked_bg}dd 50%, {picked_bg}bb 100%)"
        st.rerun()
    st.markdown(f'<div class="preview-bar" style="background:{picked_bg};"></div>', unsafe_allow_html=True)

    st.markdown('<div class="s-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="settings-section">✦ Accent Color</span>', unsafe_allow_html=True)
    accent_options = {
        "🟣 Purple":  "#7c3aed",
        "🔵 Cyan":    "#0ea5e9",
        "🟠 Sunset":  "#f97316",
        "🟢 Emerald": "#10b981",
        "🩷 Pink":    "#ec4899",
        "🟡 Gold":    "#f59e0b",
    }
    acols = st.columns(len(accent_options))
    for col, (name, hex_val) in zip(acols, accent_options.items()):
        with col:
            label = "✓" if st.session_state.accent == hex_val else name.split()[0]
            if st.button(label, key=f"acc_{hex_val}", help=name):
                st.session_state.accent = hex_val
                st.rerun()

    st.markdown('<div class="s-divider"></div>', unsafe_allow_html=True)
    st.markdown('<span class="settings-section">✦ Daily Calorie Goal</span>', unsafe_allow_html=True)
    new_goal = st.number_input(
        "Daily calorie goal (kcal)",
        min_value=500, max_value=5000,
        value=int(st.session_state.cal_goal),
        step=50, label_visibility="collapsed"
    )
    if new_goal != st.session_state.cal_goal:
        st.session_state.cal_goal = new_goal
        st.rerun()
    st.markdown(f'<div style="font-size:0.78rem;color:rgba(0,0,0,0.35);text-align:center;margin-top:0.4rem;">Current goal: {int(st.session_state.cal_goal)} kcal/day</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# ── Hero ──
# ══════════════════════════════════════
st.markdown(f"""
<div class="frost" style="
    text-align: center; padding: 2.2rem 2rem 2rem;
    margin-bottom: 1.2rem; position: relative; overflow: hidden;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
">
    <div style="position:absolute;top:0;left:-100%;width:300%;height:1px;
        background:linear-gradient(90deg,transparent,rgba(255,255,255,0.95),transparent);
        animation:shimmerLine 4s linear infinite;"></div>
    <div style="display:inline-block;background:rgba(255,255,255,0.4);
        border:1px solid rgba(255,255,255,0.6);border-radius:99px;padding:3px 16px;
        font-size:0.68rem;font-weight:600;letter-spacing:2px;text-transform:uppercase;
        color:#888;margin-bottom:0.7rem;backdrop-filter:blur(8px);">
        AI Powered · Cambodia 🇰🇭
    </div>
    <div style="font-size:2.6rem;font-weight:800;letter-spacing:-1.5px;color:#1a1a2e;
        margin:0 0 0.3rem;line-height:1;">
        AhaLaor <span style="color:{acc};">AI</span>
    </div>
    <div style="font-size:1rem;font-weight:500;color:rgba(0,0,0,0.3);margin:0 0 0.4rem;">
        អាហារល្អ
    </div>
    <div style="font-size:0.88rem;color:rgba(0,0,0,0.35);font-weight:400;margin:0;">
        {t("Snap a photo. Know your food.", "ថតរូបភាព។ ស្គាល់ម្ហូបរបស់អ្នក។")}
    </div>
</div>
""", unsafe_allow_html=True)

# ── Calorie Goal Ring (top of page) ──
if st.session_state.get("user"):
    goal    = st.session_state.cal_goal
    current = st.session_state.cal_today
    pct     = min(current / goal, 1.0) if goal > 0 else 0
    color   = "#10b981" if pct < 0.75 else "#f59e0b" if pct < 1.0 else "#ef4444"
    remaining = max(goal - current, 0)

    st.markdown(f"""
    <div class="frost cal-goal-card">
        <span class="chip-label">🎯 {t("Today's Calorie Goal", "គោលដៅកាឡូរីថ្ងៃនេះ")}</span>
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.6rem;">
            <span style="font-size:1.4rem;font-weight:800;color:{color};">{int(current)} kcal</span>
            <span style="font-size:0.82rem;color:rgba(0,0,0,0.35);">Goal: {int(goal)} kcal</span>
        </div>
        <div style="background:rgba(0,0,0,0.06);border-radius:99px;height:10px;overflow:hidden;">
            <div style="width:{pct*100:.1f}%;height:100%;background:{color};border-radius:99px;transition:width 0.5s ease;"></div>
        </div>
        <div style="font-size:0.75rem;color:rgba(0,0,0,0.3);margin-top:0.4rem;text-align:right;">
            {int(remaining)} kcal remaining · Change goal in ⚙️
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# ── Gemini client ──
# ══════════════════════════════════════
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# ══════════════════════════════════════
# ── Upload ──
# ══════════════════════════════════════
uploaded_file = st.file_uploader(
    t("Drop your food photo here", "ទម្លាក់រូបភាពម្ហូបរបស់អ្នក"),
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

hint = st.text_input(
    t("TELL US MORE (OPTIONAL)", "បញ្ជាក់បន្ថែម (ជាជម្រើស)"),
    placeholder=t('e.g. "whole milk", "brown rice"', 'ឧ. "ទឹកដោះគោ", "បាយស្វាយចន្ទី"')
)

if uploaded_file:
    img = Image.open(uploaded_file)
    st.session_state.image = img
    st.image(img, use_container_width=True)

    st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
    scan_clicked = st.button(t("🔍   Scan Food", "🔍   វិភាគម្ហូប"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    scan_placeholder = st.empty()

    if scan_clicked:
        if not st.session_state.get("user"):
            st.switch_page("pages/login.py")
            st.stop()

        st.session_state.result = None
        st.session_state.last_rating = None
        scan_placeholder.empty()
        bar = st.progress(0, text=t("Waking up the AI...", "កំពុងភ្ញាក់ AI..."))
        steps = [
            (15, t("Reading your photo...",      "កំពុងអានរូបភាព...")),
            (35, t("Identifying the food...",    "កំពុងកំណត់ម្ហូប...")),
            (58, t("Calculating calories...",    "កំពុងគណនាកាឡូរី...")),
            (78, t("Breaking down nutrition...", "កំពុងវិភាគជីវជាតិ...")),
            (92, t("Wrapping up results...",     "កំពុងបញ្ចប់លទ្ធផល...")),
        ]
        for pct, msg in steps:
            time.sleep(0.35)
            bar.progress(pct, text=msg)

        hint_clause = f'The user says this is: "{hint}". Use this to improve accuracy.' if hint.strip() else ""
        prompt = f"""Analyze the food image. {hint_clause}

Return ONLY a JSON object, no markdown, no explanation:

{{
  "food_en": "food name in English",
  "food_km": "food name in Khmer",
  "calories": "estimated total calories as number only",
  "ingredients_en": ["ingredient1", "ingredient2", "ingredient3"],
  "ingredients_km": ["ingredient1 in Khmer", "ingredient2 in Khmer", "ingredient3 in Khmer"],
  "nutrition": {{
    "protein": "Xg",
    "carbs": "Xg",
    "fat": "Xg",
    "fiber": "Xg",
    "sugar": "Xg",
    "sodium": "Xmg"
  }}
}}"""

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, st.session_state.image]
            )
            text = response.text.replace("```json", "").replace("```", "").strip()
            st.session_state.result = json.loads(text)
            bar.progress(100, text=t("Done! ✅", "រួចរាល់! ✅"))
            time.sleep(0.4)
            bar.empty()
        except Exception as e:
            bar.empty()
            st.error(f"Error: {e}")

# ══════════════════════════════════════
# ── Results ──
# ══════════════════════════════════════
if st.session_state.result and st.session_state.image:
    data = st.session_state.result
    lang = st.session_state.lang
    food        = data.get("food_km" if lang == "km" else "food_en", "Unknown")
    calories    = str(data.get("calories", "?"))
    nutrition   = data.get("nutrition", {})
    ing_key     = "ingredients_km" if lang == "km" else "ingredients_en"
    ignore      = ["bun", "bread", "beef patty"]
    ingredients = [i for i in data.get(ing_key, []) if i.lower() not in ignore]

    st.markdown(f"""
    <div class="frost g-card g-card-accent">
        <span class="chip-label">🍽 {t("Detected Food", "ម្ហូបដែលបានរកឃើញ")}</span>
        <div class="food-name">{food}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="frost g-card g-card-green">
        <span class="chip-label chip-label-green">🔥 {t("Estimated Calories", "កាឡូរីដែលប៉ាន់ស្មាន")}</span>
        <div><span class="cal-number">{calories}</span><span class="cal-unit">kcal</span></div>
    </div>""", unsafe_allow_html=True)

    if nutrition:
        items = [
            ("💪", t("Protein", "ប្រូតេអ៊ីន"),  nutrition.get("protein", "–")),
            ("🍞", t("Carbs",   "កាបូអ៊ីដ្រាត"), nutrition.get("carbs",   "–")),
            ("🧈", t("Fat",     "ខ្លាញ់"),        nutrition.get("fat",     "–")),
            ("🌿", t("Fiber",   "ជាតិសរសៃ"),      nutrition.get("fiber",   "–")),
            ("🍬", t("Sugar",   "ស្ករ"),          nutrition.get("sugar",   "–")),
            ("🧂", t("Sodium",  "អំបិល"),         nutrition.get("sodium",  "–")),
        ]
        cells = "".join(f"""<div class="nut-cell">
            <div class="nut-icon">{icon}</div>
            <div class="nut-val">{val}</div>
            <div class="nut-name">{name}</div>
        </div>""" for icon, name, val in items)
        st.markdown(f"""
        <div class="frost g-card">
            <span class="chip-label">🧬 {t("Nutrition Breakdown", "តម្លៃអាហារូបត្ថម្ភ")}</span>
            <div class="nut-grid">{cells}</div>
        </div>""", unsafe_allow_html=True)

    if nutrition:
        def parse_g(val):
            try:
                return float(''.join(c for c in str(val) if c.isdigit() or c == '.'))
            except:
                return 0.0

        macro_cals = {
            t("Protein", "ប្រូតេអ៊ីន"):  parse_g(nutrition.get("protein", "0")) * 4,
            t("Carbs",   "កាបូអ៊ីដ្រាត"): parse_g(nutrition.get("carbs",   "0")) * 4,
            t("Fat",     "ខ្លាញ់"):        parse_g(nutrition.get("fat",     "0")) * 9,
            t("Fiber",   "ជាតិសរសៃ"):      parse_g(nutrition.get("fiber",   "0")) * 2,
            t("Sugar",   "ស្ករ"):          parse_g(nutrition.get("sugar",   "0")) * 4,
        }
        total_cal = sum(macro_cals.values()) or 1
        colors = ["#7c3aed", "#34d399", "#f97316", "#60a5fa", "#f472b6"]
        slices = [(name, cal, colors[i]) for i, (name, cal) in enumerate(macro_cals.items()) if cal > 0]

        cx, cy, r, stroke = 90, 90, 70, 28
        circumference = 2 * 3.14159 * r
        segments, offset = [], 0
        for name, cal, color in slices:
            dash = (cal / total_cal) * circumference
            gap  = circumference - dash
            segments.append(
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" '
                f'stroke-width="{stroke}" stroke-dasharray="{dash:.2f} {gap:.2f}" '
                f'stroke-dashoffset="{-offset:.2f}" transform="rotate(-90 {cx} {cy})"/>'
            )
            offset += dash

        svg = f"""<svg width="180" height="180" viewBox="0 0 180 180">
            <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="{stroke}"/>
            {''.join(segments)}
            <text x="{cx}" y="{cy-8}" text-anchor="middle" fill="#1a1a2e" font-size="13" font-weight="700" font-family="Outfit">{t("Macros","ម៉ាក្រូ")}</text>
            <text x="{cx}" y="{cy+10}" text-anchor="middle" fill="rgba(0,0,0,0.28)" font-size="10" font-family="Outfit">{t("breakdown","ចំណែក")}</text>
        </svg>"""

        legend = "".join(
            f'<div class="legend-item"><div class="legend-dot" style="background:{c}"></div>'
            f'<span>{n}</span><span class="legend-pct">{cal/total_cal*100:.0f}%</span></div>'
            for n, cal, c in slices
        )
        st.markdown(f"""
        <div class="frost g-card">
            <span class="chip-label">🥧 {t("Macro Wheel", "កង់ម៉ាក្រូ")}</span>
            <div class="donut-wrap">{svg}<div class="donut-legend">{legend}</div></div>
        </div>""", unsafe_allow_html=True)

    if ingredients:
        tags = "".join(f'<span class="tag">{i}</span>' for i in ingredients)
        st.markdown(f"""
        <div class="frost g-card">
            <span class="chip-label">🥬 {t("Ingredients", "គ្រឿងផ្សំ")}</span>
            <div class="tag-wrap">{tags}</div>
        </div>""", unsafe_allow_html=True)

    # ── Meal Rating ──
    if not st.session_state.last_rating:
        st.markdown(f"""
        <div class="frost rating-card">
            <span class="chip-label" style="text-align:center;display:block;">
                ✦ {t("Rate this meal", "វាយតម្លៃអាហារនេះ")}
            </span>
        </div>
        """, unsafe_allow_html=True)

        rc1, rc2, rc3 = st.columns(3)
        rating = None
        with rc1:
            if st.button("🟢 Healthy", use_container_width=True, key="rate_healthy"):
                rating = "healthy"
        with rc2:
            if st.button("🟡 Okay", use_container_width=True, key="rate_okay"):
                rating = "okay"
        with rc3:
            if st.button("🔴 Indulgent", use_container_width=True, key="rate_indulgent"):
                rating = "indulgent"

        if rating:
            st.session_state.last_rating = rating
            # Save to Firestore
            try:
                cal_val = float(''.join(c for c in str(data.get("calories","0")) if c.isdigit() or c == '.'))
                db.collection("scans").add({
                    "uid":       st.session_state.user["uid"],
                    "food":      data.get("food_en", "Unknown"),
                    "calories":  data.get("calories", "0"),
                    "rating":    rating,
                    "timestamp": datetime.utcnow(),
                    "nutrition": data.get("nutrition", {}),
                })
                st.session_state.cal_today += cal_val
                emoji = "🟢" if rating == "healthy" else "🟡" if rating == "okay" else "🔴"
                st.success(f"Saved as {emoji} {rating.capitalize()}! +{int(cal_val)} kcal added to today's total.")
                st.rerun()
            except Exception as e:
                st.error(f"Could not save: {e}")
    else:
        emoji = "🟢" if st.session_state.last_rating == "healthy" else "🟡" if st.session_state.last_rating == "okay" else "🔴"
        st.markdown(f"""
        <div class="frost rating-card">
            <span style="font-size:1.5rem;">{emoji}</span>
            <span style="font-size:0.9rem;color:rgba(0,0,0,0.45);margin-left:8px;">
                Rated as {st.session_state.last_rating.capitalize()} · Saved to history ✅
            </span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="page-footer">AhaLaor AI · Made with ♥ in Phnom Penh</div>', unsafe_allow_html=True)
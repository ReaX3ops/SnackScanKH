import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
from datetime import datetime

st.set_page_config(page_title="History · AhaLaor AI", page_icon="favicon.png", layout="centered")

if not st.session_state.get("user"):
    st.switch_page("pages/login.py")
    st.stop()

acc = st.session_state.get("accent", "#7c3aed")
bg  = st.session_state.get("bg", "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}
.stApp, html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {bg} !important; min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2rem; max-width: 680px; }}

.frost {{
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(40px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.85);
    box-shadow: 0 20px 60px rgba(0,0,0,0.07), 0 2px 0 rgba(255,255,255,0.9) inset;
    border-radius: 24px;
}}

@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(16px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}

.page-title {{
    font-size: 1.8rem; font-weight: 800;
    color: #1a1a2e; letter-spacing: -0.5px;
    margin: 0 0 0.3rem;
}}
.page-title span {{ color: {acc}; }}
.page-sub {{ font-size: 0.88rem; color: rgba(0,0,0,0.35); margin: 0 0 1.5rem; }}

.history-card {{
    padding: 1.2rem 1.6rem;
    margin-bottom: 0.8rem;
    animation: fadeUp 0.4s ease both;
    display: flex; align-items: center; gap: 1rem;
}}
.h-icon {{ font-size: 2rem; flex-shrink: 0; }}
.h-info {{ flex: 1; }}
.h-food {{ font-size: 1rem; font-weight: 700; color: #1a1a2e; }}
.h-cal {{ font-size: 0.82rem; color: rgba(0,0,0,0.4); margin-top: 2px; }}
.h-date {{ font-size: 0.75rem; color: rgba(0,0,0,0.28); margin-top: 2px; }}
.h-rating {{ font-size: 1.4rem; flex-shrink: 0; }}
.h-cal-badge {{
    font-size: 0.88rem; font-weight: 700;
    color: #10b981; flex-shrink: 0;
}}

.empty-state {{
    text-align: center; padding: 3rem 2rem;
}}
.empty-icon {{ font-size: 3rem; margin-bottom: 0.8rem; }}
.empty-title {{ font-size: 1.1rem; font-weight: 700; color: #1a1a2e; }}
.empty-sub {{ font-size: 0.88rem; color: rgba(0,0,0,0.35); margin-top: 0.3rem; }}

.stButton > button {{
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    color: rgba(0,0,0,0.5) !important;
    border-radius: 99px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    background: rgba(255,255,255,0.9) !important;
    color: {acc} !important;
    border-color: {acc} !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Init Firestore ──
@st.cache_resource
def get_db():
    if not firebase_admin._apps:
        fa = dict(st.secrets["firebase_admin"])
        fa["private_key"] = fa["private_key"].replace("\\n", "\n")
        cred = credentials.Certificate(fa)
        firebase_admin.initialize_app(cred)
    return firestore.client()

db = get_db()

# ── Header ──
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"""
    <div class="page-title">Scan <span>History</span></div>
    <div class="page-sub">Your past food scans</div>
    """, unsafe_allow_html=True)
with col2:
    if st.button("← Back"):
        st.switch_page("app.py")

# ── Load history ──
uid = st.session_state.user["uid"]
try:
    docs = db.collection("scans").where("uid", "==", uid)\
             .order_by("timestamp", direction=firestore.Query.DESCENDING)\
             .limit(50).stream()
    scans = [doc.to_dict() for doc in docs]
except Exception as e:
    scans = []
    st.error(f"Error loading history: {e}")

if not scans:
    st.markdown("""
    <div class="frost empty-state">
        <div class="empty-icon">🍽️</div>
        <div class="empty-title">No scans yet</div>
        <div class="empty-sub">Start scanning food to see your history here</div>
    </div>
    """, unsafe_allow_html=True)
else:
    rating_emoji = {"healthy": "🟢", "okay": "🟡", "indulgent": "🔴", None: "⚪"}

    for scan in scans:
        food    = scan.get("food", "Unknown")
        cal     = scan.get("calories", "?")
        rating  = scan.get("rating", None)
        ts      = scan.get("timestamp")
        date_str = ts.strftime("%b %d, %Y · %I:%M %p") if ts else ""

        st.markdown(f"""
        <div class="frost history-card">
            <div class="h-icon">🍱</div>
            <div class="h-info">
                <div class="h-food">{food}</div>
                <div class="h-cal">🔥 {cal} kcal</div>
                <div class="h-date">{date_str}</div>
            </div>
            <div class="h-cal-badge">{cal}</div>
            <div class="h-rating">{rating_emoji.get(rating, "⚪")}</div>
        </div>
        """, unsafe_allow_html=True)
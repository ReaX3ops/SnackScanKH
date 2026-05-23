import streamlit as st
import pyrebase

st.set_page_config(page_title="Sign In · SnackScanKH", page_icon="🔐", layout="centered")

firebase_config = {
    "apiKey":            st.secrets["firebase"]["apiKey"],
    "authDomain":        st.secrets["firebase"]["authDomain"],
    "projectId":         st.secrets["firebase"]["projectId"],
    "storageBucket":     st.secrets["firebase"]["storageBucket"],
    "messagingSenderId": st.secrets["firebase"]["messagingSenderId"],
    "appId":             st.secrets["firebase"]["appId"],
    "databaseURL":       st.secrets["firebase"]["databaseURL"],
}

firebase = pyrebase.initialize_app(firebase_config)
auth     = firebase.auth()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user:
    st.switch_page("app.py")
    st.stop()

acc = st.session_state.get("accent", "#7c3aed")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}

.stApp {{
    background: linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%);
    min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 3.5rem; max-width: 460px; }}

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

.auth-card {{
    padding: 2.2rem 2.2rem 1.8rem;
    text-align: center;
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}}
.auth-card::before {{
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
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(124,58,237,0.07) 0%, transparent 70%);
    top: -60px; left: -60px;
    animation: floatOrb 6s ease-in-out infinite;
}}
.orb2 {{
    width: 140px; height: 140px;
    background: radial-gradient(circle, rgba(14,165,233,0.06) 0%, transparent 70%);
    bottom: -40px; right: -40px;
    animation: floatOrb 8s ease-in-out infinite reverse;
}}
.auth-icon {{ font-size: 2rem; margin-bottom: 0.4rem; }}
.auth-title {{
    font-size: 1.5rem; font-weight: 800; color: #1a1a2e;
    letter-spacing: -0.5px; margin: 0 0 0.25rem; line-height: 1.25;
}}
.auth-title span {{ color: {acc}; }}
.auth-sub {{ font-size: 0.83rem; color: rgba(0,0,0,0.35); margin: 0; }}

.success-box {{
    background: rgba(240,253,244,0.8);
    border: 1px solid rgba(187,247,208,0.9);
    border-radius: 14px; padding: 0.85rem 1rem;
    color: #16a34a; font-size: 0.88rem; margin-bottom: 0.8rem;
    backdrop-filter: blur(8px); text-align: left;
    animation: fadeUp 0.3s ease both;
}}
.error-box {{
    background: rgba(255,245,245,0.8);
    border: 1px solid rgba(254,226,226,0.9);
    border-radius: 14px; padding: 0.85rem 1rem;
    color: #dc2626; font-size: 0.88rem; margin-bottom: 0.8rem;
    backdrop-filter: blur(8px); text-align: left;
    animation: fadeUp 0.3s ease both;
}}

/* ── Inputs ── */
.stTextInput {{ margin-bottom: 0.6rem; }}
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.55) !important;
    border: 1.5px solid rgba(255,255,255,0.75) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 0.9rem !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.25s !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {acc} !important;
    background: rgba(255,255,255,0.85) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(0,0,0,0.25) !important; }}
.stTextInput label {{
    color: rgba(0,0,0,0.38) !important; font-size: 0.68rem !important;
    font-weight: 700 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
    margin-bottom: 0.3rem !important;
    display: block !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: {acc} !important;
    border: none !important; border-radius: 14px !important;
    color: white !important; font-size: 0.95rem !important;
    font-weight: 700 !important; width: 100% !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 0.65rem !important;
    box-shadow: 0 6px 20px rgba(124,58,237,0.28) !important;
    transition: all 0.25s !important;
    margin-top: 0.4rem !important;
}}
.stButton > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(124,58,237,0.38) !important;
}}

.back-btn > div > button {{
    background: rgba(255,255,255,0.5) !important;
    border: 1.5px solid rgba(255,255,255,0.75) !important;
    color: rgba(0,0,0,0.45) !important;
    border-radius: 99px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    width: auto !important;
    box-shadow: none !important;
    backdrop-filter: blur(12px) !important;
    margin-bottom: 1.2rem !important;
    margin-top: 0 !important;
    padding: 0.4rem 1.2rem !important;
}}
.back-btn > div > button:hover {{
    background: rgba(255,255,255,0.8) !important;
    border-color: {acc} !important;
    color: {acc} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.4) !important;
    border-radius: 14px !important; padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.65) !important;
    backdrop-filter: blur(16px) !important;
    gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; color: rgba(0,0,0,0.4) !important;
    padding: 0.4rem 1.2rem !important;
    transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(255,255,255,0.85) !important;
    color: {acc} !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

/* ── Background picker card ── */
.bg-card {{
    padding: 1.6rem 2rem 1.8rem;
    text-align: center;
    margin-top: 1rem;
    animation: fadeUp 0.6s ease 0.1s both;
}}
.section-label {{
    font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: rgba(0,0,0,0.3); margin-bottom: 1rem; display: block;
}}
.bg-swatches {{
    display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;
    margin-bottom: 1rem;
}}
.bg-swatch {{
    width: 40px; height: 40px; border-radius: 50%;
    border: 3px solid rgba(255,255,255,0.85);
    cursor: pointer;
    box-shadow: 0 3px 10px rgba(0,0,0,0.12);
    transition: transform 0.2s, box-shadow 0.2s;
    display: inline-block;
}}
.bg-swatch:hover {{ transform: scale(1.15); box-shadow: 0 5px 16px rgba(0,0,0,0.18); }}
</style>
""", unsafe_allow_html=True)

# ── Logo ──
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    try:
        st.image("SnackScan.jpg", width=68)
    except:
        pass

# ── Back button ──
st.markdown('<div class="back-btn">', unsafe_allow_html=True)
if st.button("← Back to SnackScanKH"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2 = st.tabs(["Sign In", "Create Account"])

with tab1:
    st.markdown(f"""
    <div class="glass auth-card">
        <div class="orb orb1"></div><div class="orb orb2"></div>
        <div class="auth-icon">🔐</div>
        <div class="auth-title">Welcome back to<br><span>SnackScanKH</span></div>
        <div class="auth-sub">Sign in to start scanning</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signin_form"):
        email    = st.text_input("EMAIL",    placeholder="you@example.com")
        password = st.text_input("PASSWORD", placeholder="••••••••", type="password")
        submitted = st.form_submit_button("Sign In →")

    if submitted:
        if not email or not password:
            st.markdown('<div class="error-box">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = {
                    "email": email,
                    "token": user["idToken"],
                    "uid":   user["localId"]
                }
                st.switch_page("app.py")
            except Exception:
                st.markdown('<div class="error-box">❌ Incorrect email or password.</div>', unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="glass auth-card">
        <div class="orb orb1"></div><div class="orb orb2"></div>
        <div class="auth-icon">👋</div>
        <div class="auth-title">Join<br><span>SnackScanKH</span></div>
        <div class="auth-sub">Create your free account</div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        new_email    = st.text_input("EMAIL",            placeholder="you@example.com")
        new_password = st.text_input("PASSWORD",         placeholder="Min. 6 characters", type="password")
        confirm_pass = st.text_input("CONFIRM PASSWORD", placeholder="••••••••",          type="password")
        submitted2   = st.form_submit_button("Create Account →")

    if submitted2:
        if not new_email or not new_password or not confirm_pass:
            st.markdown('<div class="error-box">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif new_password != confirm_pass:
            st.markdown('<div class="error-box">❌ Passwords don\'t match.</div>', unsafe_allow_html=True)
        elif len(new_password) < 6:
            st.markdown('<div class="error-box">❌ Password must be at least 6 characters.</div>', unsafe_allow_html=True)
        else:
            try:
                user = auth.create_user_with_email_and_password(new_email, new_password)
                st.session_state.user = {
                    "email": new_email,
                    "token": user["idToken"],
                    "uid":   user["localId"]
                }
                st.markdown('<div class="success-box">🎉 Welcome to SnackScanKH!</div>', unsafe_allow_html=True)
                st.switch_page("app.py")
            except Exception:
                st.markdown('<div class="error-box">❌ Email may already be in use.</div>', unsafe_allow_html=True)

# ── Background customizer ──
st.markdown("""
<div class="glass bg-card">
    <span class="section-label">✦ Background Style</span>
</div>
""", unsafe_allow_html=True)

bg_options = {
    "🫐 Frost":    "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)",
    "🌸 Blush":    "linear-gradient(135deg, #fde8f0 0%, #fdf2fb 40%, #f0e8fd 100%)",
    "🌿 Sage":     "linear-gradient(135deg, #d8f0e8 0%, #eefbf2 40%, #e8f5d8 100%)",
    "🌅 Sunset":   "linear-gradient(135deg, #fde8d8 0%, #fdf5eb 40%, #fdf0d8 100%)",
    "🌊 Ocean":    "linear-gradient(135deg, #d8eef5 0%, #ebf7fd 40%, #d8e8f5 100%)",
    "🌑 Midnight": "linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)",
}

if "bg" not in st.session_state:
    st.session_state.bg = "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)"

cols = st.columns(len(bg_options))
swatch_colors = ["#b8d4f0", "#f0b8d4", "#b8f0d4", "#f0d4b8", "#b8e8f5", "#1a1a2e"]
for col, ((name, grad), color) in zip(cols, zip(bg_options.items(), swatch_colors)):
    with col:
        if st.button(name.split()[0], key=f"bg_{name}", help=name):
            st.session_state.bg = grad
            st.rerun()

# Apply chosen background
st.markdown(f"""
<style>
.stApp {{
    background: {st.session_state.bg} !important;
}}
</style>
""", unsafe_allow_html=True)
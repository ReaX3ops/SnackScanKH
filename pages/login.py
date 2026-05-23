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
.stApp {{ background: #f7f7f7; min-height: 100vh; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 3rem; max-width: 460px; }}

.auth-card {{
    background: white;
    border-radius: 24px;
    padding: 2.5rem 2.2rem 2rem;
    border: 1px solid #ebebeb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04);
    text-align: center;
    margin-bottom: 1.2rem;
}}
.auth-icon {{ font-size: 2rem; margin-bottom: 0.5rem; }}
.auth-title {{
    font-size: 1.5rem; font-weight: 800; color: #111;
    letter-spacing: -0.5px; margin: 0 0 0.3rem; line-height: 1.2;
}}
.auth-title span {{ color: {acc}; }}
.auth-sub {{ font-size: 0.85rem; color: #aaa; margin: 0 0 0.2rem; }}

.success-box {{
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 12px; padding: 0.85rem 1rem;
    color: #16a34a; font-size: 0.88rem; margin-bottom: 0.8rem;
    text-align: left;
}}
.error-box {{
    background: #fff5f5; border: 1px solid #fee2e2;
    border-radius: 12px; padding: 0.85rem 1rem;
    color: #dc2626; font-size: 0.88rem; margin-bottom: 0.8rem;
    text-align: left;
}}

.stTextInput > div > div > input {{
    background: #fafafa !important;
    border: 1.5px solid #e8e8e8 !important;
    border-radius: 12px !important;
    color: #111 !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.93rem !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {acc} !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(0,0,0,0.04) !important;
}}
.stTextInput > div > div > input::placeholder {{ color: #ccc !important; }}
.stTextInput label {{
    color: #aaa !important; font-size: 0.68rem !important;
    font-weight: 700 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}}

.stButton > button {{
    background: {acc} !important;
    border: none !important; border-radius: 12px !important;
    color: white !important; font-size: 0.95rem !important;
    font-weight: 700 !important; width: 100% !important;
    font-family: 'Outfit', sans-serif !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
    transition: all 0.2s !important;
}}
.stButton > button:hover {{
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 18px rgba(0,0,0,0.12) !important;
}}

.back-btn > div > button {{
    background: white !important;
    border: 1.5px solid #e8e8e8 !important;
    color: #888 !important;
    border-radius: 99px !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    width: auto !important;
    box-shadow: none !important;
    margin-bottom: 1.2rem;
}}
.back-btn > div > button:hover {{
    border-color: {acc} !important;
    color: {acc} !important;
    opacity: 1 !important;
    transform: none !important;
    box-shadow: none !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: #f5f5f5 !important;
    border-radius: 12px !important; padding: 4px !important;
    border: 1px solid #ebebeb !important;
    gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; color: #999 !important;
    padding: 0.4rem 1.2rem !important;
}}
.stTabs [aria-selected="true"] {{
    background: white !important; color: {acc} !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}
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
    <div class="auth-card">
        <div class="auth-icon">🔐</div>
        <div class="auth-title">Welcome back to<br><span>SnackScanKH</span></div>
        <div class="auth-sub">Sign in to start scanning</div>
    </div>
    """, unsafe_allow_html=True)

    email    = st.text_input("EMAIL",    placeholder="you@example.com", key="si_email")
    password = st.text_input("PASSWORD", placeholder="••••••••", type="password", key="si_pass")

    if st.button("Sign In →", key="signin_btn"):
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
    <div class="auth-card">
        <div class="auth-icon">👋</div>
        <div class="auth-title">Join<br><span>SnackScanKH</span></div>
        <div class="auth-sub">Create your free account</div>
    </div>
    """, unsafe_allow_html=True)

    new_email    = st.text_input("EMAIL",            placeholder="you@example.com",   key="su_email")
    new_password = st.text_input("PASSWORD",         placeholder="Min. 6 characters", type="password", key="su_pass")
    confirm_pass = st.text_input("CONFIRM PASSWORD", placeholder="••••••••",          type="password", key="su_confirm")

    if st.button("Create Account →", key="signup_btn"):
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
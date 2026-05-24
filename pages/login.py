import streamlit as st
import pyrebase
from streamlit_oauth import OAuth2Component
import jwt

st.set_page_config(page_title="Sign In · AhaLaor", page_icon="favicon.png", layout="centered")

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

client_id     = st.secrets["google_auth"]["client_id"]
client_secret = st.secrets["google_auth"]["client_secret"]
redirect_uri  = st.secrets["google_auth"]["redirect_uri"]

if "user" not in st.session_state:
    st.session_state.user = None
if st.session_state.user:
    st.switch_page("app.py")
    st.stop()

acc = st.session_state.get("accent", "#7c3aed")
bg  = st.session_state.get("bg", "linear-gradient(135deg, #dde8f5 0%, #eef2fb 40%, #e8dff5 100%)")

oauth2 = OAuth2Component(
    client_id=client_id,
    client_secret=client_secret,
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token",
    refresh_token_endpoint="https://oauth2.googleapis.com/token",
    revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&display=swap');

* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {bg} !important;
}}
.stApp {{
    background: {bg} !important;
    min-height: 100vh;
}}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{
    padding-top: 3rem !important;
    max-width: 420px !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}}

/* ── Apple-grade frosted glass ── */
.frost {{
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(40px) saturate(200%) brightness(105%);
    -webkit-backdrop-filter: blur(40px) saturate(200%) brightness(105%);
    border: 1px solid rgba(255,255,255,0.85);
    box-shadow:
        0 2px 0 rgba(255,255,255,0.9) inset,
        0 -1px 0 rgba(0,0,0,0.04) inset,
        0 20px 60px rgba(0,0,0,0.08),
        0 4px 16px rgba(0,0,0,0.04);
    border-radius: 28px;
}}

/* ── Animations ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(24px) scale(0.98); }}
    to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes shimmerLine {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}
@keyframes floatA {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33%     {{ transform: translate(18px,22px) scale(1.05); }}
    66%     {{ transform: translate(-12px,14px) scale(0.97); }}
}}
@keyframes floatB {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33%     {{ transform: translate(-20px,-16px) scale(1.04); }}
    66%     {{ transform: translate(14px,-22px) scale(0.98); }}
}}
@keyframes pulse {{
    0%,100% {{ opacity: 0.6; transform: scale(1); }}
    50%     {{ opacity: 1;   transform: scale(1.04); }}
}}

/* ── Auth card ── */
.auth-card {{
    padding: 2.4rem 2rem 2rem;
    text-align: center;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.6s cubic-bezier(0.34,1.56,0.64,1) both;
}}
.auth-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(255,255,255,0.95) 30%,
        rgba(255,255,255,1) 50%,
        rgba(255,255,255,0.95) 70%,
        transparent 100%
    );
}}
.auth-card::after {{
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 60%; height: 100%;
    background: linear-gradient(105deg,
        transparent 40%,
        rgba(255,255,255,0.18) 50%,
        transparent 60%
    );
    animation: shimmerLine 6s ease-in-out infinite;
    pointer-events: none;
}}

/* ── Floating orbs ── */
.orb {{
    position: absolute; border-radius: 50%;
    pointer-events: none; filter: blur(1px);
}}
.orb1 {{
    width: 220px; height: 220px;
    background: radial-gradient(circle at 40% 40%,
        rgba(124,58,237,0.10) 0%,
        rgba(124,58,237,0.04) 40%,
        transparent 70%
    );
    top: -80px; left: -80px;
    animation: floatA 9s ease-in-out infinite;
}}
.orb2 {{
    width: 180px; height: 180px;
    background: radial-gradient(circle at 60% 60%,
        rgba(14,165,233,0.09) 0%,
        rgba(14,165,233,0.03) 40%,
        transparent 70%
    );
    bottom: -60px; right: -60px;
    animation: floatB 11s ease-in-out infinite;
}}
.orb3 {{
    width: 100px; height: 100px;
    background: radial-gradient(circle,
        rgba(236,72,153,0.07) 0%,
        transparent 70%
    );
    top: 40%; left: 70%;
    animation: pulse 5s ease-in-out infinite;
}}

/* ── App icon ── */
.app-icon-wrap {{
    width: 72px; height: 72px;
    margin: 0 auto 1.2rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.7);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow:
        0 2px 0 rgba(255,255,255,0.9) inset,
        0 8px 24px rgba(0,0,0,0.1);
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem;
    transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1);
}}
.app-icon-wrap:hover {{ transform: scale(1.06) translateY(-2px); }}

.auth-title {{
    font-size: 1.55rem; font-weight: 800; color: #1a1a2e;
    letter-spacing: -0.5px; margin: 0 0 0.3rem; line-height: 1.2;
}}
.auth-title span {{ color: {acc}; }}
.auth-sub {{ font-size: 0.83rem; color: rgba(0,0,0,0.38); line-height: 1.5; }}

/* ── Form area ── */
.form-area {{
    padding: 1.6rem 2rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.6s cubic-bezier(0.34,1.56,0.64,1) 0.08s both;
    position: relative; overflow: hidden;
}}
.form-area::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}

/* ── Inputs ── */
.stTextInput {{ margin-bottom: 0.5rem !important; }}
.stTextInput > label {{
    color: rgba(0,0,0,0.4) !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 1.6px !important;
    text-transform: uppercase !important;
    margin-bottom: 0.35rem !important;
    display: block !important;
}}
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.65) !important;
    border: 1px solid rgba(255,255,255,0.9) !important;
    border-radius: 14px !important;
    color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: all 0.2s ease !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(0,0,0,0.22) !important; }}
.stTextInput > div > div > input:focus {{
    border-color: rgba({acc.lstrip('#') and ','.join(str(int(acc.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.5) !important;
    background: rgba(255,255,255,0.88) !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.9) inset,
        0 0 0 3px rgba(124,58,237,0.1),
        0 4px 12px rgba(0,0,0,0.06) !important;
    outline: none !important;
}}

/* ── Submit button ── */
.stButton > button {{
    background: {acc} !important;
    border: none !important;
    border-radius: 14px !important;
    color: white !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    font-family: 'Outfit', sans-serif !important;
    padding: 0.72rem !important;
    letter-spacing: 0.2px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.25) inset,
        0 6px 20px rgba(124,58,237,0.32),
        0 2px 6px rgba(124,58,237,0.2) !important;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1) !important;
    margin-top: 0.5rem !important;
}}
.stButton > button:hover {{
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.25) inset,
        0 10px 28px rgba(124,58,237,0.4),
        0 4px 10px rgba(124,58,237,0.25) !important;
}}
.stButton > button:active {{
    transform: translateY(0) scale(0.99) !important;
}}

/* ── Back button ── */
.back-btn > div > button {{
    background: rgba(255,255,255,0.55) !important;
    border: 1px solid rgba(255,255,255,0.85) !important;
    color: rgba(0,0,0,0.45) !important;
    border-radius: 99px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    width: auto !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
    margin-bottom: 1rem !important;
    margin-top: 0 !important;
    padding: 0.4rem 1.1rem !important;
    transition: all 0.2s ease !important;
}}
.back-btn > div > button:hover {{
    background: rgba(255,255,255,0.85) !important;
    color: {acc} !important;
    border-color: rgba(124,58,237,0.3) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08) !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.45) !important;
    border-radius: 16px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.8) !important;
    backdrop-filter: blur(20px) !important;
    gap: 4px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    color: rgba(0,0,0,0.38) !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.1px !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(255,255,255,0.92) !important;
    color: {acc} !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.9) inset,
        0 2px 10px rgba(0,0,0,0.08) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1rem !important; }}

/* ── Checkbox ── */
.stCheckbox {{ margin-top: 0.2rem !important; }}
.stCheckbox label {{
    color: rgba(0,0,0,0.4) !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
}}

/* ── Divider ── */
.or-divider {{
    display: flex; align-items: center; gap: 10px;
    margin: 1rem 0; color: rgba(0,0,0,0.25);
    font-size: 0.75rem; font-weight: 600;
    letter-spacing: 1px; text-transform: uppercase;
}}
.or-divider::before, .or-divider::after {{
    content: ''; flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,0,0,0.08), transparent);
}}

/* ── Alerts ── */
.success-box {{
    background: rgba(240,253,244,0.85);
    border: 1px solid rgba(187,247,208,0.9);
    border-radius: 14px; padding: 0.85rem 1rem;
    color: #16a34a; font-size: 0.88rem; margin-bottom: 0.8rem;
    backdrop-filter: blur(12px); text-align: left;
    animation: fadeUp 0.3s ease both;
    box-shadow: 0 2px 8px rgba(16,185,129,0.08);
}}
.error-box {{
    background: rgba(255,245,245,0.85);
    border: 1px solid rgba(254,226,226,0.9);
    border-radius: 14px; padding: 0.85rem 1rem;
    color: #dc2626; font-size: 0.88rem; margin-bottom: 0.8rem;
    backdrop-filter: blur(12px); text-align: left;
    animation: fadeUp 0.3s ease both;
    box-shadow: 0 2px 8px rgba(239,68,68,0.08);
}}

/* ── OAuth Google button ── */
[data-testid="stButton"] > button[kind="secondary"],
div[data-testid="stVerticalBlock"] iframe {{
    border-radius: 14px !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Logo ──
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    try:
        st.image("lock.png", width=64)
    except:
        pass

# ── Back button ──
st.markdown('<div class="back-btn">', unsafe_allow_html=True)
if st.button("← Back to AhaLaor"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2 = st.tabs(["Sign In", "Create Account"])

# ════════════════════════════════
# TAB 1 — SIGN IN
# ════════════════════════════════
with tab1:
    st.markdown(f"""
    <div class="frost auth-card">
        <div class="orb orb1"></div>
        <div class="orb orb2"></div>
        <div class="orb orb3"></div>
        <div class="app-icon-wrap">🍱</div>
        <div class="auth-title">Welcome back to<br><span>AhaLaor AI</span></div>
        <div class="auth-sub">Sign in to start scanning your food</div>
    </div>
    """, unsafe_allow_html=True)

    remembered_email = st.session_state.get("remembered_email", "")

    with st.form("signin_form"):
        email    = st.text_input("EMAIL",    placeholder="you@example.com", value=remembered_email)
        password = st.text_input("PASSWORD", placeholder="••••••••", type="password")
        remember = st.checkbox("Remember me", value=bool(remembered_email))
        submitted = st.form_submit_button("Sign In →")

    if submitted:
        if not email or not password:
            st.markdown('<div class="error-box">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        else:
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                user_info      = auth.get_account_info(user["idToken"])
                email_verified = user_info["users"][0]["emailVerified"]
                if not email_verified:
                    st.markdown('<div class="error-box">📧 Please verify your email first. Check your inbox.</div>', unsafe_allow_html=True)
                else:
                    st.session_state.user = {
                        "email": email,
                        "token": user["idToken"],
                        "uid":   user["localId"],
                    }
                    st.session_state.remembered_email = email if remember else ""
                    st.switch_page("app.py")
            except Exception:
                st.markdown('<div class="error-box">❌ Incorrect email or password.</div>', unsafe_allow_html=True)

    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

    result = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com/favicon.ico",
        redirect_uri=redirect_uri,
        scope="openid email profile",
        key="google_signin",
        extras_params={"prompt": "consent"},
        use_container_width=True,
    )
    if result and "token" in result:
        try:
            id_info = jwt.decode(
                result["token"]["id_token"],
                options={"verify_signature": False}
            )
            st.session_state.user = {
                "email":   id_info["email"],
                "name":    id_info.get("name", ""),
                "picture": id_info.get("picture", ""),
                "uid":     id_info["sub"],
                "token":   result["token"]["access_token"],
            }
            st.switch_page("app.py")
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Google sign-in failed: {e}</div>', unsafe_allow_html=True)

# ════════════════════════════════
# TAB 2 — CREATE ACCOUNT
# ════════════════════════════════
with tab2:
    st.markdown(f"""
    <div class="frost auth-card">
        <div class="orb orb1"></div>
        <div class="orb orb2"></div>
        <div class="orb orb3"></div>
        <div class="app-icon-wrap">👋</div>
        <div class="auth-title">Join<br><span>AhaLaor AI</span></div>
        <div class="auth-sub">Create your free account today</div>
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
                auth.send_email_verification(user["idToken"])
                st.markdown('<div class="success-box">🎉 Account created! Check your email for the verification link before signing in.</div>', unsafe_allow_html=True)
                st.stop()
            except Exception:
                st.markdown('<div class="error-box">❌ Email may already be in use.</div>', unsafe_allow_html=True)

    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

    result2 = oauth2.authorize_button(
        name="Continue with Google",
        icon="https://www.google.com/favicon.ico",
        redirect_uri=redirect_uri,
        scope="openid email profile",
        key="google_signup",
        extras_params={"prompt": "consent"},
        use_container_width=True,
    )
    if result2 and "token" in result2:
        try:
            id_info = jwt.decode(
                result2["token"]["id_token"],
                options={"verify_signature": False}
            )
            st.session_state.user = {
                "email":   id_info["email"],
                "name":    id_info.get("name", ""),
                "picture": id_info.get("picture", ""),
                "uid":     id_info["sub"],
                "token":   result2["token"]["access_token"],
            }
            st.switch_page("app.py")
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Google sign-in failed: {e}</div>', unsafe_allow_html=True)
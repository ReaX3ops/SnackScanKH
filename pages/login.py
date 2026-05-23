import streamlit as st
import pyrebase
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

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

firebase  = pyrebase.initialize_app(firebase_config)
auth      = firebase.auth()

# ── Google OAuth config ──
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

# ── Handle Google OAuth callback ──
params = st.query_params
if "code" in params:
    try:
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id":     client_id,
                    "client_secret": client_secret,
                    "redirect_uris": [redirect_uri],
                    "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                    "token_uri":     "https://oauth2.googleapis.com/token",
                }
            },
            scopes=["openid", "email", "profile"],
            redirect_uri=redirect_uri,
        )
        flow.fetch_token(code=params["code"])
        credentials = flow.credentials
        id_info = id_token.verify_oauth2_token(
            credentials.id_token,
            google_requests.Request(),
            client_id
        )
        st.session_state.user = {
            "email":   id_info["email"],
            "name":    id_info.get("name", ""),
            "picture": id_info.get("picture", ""),
            "uid":     id_info["sub"],
            "token":   credentials.token,
        }
        st.query_params.clear()
        st.switch_page("app.py")
    except Exception as e:
        st.error(f"Google sign-in failed: {e}")

# ── Build Google auth URL ──
def get_google_auth_url():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id":     client_id,
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
                "auth_uri":      "https://accounts.google.com/o/oauth2/auth",
                "token_uri":     "https://oauth2.googleapis.com/token",
            }
        },
        scopes=["openid", "email", "profile"],
        redirect_uri=redirect_uri,
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return auth_url

google_auth_url = get_google_auth_url()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; box-sizing: border-box; }}

.stApp {{
    background: {bg} !important;
    min-height: 100vh;
}}
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {bg} !important;
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
.orb {{ position: absolute; border-radius: 50%; pointer-events: none; }}
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
    margin-bottom: 0.3rem !important; display: block !important;
}}

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
    font-size: 0.83rem !important; font-weight: 500 !important;
    width: auto !important; box-shadow: none !important;
    backdrop-filter: blur(12px) !important;
    margin-bottom: 1.2rem !important; margin-top: 0 !important;
    padding: 0.4rem 1.2rem !important;
}}
.back-btn > div > button:hover {{
    background: rgba(255,255,255,0.8) !important;
    border-color: {acc} !important; color: {acc} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: rgba(255,255,255,0.4) !important;
    border-radius: 14px !important; padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.65) !important;
    backdrop-filter: blur(16px) !important; gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 10px !important; font-weight: 600 !important;
    font-size: 0.88rem !important; color: rgba(0,0,0,0.4) !important;
    padding: 0.4rem 1.2rem !important; transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: rgba(255,255,255,0.85) !important;
    color: {acc} !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

.stCheckbox {{ margin-top: 0.3rem !important; margin-bottom: 0.2rem !important; }}
.stCheckbox label {{
    color: rgba(0,0,0,0.45) !important;
    font-size: 0.85rem !important; font-weight: 500 !important;
    letter-spacing: 0 !important; text-transform: none !important;
}}

/* ── Divider ── */
.or-divider {{
    display: flex; align-items: center; gap: 12px;
    margin: 1rem 0; color: rgba(0,0,0,0.3);
    font-size: 0.78rem; font-weight: 500;
}}
.or-divider::before, .or-divider::after {{
    content: ''; flex: 1;
    height: 1px; background: rgba(0,0,0,0.1);
}}

/* ── Google button ── */
.google-btn {{
    display: flex; align-items: center; justify-content: center; gap: 10px;
    background: rgba(255,255,255,0.85);
    border: 1.5px solid rgba(0,0,0,0.08);
    border-radius: 14px; padding: 0.7rem 1.2rem;
    font-size: 0.93rem; font-weight: 600; color: #1a1a2e;
    text-decoration: none; width: 100%;
    backdrop-filter: blur(12px);
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    transition: all 0.25s;
    margin-bottom: 0.2rem;
}}
.google-btn:hover {{
    background: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    transform: translateY(-2px);
    text-decoration: none; color: #1a1a2e;
}}
.google-logo {{
    width: 20px; height: 20px; flex-shrink: 0;
}}
</style>
""", unsafe_allow_html=True)

# ── Logo ──
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    try:
        st.image("lock.png", width=68)
    except:
        pass

# ── Back button ──
st.markdown('<div class="back-btn">', unsafe_allow_html=True)
if st.button("← Back to AhaLaor"):
    st.switch_page("app.py")
st.markdown('</div>', unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2 = st.tabs(["Sign In", "Create Account"])

with tab1:
    st.markdown(f"""
    <div class="glass auth-card">
        <div class="orb orb1"></div><div class="orb orb2"></div>
        <div class="auth-icon">🔐</div>
        <div class="auth-title">Welcome back to<br><span>AhaLaor AI</span></div>
        <div class="auth-sub">Sign in to start scanning</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Google Sign-In button ──
    st.markdown(f"""
    <a href="{google_auth_url}" class="google-btn" target="_self">
        <svg class="google-logo" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Continue with Google
    </a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

    remembered_email = st.session_state.get("remembered_email", "")

    with st.form("signin_form"):
        email     = st.text_input("EMAIL",    placeholder="you@example.com", value=remembered_email)
        password  = st.text_input("PASSWORD", placeholder="••••••••", type="password")
        remember  = st.checkbox("Remember me", value=bool(remembered_email))
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
                    st.markdown('<div class="error-box">📧 Please verify your email first. Check your inbox for the verification link.</div>', unsafe_allow_html=True)
                else:
                    st.session_state.user = {
                        "email": email,
                        "token": user["idToken"],
                        "uid":   user["localId"]
                    }
                    if remember:
                        st.session_state.remembered_email = email
                    else:
                        st.session_state.remembered_email = ""
                    st.switch_page("app.py")
            except Exception:
                st.markdown('<div class="error-box">❌ Incorrect email or password.</div>', unsafe_allow_html=True)

with tab2:
    st.markdown(f"""
    <div class="glass auth-card">
        <div class="orb orb1"></div><div class="orb orb2"></div>
        <div class="auth-icon">👋</div>
        <div class="auth-title">Join<br><span>AhaLaor</span></div>
        <div class="auth-sub">Create your free account</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Google Sign-Up button ──
    st.markdown(f"""
    <a href="{google_auth_url}" class="google-btn" target="_self">
        <svg class="google-logo" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        Continue with Google
    </a>
    """, unsafe_allow_html=True)

    st.markdown('<div class="or-divider">or</div>', unsafe_allow_html=True)

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
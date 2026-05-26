import streamlit as st
from google import genai
from PIL import Image
import json
import time

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
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def t(en, km):
    return km if st.session_state.lang == "km" else en

acc = st.session_state.accent
bg  = st.session_state.bg

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

/* ── Apple-grade frosted glass ── */
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

/* ── Animations ── */
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(20px) scale(0.98); }}
    to   {{ opacity: 1; transform: translateY(0) scale(1); }}
}}
@keyframes shimmerLine {{
    0%   {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(400%); }}
}}
@keyframes floatA {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33%     {{ transform: translate(18px,22px) scale(1.04); }}
    66%     {{ transform: translate(-12px,14px) scale(0.97); }}
}}
@keyframes floatB {{
    0%,100% {{ transform: translate(0,0) scale(1); }}
    33%     {{ transform: translate(-20px,-16px) scale(1.03); }}
    66%     {{ transform: translate(14px,-22px) scale(0.98); }}
}}
@keyframes dash {{
    to {{ stroke-dashoffset: 0; }}
}}

/* ── Buttons ── */
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
.stButton > button:active {{
    transform: translateY(0) scale(0.98) !important;
}}

/* ── Scan button ── */
div.scan-btn > div > button {{
    background: {acc} !important;
    border: none !important;
    border-radius: 18px !important;
    color: white !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: 0.2px !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.2) inset,
        0 8px 28px rgba(124,58,237,0.35),
        0 3px 10px rgba(124,58,237,0.2) !important;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1) !important;
    backdrop-filter: none !important;
}}
div.scan-btn > div > button:hover {{
    transform: translateY(-2px) scale(1.01) !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.2) inset,
        0 12px 36px rgba(124,58,237,0.45),
        0 5px 14px rgba(124,58,237,0.25) !important;
}}
div.scan-btn > div > button:active {{
    transform: translateY(0) scale(0.99) !important;
}}

.upload-zone {{
    background: rgba(255,255,255,0.38);
    border: 2.5px dashed rgba(124,58,237,0.28);
    border-radius: 26px;
    padding: 3rem 2rem;
    text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: 0 2px 16px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.8) inset;
    margin-bottom: 0.5rem;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    cursor: pointer;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    position: relative;
    overflow: hidden;
    min-height: 180px;
}}
.upload-zone:hover {{
    background: rgba(255,255,255,0.58);
    border-color: rgba(124,58,237,0.5);
    box-shadow: 0 8px 32px rgba(124,58,237,0.1), 0 1px 0 rgba(255,255,255,0.9) inset;
    transform: translateY(-2px);
}}
.upload-icon {{
    font-size: 3rem; margin-bottom: 0.7rem;
    animation: floatA 4s ease-in-out infinite;
    display: block;
}}
.upload-title {{
    font-size: 1.05rem; font-weight: 700;
    color: #1a1a2e; margin-bottom: 0.3rem;
}}
.upload-sub {{
    font-size: 0.8rem; color: rgba(0,0,0,0.32);
    font-weight: 400;
}}

/* ── Make file uploader invisible but cover entire zone ── */
[data-testid="stFileUploadDropzone"] {{
    position: relative !important;
    z-index: 10 !important;
    margin-top: -180px !important;
    height: 180px !important;
    min-height: 180px !important;
    opacity: 0 !important;
    cursor: pointer !important;
    border: none !important;
    background: transparent !important;
    border-radius: 26px !important;
}}
[data-testid="stFileUploadDropzone"] > div {{
    height: 180px !important;
    min-height: 180px !important;
}}

[data-testid="stImage"] img {{
    border-radius: 22px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.06) !important;
    border: 1px solid rgba(255,255,255,0.7) !important;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
}}

/* ── Text input ── */
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(255,255,255,0.88) !important;
    border-radius: 14px !important;
    color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.9) inset, 0 2px 8px rgba(0,0,0,0.04) !important;
    transition: all 0.2s ease !important;
    padding: 0.65rem 1rem !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(0,0,0,0.22) !important; }}
.stTextInput > div > div > input:focus {{
    border-color: rgba(124,58,237,0.4) !important;
    background: rgba(255,255,255,0.88) !important;
    box-shadow:
        0 1px 0 rgba(255,255,255,0.9) inset,
        0 0 0 3px rgba(124,58,237,0.1),
        0 4px 12px rgba(0,0,0,0.06) !important;
}}
.stTextInput label {{
    color: rgba(0,0,0,0.38) !important; font-size: 0.67rem !important;
    font-weight: 700 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}}

/* ── Progress ── */
.stProgress > div > div {{
    background: {acc} !important; border-radius: 99px !important;
    transition: width 0.5s cubic-bezier(0.34,1.56,0.64,1) !important;
}}
.stProgress > div {{
    background: rgba(255,255,255,0.45) !important;
    border-radius: 99px !important; height: 6px !important;
    backdrop-filter: blur(8px) !important;
    box-shadow: 0 1px 0 rgba(255,255,255,0.6) inset !important;
}}

/* ── Alert ── */
.stAlert {{
    background: rgba(255,245,245,0.75) !important;
    border: 1px solid rgba(254,226,226,0.85) !important;
    border-radius: 16px !important; color: #dc2626 !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 4px 16px rgba(239,68,68,0.08) !important;
}}

/* ── Result cards ── */
.g-card {{
    padding: 1.5rem 1.8rem;
    margin-bottom: 0.9rem;
    position: relative; overflow: hidden;
    animation: fadeUp 0.55s cubic-bezier(0.34,1.56,0.64,1) both;
}}
.g-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}
.g-card::after {{
    content: '';
    position: absolute; inset: 0; border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,0.35) 0%, transparent 55%);
    pointer-events: none;
}}
.g-card-accent {{ border-left: 3px solid {acc} !important; }}
.g-card-green  {{ border-left: 3px solid #10b981 !important; }}
.g-card-blue   {{ border-left: 3px solid #0ea5e9 !important; }}

.chip-label {{
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: {acc}; margin-bottom: 0.45rem; display: block; opacity: 0.7;
}}
.chip-label-green {{ color: #10b981; opacity: 1; }}
.chip-label-blue  {{ color: #0ea5e9; opacity: 1; }}

.food-name {{
    font-size: 1.95rem; font-weight: 700; color: #1a1a2e;
    letter-spacing: -0.5px; line-height: 1.2;
}}
.cal-number {{
    font-size: 3.2rem; font-weight: 800; color: #10b981;
    letter-spacing: -2px; line-height: 1;
}}
.cal-unit {{
    font-size: 0.95rem; color: rgba(0,0,0,0.28);
    margin-left: 5px; font-weight: 300;
}}

/* ── Nutrition grid ── */
.nut-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 9px; margin-top: 0.9rem; }}
.nut-cell {{
    background: rgba(255,255,255,0.5);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 18px; padding: 1rem 0.4rem;
    text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.9) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
}}
.nut-cell:hover {{
    background: rgba(255,255,255,0.82);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 12px 28px rgba(0,0,0,0.09), 0 1px 0 rgba(255,255,255,0.9) inset;
}}
.nut-icon {{ font-size: 1.4rem; line-height: 1; }}
.nut-val {{ font-size: 1.05rem; font-weight: 700; color: #1a1a2e; margin: 5px 0 3px; }}
.nut-name {{ font-size: 0.58rem; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(0,0,0,0.32); }}

/* ── Benefit / source rows ── */
.info-row {{
    display: flex; align-items: flex-start; gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.55);
    font-size: 0.88rem; color: #1a1a2e; line-height: 1.5;
}}
.info-row:last-child {{ border-bottom: none; }}
.info-row-sub {{
    font-size: 0.78rem; color: rgba(0,0,0,0.4);
    margin-top: 1px;
}}

/* ── Tags ── */
.tag-wrap {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 0.75rem; }}
.tag {{
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.8);
    border-radius: 99px; padding: 6px 16px;
    font-size: 0.83rem; color: rgba(0,0,0,0.5);
    backdrop-filter: blur(12px);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.9) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
}}
.tag:hover {{
    background: rgba(255,255,255,0.9);
    color: {acc};
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
}}

/* ── Donut ── */
.donut-wrap {{ display: flex; align-items: center; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap; }}
.donut-legend {{ display: flex; flex-direction: column; gap: 9px; }}
.legend-item {{ display: flex; align-items: center; gap: 9px; font-size: 0.83rem; color: rgba(0,0,0,0.5); }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.legend-pct {{ font-weight: 700; color: #1a1a2e; margin-left: auto; padding-left: 12px; }}

/* ── Settings panel ── */
.settings-wrap {{
    padding: 1.8rem 2rem 2rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    position: relative; overflow: hidden;
}}
.settings-wrap::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.95), transparent);
}}
.settings-title {{
    font-size: 1.1rem; font-weight: 700; color: #1a1a2e;
    margin: 0 0 1.4rem; letter-spacing: -0.3px;
}}
.settings-section {{
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: rgba(0,0,0,0.28); margin-bottom: 0.8rem; display: block;
}}
.gradient-swatch {{
    height: 54px; border-radius: 16px;
    border: 2px solid rgba(255,255,255,0.85);
    cursor: pointer;
    box-shadow: 0 3px 12px rgba(0,0,0,0.09), 0 1px 0 rgba(255,255,255,0.6) inset;
    transition: all 0.2s cubic-bezier(0.34,1.56,0.64,1);
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 600; color: rgba(0,0,0,0.5);
    margin-bottom: 4px;
}}
.gradient-swatch:hover {{
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 10px 24px rgba(0,0,0,0.13);
}}
.gradient-swatch.active {{
    border-color: {acc} !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.18), 0 8px 24px rgba(0,0,0,0.12);
}}
.s-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.7), transparent);
    margin: 1.3rem 0;
}}
.preview-bar {{
    height: 5px; border-radius: 99px;
    margin: 0.8rem auto 0; max-width: 160px;
    transition: background 0.35s ease;
    box-shadow: 0 2px 8px rgba(124,58,237,0.2);
}}

[data-testid="stColorPicker"] {{ display: flex; justify-content: center; }}
[data-testid="stColorPicker"] > div {{
    width: 58px !important; height: 58px !important;
    border-radius: 50% !important;
    border: 3px solid rgba(255,255,255,0.9) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12), 0 1px 0 rgba(255,255,255,0.9) inset !important;
    cursor: pointer !important;
    transition: transform 0.2s cubic-bezier(0.34,1.56,0.64,1), box-shadow 0.2s !important;
}}
[data-testid="stColorPicker"] > div:hover {{
    transform: scale(1.1) !important;
    box-shadow: 0 8px 22px rgba(0,0,0,0.16) !important;
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
col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

with col1:
    try:
        ic, tx = st.columns([1, 5])
        with ic:
            st.image("favicon.jpg", width=34)
        with tx:
            st.markdown(f"""
            <div style="display:flex;align-items:center;height:100%;margin-top:4px;">
                <span style="font-size:1.05rem;font-weight:800;color:#1a1a2e;letter-spacing:-0.4px;">
                    AhaLaor <span style="color:{acc};">AI</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
    except:
        st.markdown(f"""
        <div style="display:flex;align-items:center;height:100%;">
            <span style="font-size:1.05rem;font-weight:800;color:#1a1a2e;letter-spacing:-0.4px;">
                AhaLaor <span style="color:{acc};">AI</span>
            </span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    if st.button("⚙️", help="Settings"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

with col3:
    if st.button("🇰🇭" if st.session_state.lang == "en" else "🇬🇧"):
        st.session_state.lang = "km" if st.session_state.lang == "en" else "en"
        st.rerun()

with col4:
    if st.session_state.get("user"):
        email_short = st.session_state.user.get("email", "").split("@")[0]
        if st.button(f"👤 {email_short[:8]}", help="Click to sign out"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("🔐 Login"):
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
    st.markdown('<span class="settings-section">✦ Custom Background Color</span>', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════
# ── Gemini client ──
# ══════════════════════════════════════
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# ══════════════════════════════════════
# ── Upload zone ──
# ══════════════════════════════════════
st.markdown(f"""
<style>
.upload-wrapper {{
    position: relative;
    margin-bottom: 1rem;
    cursor: pointer;
}}
.upload-zone {{
    background: rgba(255,255,255,0.38);
    border: 2.5px dashed rgba(124,58,237,0.28);
    border-radius: 26px;
    padding: 3.5rem 2rem;
    text-align: center;
    backdrop-filter: blur(20px);
    box-shadow: 0 2px 16px rgba(0,0,0,0.04), 0 1px 0 rgba(255,255,255,0.8) inset;
    transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
    animation: fadeUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both;
    pointer-events: none;
}}
.upload-wrapper:hover .upload-zone {{
    background: rgba(255,255,255,0.65);
    border-color: rgba(124,58,237,0.55);
    box-shadow: 0 8px 32px rgba(124,58,237,0.12), 0 1px 0 rgba(255,255,255,0.9) inset;
    transform: translateY(-2px);
}}
.upload-icon {{
    font-size: 3.2rem; margin-bottom: 0.7rem; display: block;
    animation: floatA 4s ease-in-out infinite;
}}
.upload-title {{
    font-size: 1.05rem; font-weight: 700;
    color: #1a1a2e; margin-bottom: 0.3rem;
}}
.upload-sub {{
    font-size: 0.8rem; color: rgba(0,0,0,0.32); font-weight: 400;
}}

/* Native uploader: absolute, covers entire wrapper */
[data-testid="stFileUploader"] {{
    position: absolute !important;
    top: 0 !important; left: 0 !important;
    width: 100% !important; height: 100% !important;
    z-index: 10 !important;
    opacity: 0 !important;
    cursor: pointer !important;
}}
[data-testid="stFileUploadDropzone"] {{
    width: 100% !important;
    height: 100% !important;
    min-height: 200px !important;
    cursor: pointer !important;
    border: none !important;
    background: transparent !important;
    border-radius: 26px !important;
}}
[data-testid="stFileUploadDropzone"] > div {{
    width: 100% !important;
    height: 100% !important;
    min-height: 200px !important;
}}
[data-testid="stFileUploader"] label {{ display: none !important; }}
[data-testid="stFileUploader"] section {{ display: none !important; }}
[data-testid="stFileUploader"] button {{ display: none !important; }}
</style>

<div class="upload-wrapper">
    <div class="upload-zone">
        <span class="upload-icon">🍱</span>
        <div class="upload-title">{t("Drop your food photo here", "ទម្លាក់រូបភាពម្ហូបរបស់អ្នក")}</div>
        <div class="upload-sub">{t("Drag & drop or click to browse · JPG PNG WEBP", "អូស & ទម្លាក់ ឬចុចដើម្បីរក · JPG PNG WEBP")}</div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "upload",
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

    if scan_clicked:
        if not st.session_state.get("user"):
            st.switch_page("pages/login.py")
            st.stop()

        st.session_state.result = None

        progress_text = st.empty()
        bar = st.progress(0)

        steps = [
            (15, t("Reading your photo...",      "កំពុងអានរូបភាព...")),
            (35, t("Identifying the food...",    "កំពុងកំណត់ម្ហូប...")),
            (58, t("Calculating calories...",    "កំពុងគណនាកាឡូរី...")),
            (78, t("Breaking down nutrition...", "កំពុងវិភាគជីវជាតិ...")),
            (92, t("Wrapping up results...",     "កំពុងបញ្ចប់លទ្ធផល...")),
        ]
        for pct, msg in steps:
            time.sleep(0.35)
            progress_text.markdown(f"""
            <div style="text-align:center;font-size:0.82rem;color:rgba(0,0,0,0.4);
            font-weight:500;margin-bottom:0.4rem;letter-spacing:0.3px;">{msg}</div>
            """, unsafe_allow_html=True)
            bar.progress(pct)

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
            progress_text.markdown(f"""
            <div style="text-align:center;font-size:0.85rem;color:#10b981;
            font-weight:600;margin-bottom:0.4rem;">✅ {t("Done!", "រួចរាល់!")}</div>
            """, unsafe_allow_html=True)
            bar.progress(100)
            time.sleep(0.5)
            bar.empty()
            progress_text.empty()
        except Exception as e:
            bar.empty()
            progress_text.empty()
            st.error(f"Error: {e}")

# ══════════════════════════════════════
# ── Results ──
# ══════════════════════════════════════
if st.session_state.result and st.session_state.image:
    data = st.session_state.result
    lang = st.session_state.lang
    food        = data.get("food_km" if lang == "km" else "food_en", "Unknown")
    food_en     = data.get("food_en", "this food")
    calories    = str(data.get("calories", "?"))
    nutrition   = data.get("nutrition", {})
    ing_key     = "ingredients_km" if lang == "km" else "ingredients_en"
    ignore      = ["bun", "bread", "beef patty"]
    ingredients = [i for i in data.get(ing_key, []) if i.lower() not in ignore]

    def parse_g(val):
        try:
            return float(''.join(c for c in str(val) if c.isdigit() or c == '.'))
        except:
            return 0.0

    protein_g = parse_g(nutrition.get("protein", "0"))
    carbs_g   = parse_g(nutrition.get("carbs",   "0"))
    fat_g     = parse_g(nutrition.get("fat",     "0"))
    fiber_g   = parse_g(nutrition.get("fiber",   "0"))
    sodium_mg = parse_g(nutrition.get("sodium",  "0"))

    # ── Detected food ──
    st.markdown(f"""
    <div class="frost g-card g-card-accent">
        <span class="chip-label">🍽 {t("Detected Food", "ម្ហូបដែលបានរកឃើញ")}</span>
        <div class="food-name">{food}</div>
    </div>""", unsafe_allow_html=True)

    # ── Calories ──
    st.markdown(f"""
    <div class="frost g-card g-card-green">
        <span class="chip-label chip-label-green">🔥 {t("Estimated Calories", "កាឡូរីដែលប៉ាន់ស្មាន")}</span>
        <div><span class="cal-number">{calories}</span><span class="cal-unit">kcal</span></div>
    </div>""", unsafe_allow_html=True)

    # ── Nutrition breakdown ──
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

    # ── What this food helps with ──
    benefits = []
    if protein_g >= 10:
        benefits.append((
            "💪", t("Muscle building & repair", "កសាង & ជួសជុលសាច់ដុំ"),
            t(f"High protein ({int(protein_g)}g) supports muscle recovery and growth",
              f"ប្រូតេអ៊ីនខ្ពស់ ({int(protein_g)}g) ជួយស្ដារ & លូតសាច់ដុំ")
        ))
    elif protein_g >= 5:
        benefits.append((
            "🫀", t("Heart & tissue support", "គាំទ្របេះដូង & ជាលិកា"),
            t(f"Moderate protein ({int(protein_g)}g) supports cell repair",
              f"ប្រូតេអ៊ីនមធ្យម ({int(protein_g)}g) ជួយជួសជុលកោសិកា")
        ))
    if carbs_g >= 30:
        benefits.append((
            "⚡", t("Energy boost", "ថាមពលរហ័ស"),
            t(f"High carbs ({int(carbs_g)}g) give quick sustained energy",
              f"កាបូអ៊ីដ្រាតខ្ពស់ ({int(carbs_g)}g) ផ្ដល់ថាមពលយូរ")
        ))
    if fat_g >= 8:
        benefits.append((
            "🧠", t("Brain & hormone health", "សុខភាពខួរក្បាល & អ័រម៉ូន"),
            t(f"Fat ({int(fat_g)}g) supports brain function and hormone balance",
              f"ខ្លាញ់ ({int(fat_g)}g) គាំទ្រខួរក្បាល & តុល្យភាពអ័រម៉ូន")
        ))
    if fiber_g >= 3:
        benefits.append((
            "🌿", t("Digestive health", "សុខភាពរំលាយអាហារ"),
            t(f"Fiber ({int(fiber_g)}g) promotes healthy digestion",
              f"ជាតិសរសៃ ({int(fiber_g)}g) ជំរុញការរំលាយអាហារល្អ")
        ))
    if not benefits:
        benefits.append((
            "🍃", t("Light & balanced", "ស្រាល & មានតុល្យភាព"),
            t("Low in macros — good as a light meal or snack",
              "ម៉ាក្រូទាប — ល្អជាអាហារស្រាល ឬអាហារសម្រន់")
        ))

    benefit_rows = "".join(f"""
    <div class="info-row">
        <span style="font-size:1.2rem;">{icon}</span>
        <div>
            <div style="font-weight:600;color:#1a1a2e;">{title}</div>
            <div class="info-row-sub">{sub}</div>
        </div>
    </div>""" for icon, title, sub in benefits)

    st.markdown(f"""
    <div class="frost g-card g-card-blue">
        <span class="chip-label chip-label-blue">✦ {t("What This Food Helps With", "តើអាហារនេះជួយអ្វី")}</span>
        {benefit_rows}
    </div>""", unsafe_allow_html=True)

    # ── Where nutrients come from ──
    sources = []
    if carbs_g >= 15:
        sources.append((
            "🍞", t("Carbohydrates", "កាបូអ៊ីដ្រាត"), f"{int(carbs_g)}g",
            t("Grains, rice, noodles or starchy vegetables",
              "ធញ្ញជាតិ, បាយ, មី ឬបន្លែមានម្សៅ")
        ))
    if fat_g >= 5:
        sources.append((
            "🧈", t("Fats", "ខ្លាញ់"), f"{int(fat_g)}g",
            t("Cooking oils, meat, dairy or nuts",
              "ប្រេងចម្អិន, សាច់, ទឹកដោះគោ ឬគ្រាប់")
        ))
    if protein_g >= 5:
        sources.append((
            "💪", t("Protein", "ប្រូតេអ៊ីន"), f"{int(protein_g)}g",
            t("Meat, fish, eggs, tofu or legumes",
              "សាច់, ត្រី, ពង, តៅហ៊ូ ឬ legumes")
        ))
    if sodium_mg >= 200:
        sources.append((
            "🧂", t("Sodium", "អំបិល"), f"{int(sodium_mg)}mg",
            t("Salt, soy sauce, fish sauce or seasoning",
              "អំបិល, ស៊ីអ៊ីវ, ទឹកត្រី ឬគ្រឿងទេស")
        ))
    if fiber_g >= 2:
        sources.append((
            "🌿", t("Fiber", "ជាតិសរសៃ"), f"{int(fiber_g)}g",
            t("Vegetables, fruits or whole grains",
              "បន្លែ, ផ្លែឈើ ឬធញ្ញជាតិពេញ")
        ))

    if sources:
        source_rows = "".join(f"""
        <div class="info-row">
            <span style="font-size:1.2rem;">{icon}</span>
            <div style="flex:1;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <span style="font-weight:600;color:#1a1a2e;">{name}</span>
                    <span style="font-size:0.8rem;font-weight:700;color:{acc};
                    background:rgba(124,58,237,0.08);padding:2px 10px;
                    border-radius:99px;">{amount}</span>
                </div>
                <div class="info-row-sub">{source}</div>
            </div>
        </div>""" for icon, name, amount, source in sources)

        st.markdown(f"""
        <div class="frost g-card g-card-accent">
            <span class="chip-label">📍 {t("Where Nutrients Come From", "តើជីវជាតិមកពីណា")}</span>
            {source_rows}
        </div>""", unsafe_allow_html=True)

    # ── Macro wheel ──
    if nutrition:
        macro_cals = {
            t("Protein", "ប្រូតេអ៊ីន"):  protein_g * 4,
            t("Carbs",   "កាបូអ៊ីដ្រាត"): carbs_g   * 4,
            t("Fat",     "ខ្លាញ់"):        fat_g     * 9,
            t("Fiber",   "ជាតិសរសៃ"):      fiber_g   * 2,
            t("Sugar",   "ស្ករ"):          parse_g(nutrition.get("sugar","0")) * 4,
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

    # ── Ingredients ──
    if ingredients:
        tags = "".join(f'<span class="tag">{i}</span>' for i in ingredients)
        st.markdown(f"""
        <div class="frost g-card">
            <span class="chip-label">🥬 {t("Ingredients", "គ្រឿងផ្សំ")}</span>
            <div class="tag-wrap">{tags}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="page-footer">AhaLaor AI · Made with ♥ in Phnom Penh</div>', unsafe_allow_html=True)
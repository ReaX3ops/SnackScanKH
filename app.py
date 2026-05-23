import streamlit as st
from google import genai
from PIL import Image
import json
import time

st.set_page_config(
    page_title="SnackScanKH",
    page_icon="🍱",
    layout="centered"
)

for k, v in {"lang": "en", "result": None, "image": None, "accent": "#7c3aed"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def t(en, km):
    return km if st.session_state.lang == "km" else en

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
.block-container {{ padding-top: 2.5rem; max-width: 680px; }}

/* ── Frosted glass base ── */
.glass {{
    background: rgba(255,255,255,0.55);
    backdrop-filter: blur(28px) saturate(180%);
    -webkit-backdrop-filter: blur(28px) saturate(180%);
    border: 1px solid rgba(255,255,255,0.75);
    box-shadow: 0 8px 32px rgba(0,0,0,0.07), 0 1px 0 rgba(255,255,255,0.9) inset;
    border-radius: 24px;
    animation: fadeUp 0.5s ease both;
}}
@keyframes fadeUp {{
    from {{ opacity: 0; transform: translateY(18px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes shimmer {{
    0%   {{ background-position: -200% center; }}
    100% {{ background-position:  200% center; }}
}}

.hero-wrap {{
    padding: 2.2rem 2rem 2rem;
    margin-bottom: 1.2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}}
.hero-wrap::before {{
    content: '';
    position: absolute;
    top: 0; left: -100%; width: 300%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.9), transparent);
    animation: shimmer 4s linear infinite;
}}
.hero-badge {{
    display: inline-block;
    background: rgba(255,255,255,0.4);
    border: 1px solid rgba(255,255,255,0.6);
    border-radius: 99px;
    padding: 3px 16px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.7rem;
    backdrop-filter: blur(8px);
}}
.hero-title {{
    font-size: 2.7rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #1a1a2e;
    margin: 0 0 0.4rem;
    line-height: 1;
}}
.hero-title span {{ color: {acc}; }}
.hero-sub {{ font-size: 0.88rem; color: rgba(0,0,0,0.38); font-weight: 400; margin: 0; }}

/* ── Cards ── */
.g-card {{
    padding: 1.4rem 1.8rem;
    margin-bottom: 0.85rem;
    position: relative;
    overflow: hidden;
    animation: fadeUp 0.5s ease both;
}}
.g-card::after {{
    content: '';
    position: absolute;
    inset: 0; border-radius: 24px;
    background: linear-gradient(135deg, rgba(255,255,255,0.4) 0%, transparent 60%);
    pointer-events: none;
}}
.g-card-accent {{ border-left: 3px solid {acc} !important; }}
.g-card-green  {{ border-left: 3px solid #10b981 !important; }}

.chip-label {{
    font-size: 0.67rem; font-weight: 700;
    letter-spacing: 1.8px; text-transform: uppercase;
    color: {acc}; margin-bottom: 0.4rem; display: block; opacity: 0.75;
}}
.chip-label-green {{ color: #10b981; opacity: 1; }}

.food-name {{ font-size: 1.9rem; font-weight: 700; color: #1a1a2e; letter-spacing: -0.5px; line-height: 1.2; }}
.cal-number {{ font-size: 3rem; font-weight: 800; color: #10b981; letter-spacing: -2px; line-height: 1; }}
.cal-unit {{ font-size: 0.95rem; color: rgba(0,0,0,0.3); margin-left: 4px; font-weight: 300; }}

/* ── Nutrition grid ── */
.nut-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 0.8rem; }}
.nut-cell {{
    background: rgba(255,255,255,0.45);
    border: 1px solid rgba(255,255,255,0.65);
    border-radius: 16px;
    padding: 0.9rem 0.4rem;
    text-align: center;
    backdrop-filter: blur(12px);
    transition: background 0.25s, transform 0.25s, box-shadow 0.25s;
}}
.nut-cell:hover {{
    background: rgba(255,255,255,0.75);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
}}
.nut-icon {{ font-size: 1.4rem; }}
.nut-val {{ font-size: 1.05rem; font-weight: 700; color: #1a1a2e; margin: 4px 0 2px; }}
.nut-name {{ font-size: 0.6rem; font-weight: 600; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(0,0,0,0.35); }}

/* ── Tags ── */
.tag-wrap {{ display: flex; flex-wrap: wrap; gap: 7px; margin-top: 0.7rem; }}
.tag {{
    background: rgba(255,255,255,0.5);
    border: 1px solid rgba(255,255,255,0.7);
    border-radius: 99px;
    padding: 5px 16px;
    font-size: 0.83rem;
    color: #444;
    backdrop-filter: blur(8px);
    transition: background 0.2s, color 0.2s, transform 0.2s;
}}
.tag:hover {{ background: rgba(255,255,255,0.85); color: {acc}; transform: translateY(-2px); }}

/* ── Donut ── */
.donut-wrap {{ display: flex; align-items: center; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap; }}
.donut-legend {{ display: flex; flex-direction: column; gap: 9px; }}
.legend-item {{ display: flex; align-items: center; gap: 9px; font-size: 0.83rem; color: rgba(0,0,0,0.55); }}
.legend-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
.legend-pct {{ font-weight: 700; color: #1a1a2e; margin-left: auto; padding-left: 12px; }}

/* ── Upload zone ── */
[data-testid="stFileUploadDropzone"] {{
    background: rgba(255,255,255,0.35) !important;
    border: 2px dashed rgba(255,255,255,0.6) !important;
    border-radius: 18px !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.25s !important;
}}
[data-testid="stFileUploadDropzone"]:hover {{
    background: rgba(255,255,255,0.55) !important;
    border-color: {acc} !important;
}}
[data-testid="stFileUploadDropzone"] p {{ color: rgba(0,0,0,0.3) !important; }}

[data-testid="stImage"] img {{
    border-radius: 20px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
    border: 1px solid rgba(255,255,255,0.6) !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input {{
    background: rgba(255,255,255,0.55) !important;
    border: 1.5px solid rgba(255,255,255,0.75) !important;
    border-radius: 12px !important;
    color: #1a1a2e !important;
    font-family: 'Outfit', sans-serif !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.25s !important;
}}
.stTextInput > div > div > input::placeholder {{ color: rgba(0,0,0,0.25) !important; }}
.stTextInput > div > div > input:focus {{
    border-color: {acc} !important;
    background: rgba(255,255,255,0.8) !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.1) !important;
}}
.stTextInput label {{
    color: rgba(0,0,0,0.4) !important; font-size: 0.68rem !important;
    font-weight: 700 !important; letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: rgba(255,255,255,0.5) !important;
    border: 1.5px solid rgba(255,255,255,0.75) !important;
    color: #555 !important;
    border-radius: 99px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    backdrop-filter: blur(12px) !important;
    transition: all 0.25s !important;
}}
.stButton > button:hover {{
    background: rgba(255,255,255,0.8) !important;
    border-color: {acc} !important;
    color: {acc} !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
}}

div.scan-btn > div > button {{
    background: {acc} !important;
    border: none !important;
    border-radius: 16px !important;
    color: white !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 6px 24px rgba(124,58,237,0.3) !important;
    transition: all 0.25s !important;
    backdrop-filter: none !important;
}}
div.scan-btn > div > button:hover {{
    opacity: 0.9 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(124,58,237,0.4) !important;
}}

/* ── Progress ── */
.stProgress > div > div {{ background: {acc} !important; border-radius: 99px !important; transition: width 0.4s ease !important; }}
.stProgress > div {{ background: rgba(255,255,255,0.4) !important; border-radius: 99px !important; height: 5px !important; backdrop-filter: blur(8px) !important; }}

.stAlert {{
    background: rgba(255,245,245,0.7) !important;
    border: 1px solid rgba(254,226,226,0.8) !important;
    border-radius: 14px !important;
    color: #dc2626 !important;
    backdrop-filter: blur(12px) !important;
}}

/* ── User bar ── */
.user-bar {{
    border-radius: 16px;
    padding: 0.75rem 1.2rem;
    margin-bottom: 1rem;
    display: flex; align-items: center; justify-content: space-between;
    font-size: 0.85rem; color: rgba(0,0,0,0.5);
    animation: fadeUp 0.4s ease both;
}}
.user-email {{ font-weight: 600; color: #1a1a2e; }}

.page-footer {{
    text-align: center; margin-top: 2.5rem; padding-bottom: 1rem;
    font-size: 0.72rem; color: rgba(0,0,0,0.25); letter-spacing: 0.3px;
}}
</style>
""", unsafe_allow_html=True)

# ── Hero ──
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    try:
        st.image("SnackScan.jpg", width=72)
    except:
        pass

st.markdown(f"""
<div class="glass hero-wrap">
    <div class="hero-badge">AI Powered · Cambodia</div>
    <div class="hero-title">SnackScan<span>KH</span></div>
    <p class="hero-sub">{t("Snap a photo. Know your food.", "ថតរូបភាព។ ស្គាល់ម្ហូបរបស់អ្នក។")}</p>
</div>
""", unsafe_allow_html=True)

# ── Top bar ──
col1, col2, col3 = st.columns([5, 1, 1])
with col2:
    if st.button("🇰🇭 KM" if st.session_state.lang == "en" else "🇬🇧 EN"):
        st.session_state.lang = "km" if st.session_state.lang == "en" else "en"
with col3:
    if st.session_state.get("user"):
        if st.button("👤 Out"):
            st.session_state.user = None
            st.rerun()
    else:
        if st.button("👤 In"):
            st.switch_page("pages/login.py")

# ── User badge ──
if st.session_state.get("user"):
    email = st.session_state.user.get("email", "")
    st.markdown(f"""
    <div class="glass user-bar">
        <span>👋 Signed in as <span class="user-email">{email}</span></span>
    </div>
    """, unsafe_allow_html=True)

# ── Gemini client ──
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# ── Upload ──
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

    if scan_clicked:
        if not st.session_state.get("user"):
            st.switch_page("pages/login.py")
            st.stop()

        st.session_state.result = None
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

# ── Results ──
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
    <div class="glass g-card g-card-accent">
        <span class="chip-label">🍽 {t("Detected Food", "ម្ហូបដែលបានរកឃើញ")}</span>
        <div class="food-name">{food}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="glass g-card g-card-green">
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
        <div class="glass g-card">
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
            <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.4)" stroke-width="{stroke}"/>
            {''.join(segments)}
            <text x="{cx}" y="{cy-8}" text-anchor="middle" fill="#1a1a2e" font-size="13" font-weight="700" font-family="Outfit">{t("Macros","ម៉ាក្រូ")}</text>
            <text x="{cx}" y="{cy+10}" text-anchor="middle" fill="rgba(0,0,0,0.3)" font-size="10" font-family="Outfit">{t("breakdown","ចំណែក")}</text>
        </svg>"""

        legend = "".join(
            f'<div class="legend-item"><div class="legend-dot" style="background:{c}"></div>'
            f'<span>{n}</span><span class="legend-pct">{cal/total_cal*100:.0f}%</span></div>'
            for n, cal, c in slices
        )
        st.markdown(f"""
        <div class="glass g-card">
            <span class="chip-label">🥧 {t("Macro Wheel", "កង់ម៉ាក្រូ")}</span>
            <div class="donut-wrap">{svg}<div class="donut-legend">{legend}</div></div>
        </div>""", unsafe_allow_html=True)

    if ingredients:
        tags = "".join(f'<span class="tag">{i}</span>' for i in ingredients)
        st.markdown(f"""
        <div class="glass g-card">
            <span class="chip-label">🥬 {t("Ingredients", "គ្រឿងផ្សំ")}</span>
            <div class="tag-wrap">{tags}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="page-footer">SnackScanKH · Made with ♥ in Phnom Penh</div>', unsafe_allow_html=True)
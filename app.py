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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

.stApp {
    background: radial-gradient(ellipse at 20% 20%, #1a0533 0%, #0d0d1a 40%, #000510 100%);
    min-height: 100vh;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 2.5rem; max-width: 720px; }

.hero-wrap {
    position: relative;
    text-align: center;
    padding: 2rem 2rem 1.8rem;
    margin-bottom: 1.5rem;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(120,60,255,0.18) 0%, rgba(30,20,80,0.55) 50%, rgba(0,180,255,0.10) 100%);
    border: 1px solid rgba(150,100,255,0.25);
    backdrop-filter: blur(24px);
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(130,60,255,0.25) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrap::after {
    content: '';
    position: absolute;
    bottom: -80px; right: -40px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,180,255,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(130,60,255,0.2);
    border: 1px solid rgba(150,100,255,0.35);
    border-radius: 99px;
    padding: 4px 16px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(180,140,255,0.9);
    margin-bottom: 0.8rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1;
    margin: 0 0 0.5rem;
    background: linear-gradient(135deg, #ffffff 0%, #c4a8ff 40%, #7af0ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.92rem;
    font-weight: 300;
    color: rgba(255,255,255,0.4);
    margin: 0;
}
.g-card {
    position: relative;
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 22px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(20px);
    overflow: hidden;
}
.g-card::before {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.g-card-accent { border-color: rgba(130,60,255,0.35); }
.g-card-green  { border-color: rgba(50,210,120,0.35); }
.chip-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    color: rgba(160,120,255,0.75);
    margin-bottom: 0.5rem;
}
.chip-label-green { color: rgba(50,210,120,0.75); }
.food-name {
    font-size: 2rem;
    font-weight: 700;
    color: #f0ecff;
    line-height: 1.2;
    letter-spacing: -0.5px;
}
.cal-number {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #34d399, #7af0ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
}
.cal-unit {
    font-size: 1rem;
    color: rgba(255,255,255,0.3);
    font-weight: 300;
    margin-left: 6px;
    vertical-align: middle;
}
.nut-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-top: 0.8rem;
}
.nut-cell {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1rem 0.5rem 0.8rem;
    text-align: center;
    transition: background 0.2s, border-color 0.2s;
}
.nut-cell:hover {
    background: rgba(130,60,255,0.1);
    border-color: rgba(130,60,255,0.25);
}
.nut-icon { font-size: 1.5rem; line-height: 1; }
.nut-val { font-size: 1.15rem; font-weight: 700; color: #f0ecff; margin: 4px 0 2px; }
.nut-name { font-size: 0.65rem; font-weight: 500; letter-spacing: 1.2px; text-transform: uppercase; color: rgba(255,255,255,0.35); }
.tag-wrap { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 0.7rem; }
.tag {
    background: rgba(130,60,255,0.12);
    border: 1px solid rgba(130,60,255,0.28);
    border-radius: 99px;
    padding: 6px 18px;
    font-size: 0.85rem;
    color: rgba(210,190,255,0.9);
}
.donut-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.donut-svg { filter: drop-shadow(0 0 12px rgba(130,60,255,0.3)); }
.donut-legend { display: flex; flex-direction: column; gap: 10px; }
.legend-item { display: flex; align-items: center; gap: 10px; font-size: 0.85rem; color: rgba(255,255,255,0.75); }
.legend-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.legend-pct { font-weight: 700; color: #f0ecff; margin-left: auto; padding-left: 12px; }
[data-testid="stFileUploadDropzone"] {
    background: rgba(130,60,255,0.04) !important;
    border: 2px dashed rgba(130,60,255,0.3) !important;
    border-radius: 18px !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(130,60,255,0.55) !important;
    background: rgba(130,60,255,0.08) !important;
}
[data-testid="stFileUploadDropzone"] p { color: rgba(255,255,255,0.35) !important; }
[data-testid="stImage"] img {
    border-radius: 22px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    box-shadow: 0 16px 48px rgba(0,0,0,0.5) !important;
}
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(130,60,255,0.25) !important;
    border-radius: 14px !important;
    color: rgba(255,255,255,0.85) !important;
    font-family: 'Outfit', sans-serif !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(255,255,255,0.2) !important; }
.stTextInput > div > div > input:focus {
    border-color: rgba(130,60,255,0.6) !important;
    box-shadow: 0 0 0 3px rgba(130,60,255,0.12) !important;
}
.stTextInput label {
    color: rgba(160,120,255,0.7) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 1.8px !important;
    text-transform: uppercase !important;
}
.stButton > button {
    background: rgba(130,60,255,0.15) !important;
    border: 1px solid rgba(130,60,255,0.35) !important;
    color: rgba(210,185,255,0.95) !important;
    border-radius: 99px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
}
.stButton > button:hover { background: rgba(130,60,255,0.28) !important; }
div.scan-btn > div > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4338ca 100%) !important;
    border: none !important;
    border-radius: 18px !important;
    color: white !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    box-shadow: 0 6px 28px rgba(124,58,237,0.45), inset 0 1px 0 rgba(255,255,255,0.15) !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, #7c3aed, #a78bfa, #7af0ff) !important;
    border-radius: 99px !important;
}
.stProgress > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 99px !important;
    height: 6px !important;
}
.stAlert {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: 14px !important;
    color: #fca5a5 !important;
}
.about-wrap {
    position: relative;
    margin-top: 3rem;
    border-radius: 28px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(24px);
    padding: 2.5rem 2rem 2rem;
    text-align: center;
    animation: fadeUp 0.7s ease both;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
.about-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 300%; height: 1px;
    background: linear-gradient(90deg, transparent 0%, rgba(130,60,255,0.8) 30%, rgba(122,240,255,0.8) 50%, rgba(130,60,255,0.8) 70%, transparent 100%);
    animation: shimmer-line 4s linear infinite;
}
@keyframes shimmer-line {
    0%   { transform: translateX(0); }
    100% { transform: translateX(33.33%); }
}
.about-orb1 {
    position: absolute; width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(130,60,255,0.12) 0%, transparent 70%);
    top: -60px; left: -60px;
    animation: float1 6s ease-in-out infinite; pointer-events: none;
}
.about-orb2 {
    position: absolute; width: 160px; height: 160px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,180,255,0.1) 0%, transparent 70%);
    bottom: -40px; right: -40px;
    animation: float2 7s ease-in-out infinite; pointer-events: none;
}
@keyframes float1 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(15px,20px)} }
@keyframes float2 { 0%,100%{transform:translate(0,0)} 50%{transform:translate(-12px,-18px)} }
.avatar-ring {
    width: 88px; height: 88px; border-radius: 50%;
    margin: 0 auto 1.2rem;
    display: flex; align-items: center; justify-content: center;
    position: relative; font-size: 2.2rem;
    background: rgba(130,60,255,0.12);
}
.avatar-ring::after {
    content: ''; position: absolute; inset: -2px; border-radius: 50%;
    background: linear-gradient(135deg, #7c3aed, #7af0ff, #7c3aed);
    background-size: 200% 200%; z-index: -1;
    animation: spin-gradient 4s linear infinite;
}
@keyframes spin-gradient {
    0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}
}
.about-name { font-size: 1.35rem; font-weight: 700; color: #f0ecff; margin: 0 0 0.3rem; }
.about-bio { font-size: 0.9rem; font-weight: 300; color: rgba(255,255,255,0.45); margin: 0 0 1.4rem; line-height: 1.6; }
.about-stats { display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.6rem; padding-bottom: 1.4rem; border-bottom: 1px solid rgba(255,255,255,0.07); }
.stat-item { text-align: center; }
.stat-val {
    font-size: 1.2rem; font-weight: 700;
    background: linear-gradient(135deg, #c4a8ff, #7af0ff);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; display: block;
}
.stat-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px; color: rgba(255,255,255,0.3); font-weight: 500; }
.color-row { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 1.4rem; flex-wrap: wrap; }
.color-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1.5px; color: rgba(255,255,255,0.3); font-weight: 500; width: 100%; text-align: center; margin-bottom: 4px; }
.color-dot { width: 26px; height: 26px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.15); transition: transform 0.2s, border-color 0.2s; display: inline-block; }
.color-dot:hover { transform: scale(1.25); border-color: rgba(255,255,255,0.5); }
.gh-link {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12);
    border-radius: 99px; padding: 8px 20px; font-size: 0.85rem; font-weight: 500;
    color: rgba(255,255,255,0.7); text-decoration: none;
    transition: background 0.2s, border-color 0.2s, color 0.2s;
}
.gh-link:hover { background: rgba(130,60,255,0.18); border-color: rgba(130,60,255,0.45); color: rgba(210,185,255,0.95); text-decoration: none; }
.about-footer { margin-top: 1.6rem; font-size: 0.7rem; color: rgba(255,255,255,0.18); letter-spacing: 0.5px; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for k, v in {"lang": "en", "result": None, "image": None, "last_hint": ""}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def t(en, km):
    return km if st.session_state.lang == "km" else en

# ── Hero ──
col_l, col_c, col_r = st.columns([1, 3, 1])
with col_c:
    try:
        st.image("SnackScan.jpg", width=80)
    except:
        pass

st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-badge">✦ AI Powered · Cambodia</div>
    <div class="hero-title">SnackScan<span style="color:rgba(122,240,255,0.85)">KH</span></div>
    <p class="hero-sub">{t("Snap a photo. Know your food.", "ថតរូបភាព។ ស្គាល់ម្ហូបរបស់អ្នក។")}</p>
</div>
""", unsafe_allow_html=True)

# ── Lang toggle ──
col1, col2 = st.columns([6, 1])
with col2:
    if st.button("🇰🇭 KM" if st.session_state.lang == "en" else "🇬🇧 EN"):
        st.session_state.lang = "km" if st.session_state.lang == "en" else "en"

# ── Client ──
@st.cache_resource
def get_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = get_client()

# ── Upload ──
uploaded_file = st.file_uploader(
    t("Drop your food photo here", "ទម្លាក់រូបភាពម្ហូបរបស់អ្នកនៅទីនេះ"),
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

hint = st.text_input(
    t("TELL US MORE (OPTIONAL)", "បញ្ជាក់បន្ថែម (ជាជម្រើស)"),
    placeholder=t('e.g. "whole milk", "brown rice", "grilled chicken breast"',
                  'ឧ. "ទឹកដោះគោទាំងមូល", "បាយស្វាយចន្ទី", "សាច់មាន់អាំង"')
)

if uploaded_file:
    img = Image.open(uploaded_file)
    st.session_state.image = img
    st.image(img, use_container_width=True)

    st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
    scan_clicked = st.button(t("🔍   Scan Food", "🔍   វិភាគម្ហូប"), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if scan_clicked:
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
            text = response.text.replace("json", "").replace("", "").strip()
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
    <div class="g-card g-card-accent">
        <div class="chip-label">🍽 {t("Detected Food", "ម្ហូបដែលបានរកឃើញ")}</div>
        <div class="food-name">{food}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="g-card g-card-green">
        <div class="chip-label chip-label-green">🔥 {t("Estimated Calories", "កាឡូរីដែលប៉ាន់ស្មាន")}</div>
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
        <div class="g-card">
            <div class="chip-label">🧬 {t("Nutrition Breakdown", "តម្លៃអាហារូបត្ថម្ភ")}</div>
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
        colors = ["#a78bfa", "#34d399", "#f97316", "#60a5fa", "#f472b6"]
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

        svg = f"""<svg width="180" height="180" viewBox="0 0 180 180" class="donut-svg">
            <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="{stroke}"/>
            {''.join(segments)}
            <text x="{cx}" y="{cy-8}" text-anchor="middle" fill="rgba(255,255,255,0.9)" font-size="14" font-weight="700" font-family="Outfit">{t("Macros","ម៉ាក្រូ")}</text>
            <text x="{cx}" y="{cy+12}" text-anchor="middle" fill="rgba(255,255,255,0.4)" font-size="10" font-family="Outfit">{t("breakdown","ចំណែក")}</text>
        </svg>"""

        legend = "".join(
            f'<div class="legend-item"><div class="legend-dot" style="background:{c}"></div>'
            f'<span>{n}</span><span class="legend-pct">{cal/total_cal*100:.0f}%</span></div>'
            for n, cal, c in slices
        )
        st.markdown(f"""
        <div class="g-card">
            <div class="chip-label">🥧 {t("Macro Wheel", "កង់ម៉ាក្រូ")}</div>
            <div class="donut-wrap">{svg}<div class="donut-legend">{legend}</div></div>
        </div>""", unsafe_allow_html=True)

    if ingredients:
        tags = "".join(f'<span class="tag">{i}</span>' for i in ingredients)
        st.markdown(f"""
        <div class="g-card">
            <div class="chip-label">🥬 {t("Ingredients", "គ្រឿងផ្សំ")}</div>
            <div class="tag-wrap">{tags}</div>
        </div>""", unsafe_allow_html=True)

# ── About ──
st.markdown("""
<div class="about-wrap">
    <div class="about-orb1"></div>
    <div class="about-orb2"></div>
    <div class="avatar-ring">👨‍💻</div>
    <div class="about-name">Than Vireakseth</div>
    <div class="about-bio">
        A student developer from Cambodia 🇰🇭<br>
        <span style="color:rgba(160,120,255,0.6);font-size:0.82rem;">Building things with AI, one scan at a time.</span>
    </div>
    <div class="about-stats">
        <div class="stat-item"><span class="stat-val">Gemini</span><span class="stat-label">AI Model</span></div>
        <div class="stat-item"><span class="stat-val">2</span><span class="stat-label">Languages</span></div>
        <div class="stat-item"><span class="stat-val">6</span><span class="stat-label">Nutrients</span></div>
    </div>
    <div class="color-row">
        <div class="color-label">✦ Accent Colors</div>
        <div class="color-dot" style="background:linear-gradient(135deg,#7c3aed,#4338ca)"></div>
        <div class="color-dot" style="background:linear-gradient(135deg,#0ea5e9,#06b6d4)"></div>
        <div class="color-dot" style="background:linear-gradient(135deg,#f97316,#ef4444)"></div>
        <div class="color-dot" style="background:linear-gradient(135deg,#10b981,#34d399)"></div>
        <div class="color-dot" style="background:linear-gradient(135deg,#ec4899,#a855f7)"></div>
        <div class="color-dot" style="background:linear-gradient(135deg,#f59e0b,#fbbf24)"></div>
    </div>
    <a class="gh-link" href="https://github.com/ReaX3ops" target="_blank">⌥ github.com/ReaX3ops</a>
    <div class="about-footer">Made with ♥ in Phnom Penh · SnackScanKH © 2026</div>
</div>
""", unsafe_allow_html=True)
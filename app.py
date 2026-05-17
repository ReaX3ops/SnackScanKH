import streamlit as st
from google import genai
from PIL import Image
import json
import time

# ─────────────────────────────
# PAGE CONFIG
# ─────────────────────────────

st.set_page_config(
    page_title="SnackScanKH",
    page_icon="🍱",
    layout="centered"
)

# ─────────────────────────────
# LIGHT APPLE UI
# ─────────────────────────────

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

:root{

    --accent:#7c3aed;
    --accent2:#8b5cf6;

    --bg1:#f8faff;
    --bg2:#eef4ff;

    --card:rgba(255,255,255,0.72);

    --border:rgba(120,120,180,0.12);

    --text:#111827;
    --sub:#6b7280;
}

*{
    font-family:'Outfit',sans-serif;
    box-sizing:border-box;
}

.stApp{

    background:
    radial-gradient(circle at top left,
    rgba(124,58,237,0.10),
    transparent 30%),

    radial-gradient(circle at bottom right,
    rgba(59,130,246,0.10),
    transparent 30%),

    linear-gradient(
    180deg,
    var(--bg1),
    var(--bg2));

    min-height:100vh;
}

#MainMenu,
footer,
header{
    visibility:hidden;
}

.block-container{
    max-width:760px;
    padding-top:2rem;
}

.hero-wrap{

    position:relative;

    text-align:center;

    padding:2.5rem;

    border-radius:32px;

    background:rgba(255,255,255,0.72);

    border:1px solid var(--border);

    backdrop-filter:blur(24px);

    box-shadow:
    0 10px 40px rgba(0,0,0,0.06);

    margin-bottom:1.5rem;

    overflow:hidden;
}

.hero-title{

    font-size:3rem;

    font-weight:800;

    line-height:1;

    margin-bottom:0.5rem;

    letter-spacing:-2px;

    background:
    linear-gradient(
    135deg,
    var(--accent),
    var(--accent2));

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;
}

.hero-sub{

    color:var(--sub);

    font-size:1rem;

    font-weight:400;
}

.g-card{

    background:var(--card);

    border:1px solid var(--border);

    border-radius:28px;

    padding:1.5rem;

    margin-bottom:1rem;

    backdrop-filter:blur(24px);

    box-shadow:
    0 10px 30px rgba(0,0,0,0.05);

    transition:0.25s;
}

.g-card:hover{

    transform:translateY(-2px);

    box-shadow:
    0 18px 40px rgba(124,58,237,0.10);
}

.food-name{

    font-size:2rem;

    font-weight:700;

    color:var(--text);
}

.calories{

    font-size:3rem;

    font-weight:800;

    background:
    linear-gradient(
    135deg,
    var(--accent),
    var(--accent2));

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;
}

.label{

    font-size:0.75rem;

    letter-spacing:2px;

    text-transform:uppercase;

    color:var(--sub);

    font-weight:600;

    margin-bottom:0.6rem;
}

.ingredients{

    display:flex;

    flex-wrap:wrap;

    gap:8px;

    margin-top:1rem;
}

.tag{

    background:
    rgba(124,58,237,0.08);

    border:
    1px solid rgba(124,58,237,0.14);

    color:var(--accent);

    border-radius:999px;

    padding:8px 16px;

    font-size:0.85rem;

    font-weight:500;
}

.stButton > button{

    width:100%;

    border:none !important;

    border-radius:18px !important;

    background:
    linear-gradient(
    135deg,
    var(--accent),
    var(--accent2)
    ) !important;

    color:white !important;

    font-weight:700 !important;

    padding:0.9rem 1rem !important;

    font-size:1rem !important;

    box-shadow:
    0 10px 30px rgba(124,58,237,0.20);

    transition:0.25s;
}

.stButton > button:hover{

    transform:translateY(-2px) scale(1.01);
}

.stTextInput input{

    background:rgba(255,255,255,0.8) !important;

    border:1px solid var(--border) !important;

    border-radius:16px !important;

    color:var(--text) !important;
}

[data-testid="stFileUploadDropzone"]{

    background:rgba(255,255,255,0.55);

    border:2px dashed rgba(124,58,237,0.18);

    border-radius:24px;

    padding:2rem;
}

[data-testid="stImage"] img{

    border-radius:28px;

    border:1px solid rgba(255,255,255,0.8);

    box-shadow:
    0 15px 45px rgba(0,0,0,0.10);
}

.accent-picker{

    margin-bottom:1rem;
}

.about{

    text-align:center;

    padding:2rem;

    color:var(--sub);

    font-size:0.9rem;
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# SESSION
# ─────────────────────────────

for k, v in {
    "lang":"en",
    "result":None,
    "image":None
}.items():

    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────
# TRANSLATE
# ─────────────────────────────

def t(en, km):
    return km if st.session_state.lang == "km" else en

# ─────────────────────────────
# ACCENT PICKER
# ─────────────────────────────

accent_map = {

    "Purple":("#7c3aed","#8b5cf6"),

    "Blue":("#2563eb","#3b82f6"),

    "Pink":("#db2777","#ec4899"),

    "Green":("#059669","#10b981"),

    "Orange":("#ea580c","#f97316")
}

accent = st.selectbox(
    "Accent",
    list(accent_map.keys()),
    label_visibility="collapsed"
)

primary, secondary = accent_map[accent]

st.markdown(f"""
<style>

:root{{
    --accent:{primary};
    --accent2:{secondary};
}}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────
# HERO
# ─────────────────────────────

st.markdown(f"""
<div class="hero-wrap">

    <div class="hero-title">
        SnackScanKH
    </div>

    <div class="hero-sub">
        {t("Scan your food with AI", "ស្កេនម្ហូបរបស់អ្នកជាមួយ AI")}
    </div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────
# LANGUAGE
# ─────────────────────────────

col1, col2 = st.columns([6,1])

with col2:

    if st.button("🇰🇭 KM" if st.session_state.lang == "en" else "🇬🇧 EN"):

        st.session_state.lang = (
            "km"
            if st.session_state.lang == "en"
            else "en"
        )

# ─────────────────────────────
# GEMINI
# ─────────────────────────────

@st.cache_resource
def get_client():
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

client = get_client()

# ─────────────────────────────
# UPLOAD
# ─────────────────────────────

uploaded_file = st.file_uploader(
    t(
        "Upload food image",
        "បញ្ចូលរូបភាពម្ហូប"
    ),
    type=["jpg","jpeg","png","webp"]
)

hint = st.text_input(
    t(
        "Optional Hint",
        "ព័ត៌មានបន្ថែម"
    )
)

# ─────────────────────────────
# IMAGE
# ─────────────────────────────

if uploaded_file:

    img = Image.open(uploaded_file)

    st.session_state.image = img

    st.image(img, use_container_width=True)

    if st.button(
        t(
            "🔍 Scan Food",
            "🔍 ស្កេនម្ហូប"
        )
    ):

        progress = st.progress(
            0,
            text=t(
                "Analyzing...",
                "កំពុងវិភាគ..."
            )
        )

        for i in range(100):

            time.sleep(0.01)

            progress.progress(i + 1)

        prompt = f"""
Analyze this food image.

Return ONLY valid JSON.

{{
"food_en":"food name",
"food_km":"food name in Khmer",
"calories":"estimated calories",
"ingredients_en":["ingredient1"],
"ingredients_km":["ingredient1"]
}}
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt, img]
            )

            text = (
                response.text
                .replace("```json","")
                .replace("```","")
                .strip()
            )

            st.session_state.result = json.loads(text)

            progress.empty()

        except Exception as e:

            st.error(str(e))

# ─────────────────────────────
# RESULTS
# ─────────────────────────────

if st.session_state.result:

    data = st.session_state.result

    lang = st.session_state.lang

    food = data.get(
        "food_km"
        if lang == "km"
        else "food_en",
        "មិនដឹង"
        if lang == "km"
        else "Unknown"
    )

    calories = data.get("calories","?")

    ingredients = data.get(
        "ingredients_km"
        if lang == "km"
        else "ingredients_en",
        []
    )

    st.markdown(f"""
    <div class="g-card">

        <div class="label">
            🍔 {t("Food","ម្ហូប")}
        </div>

        <div class="food-name">
            {food}
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="g-card">

        <div class="label">
            🔥 {t("Calories","កាឡូរី")}
        </div>

        <div class="calories">
            {calories}
        </div>

    </div>
    """, unsafe_allow_html=True)

    tags = "".join([
        f'<span class="tag">{i}</span>'
        for i in ingredients
    ])

    st.markdown(f"""
    <div class="g-card">

        <div class="label">
            🥗 {t("Ingredients","គ្រឿងផ្សំ")}
        </div>

        <div class="ingredients">
            {tags}
        </div>

    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────
# ABOUT
# ─────────────────────────────

st.markdown(f"""
<div class="about">

Made with ♥ in Cambodia 🇰🇭

</div>
""", unsafe_allow_html=True)
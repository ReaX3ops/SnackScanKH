import streamlit as st

st.set_page_config(page_title="About · SnackScanKH", page_icon="👨‍💻", layout="centered")

# Pull accent from session state (defaults to purple if coming fresh)
acc = st.session_state.get("accent", "#7c3aed")
acc_rgb = {
    "#7c3aed": "124,58,237",
    "#0ea5e9": "14,165,233",
    "#f97316": "249,115,22",
    "#10b981": "16,185,129",
    "#ec4899": "236,72,153",
    "#f59e0b": "245,158,11",
}
rgb = acc_rgb.get(acc, "124,58,237")

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Outfit', sans-serif; }}
.stApp {{ background: linear-gradient(160deg, #f0f0ff 0%, #fafafa 40%, #f5f0ff 100%); }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 2.5rem; max-width: 720px; }}

/* paste in your .about-wrap, .avatar-ring, .about-stats, etc. styles here */
.about-wrap {{
    position: relative; border-radius: 28px; overflow: hidden;
    border: 1px solid rgba({rgb},0.15); background: rgba(255,255,255,0.75);
    backdrop-filter: blur(24px); padding: 2.5rem 2rem 2rem;
    text-align: center; box-shadow: 0 4px 32px rgba({rgb},0.08);
}}
.avatar-ring {{
    width: 88px; height: 88px; border-radius: 50%;
    margin: 0 auto 1.2rem; display: flex; align-items: center;
    justify-content: center; position: relative; font-size: 2.2rem;
    background: rgba({rgb},0.08);
}}
.avatar-ring::after {{
    content: ''; position: absolute; inset: -2px; border-radius: 50%;
    background: linear-gradient(135deg, {acc}, rgba({rgb},0.3), {acc});
    background-size: 200% 200%; z-index: -1;
    animation: spin-gradient 4s linear infinite;
}}
@keyframes spin-gradient {{
    0%{{background-position:0% 50%}} 50%{{background-position:100% 50%}} 100%{{background-position:0% 50%}}
}}
.about-name {{ font-size: 1.35rem; font-weight: 700; color: #1a1a2e; margin: 0 0 0.3rem; }}
.about-bio {{ font-size: 0.9rem; color: rgba(0,0,0,0.45); margin: 0 0 1.4rem; line-height: 1.6; }}
.about-stats {{ display: flex; justify-content: center; gap: 2rem; margin-bottom: 1.6rem;
    padding-bottom: 1.4rem; border-bottom: 1px solid rgba({rgb},0.1); }}
.stat-item {{ text-align: center; }}
.stat-val {{ font-size: 1.2rem; font-weight: 700; color: {acc}; display: block; }}
.stat-label {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.2px;
    color: rgba(0,0,0,0.35); font-weight: 500; }}
.gh-link {{
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba({rgb},0.06); border: 1px solid rgba({rgb},0.2);
    border-radius: 99px; padding: 8px 20px; font-size: 0.85rem; font-weight: 500;
    color: {acc}; text-decoration: none;
}}
.gh-link:hover {{ background: rgba({rgb},0.12); color: {acc}; text-decoration: none; }}
.about-footer {{ margin-top: 1.6rem; font-size: 0.7rem; color: rgba(0,0,0,0.25); }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="about-wrap">
    <div class="avatar-ring">👨‍💻</div>
    <div class="about-name">Than Vireakseth</div>
    <div class="about-bio">
        A student developer from Cambodia 🇰🇭<br>
        <span style="font-size:0.82rem;opacity:0.6;">Building things with AI, one scan at a time.</span>
    </div>
    <div class="about-stats">
        <div class="stat-item"><span class="stat-val">Gemini</span><span class="stat-label">AI Model</span></div>
        <div class="stat-item"><span class="stat-val">2</span><span class="stat-label">Languages</span></div>
        <div class="stat-item"><span class="stat-val">6</span><span class="stat-label">Nutrients</span></div>
    </div>
    <a class="gh-link" href="https://github.com/ReaX3ops" target="_blank">⌥ github.com/ReaX3ops</a>
    <div class="about-footer">Made with ♥ in Phnom Penh · SnackScanKH © 2026</div>
</div>
""", unsafe_allow_html=True)
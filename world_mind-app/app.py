import streamlit as st
import requests
import json

st.set_page_config(
    page_title="World Mind · AI News Summarizer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e6f0;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 20%, #1a0a2e 0%, #0a0a0f 50%, #0a1a1f 100%);
}

[data-testid="stSidebar"] {
    background: #0d0d18 !important;
    border-right: 1px solid #1e1e3a;
}

.main-banner {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}

.main-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 50%;
    transform: translateX(-50%);
    width: 600px; height: 200px;
    background: radial-gradient(ellipse, rgba(120, 60, 255, 0.15) 0%, transparent 70%);
    pointer-events: none;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.5rem, 5vw, 4rem);
    font-weight: 900;
    background: linear-gradient(135deg, #ffffff 0%, #c084fc 40%, #67e8f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.5rem;
}

.main-subtitle {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 300;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #3b0764, #0891b2, transparent);
    margin: 1.5rem auto;
    max-width: 600px;
}

.category-label {
    text-align: center;
    font-size: 0.75rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 1rem;
    font-weight: 500;
}

/* Category buttons */
div[data-testid="column"] .stButton > button {
    width: 100%;
    padding: 1.1rem 1.5rem;
    border: none;
    border-radius: 12px;
    font-family: 'DM Sans', sans-serif;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

/* Query input */
.stTextInput > div > div > input {
    background: #111127 !important;
    border: 1px solid #2d2d5a !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.9rem 1.2rem !important;
    transition: border-color 0.2s;
}

.stTextInput > div > div > input:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.15) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #374151 !important;
}

/* Generate button */
.generate-btn .stButton > button {
    background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.9rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
}

.generate-btn .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 15px 35px rgba(124, 58, 237, 0.35) !important;
    opacity: 0.92 !important;
}

.summary-card {
    background: linear-gradient(135deg, #111127 0%, #0d1a2a 100%);
    border: 1px solid #1e1e3a;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}

.summary-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #7c3aed, #0891b2, #10b981);
}

.summary-header {
    font-size: 0.7rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 1.2rem;
    font-weight: 500;
}

.summary-text {
    font-size: 1rem;
    line-height: 1.8;
    color: #d1d5db;
    font-weight: 300;
}

.error-card {
    background: #1a0a0a;
    border: 1px solid #7f1d1d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 1rem;
    color: #fca5a5;
    font-size: 0.9rem;
}

.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #c084fc;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e3a;
}

.query-chip {
    background: #111127;
    border: 1px solid #2d2d5a;
    border-radius: 8px;
    padding: 0.5rem 0.8rem;
    font-size: 0.82rem;
    color: #9ca3af;
    margin-bottom: 0.4rem;
    cursor: pointer;
    transition: all 0.2s;
    display: block;
    width: 100%;
    text-align: left;
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #10b981;
    display: inline-block;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

label[data-testid="stWidgetLabel"] {
    color: #6b7280 !important;
    font-size: 0.8rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

[data-testid="stSpinner"] { color: #7c3aed !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">📡 Quick Queries</div>', unsafe_allow_html=True)
    examples = [
        "Latest AI breakthroughs 2024",
        "Global climate change updates",
        "Stock market news today",
        "Space exploration recent news",
        "Cybersecurity threats 2024",
        "Electric vehicle industry news",
    ]
    for ex in examples:
        st.markdown(f'<div class="query-chip">↗ {ex}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">⚙️ System</div>', unsafe_allow_html=True)
    st.markdown(
        '<span class="status-dot"></span><span style="font-size:0.8rem;color:#6b7280;">RAG Pipeline Active</span>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div style="margin-top:0.5rem;font-size:0.75rem;color:#374151;">Tavily → ChromaDB → Gemini</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    backend_url = st.text_input("Backend URL", value="http://localhost:8000", label_visibility="visible")

# ── Main Banner ──────────────────────────────────────────
st.markdown("""
<div class="main-banner">
    <div class="main-title"> World Mind</div>
    <div class="main-subtitle">Real-time intelligence · RAG powered</div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────
if "query" not in st.session_state:
    st.session_state.query = ""
if "auto_run" not in st.session_state:
    st.session_state.auto_run = False

# ── Category Buttons ─────────────────────────────────────
st.markdown('<div class="category-label">Choose a category</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(135deg, #7f1d1d, #dc2626);
        color: white;
        box-shadow: 0 8px 25px rgba(220,38,38,0.25);
    }
    </style>""", unsafe_allow_html=True)
    if st.button("  Politics", use_container_width=True):
        st.session_state.query = "Latest world political crisis today"
        st.session_state.auto_run = True

with col2:
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #064e3b, #059669);
        color: white;
        box-shadow: 0 8px 25px rgba(5,150,105,0.25);
    }
    </style>""", unsafe_allow_html=True)
    if st.button("  Technology", use_container_width=True):
        st.session_state.query = "Latest technology changes in IT industry"
        st.session_state.auto_run = True

with col3:
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-child(3) .stButton > button {
        background: linear-gradient(135deg, #0c4a6e, #0284c7);
        color: white;
        box-shadow: 0 8px 25px rgba(2,132,199,0.25);
    }
    </style>""", unsafe_allow_html=True)
    if st.button("  Health Care", use_container_width=True):
        st.session_state.query = "New vaccine updates and healthcare news"
        st.session_state.auto_run = True

st.markdown("<br>", unsafe_allow_html=True)

# ── Query Input ──────────────────────────────────────────
query = st.text_input(
    "SEARCH QUERY",
    value=st.session_state.query,
    placeholder="e.g. Latest AI breakthroughs this week...",
)
st.session_state.query = query

st.markdown("<br>", unsafe_allow_html=True)

# ── Generate Button ──────────────────────────────────────
st.markdown('<div class="generate-btn">', unsafe_allow_html=True)
generate = st.button("✦ Generate Summary", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── API Call ─────────────────────────────────────────────
def fetch_summary(q: str, url: str) -> dict:
    resp = requests.post(
        f"{url}/summarize",
        json={"query": q},
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()

should_run = generate or st.session_state.auto_run
st.session_state.auto_run = False

if should_run:
    if not st.session_state.query.strip():
        st.warning("Please enter a query or click a category button.")
    else:
        with st.spinner("🔍 Searching the web & generating summary..."):
            try:
                result = fetch_summary(st.session_state.query.strip(), backend_url)
                summary = result.get("summary", "No summary returned.")
                st.markdown(f"""
                <div class="summary-card">
                    <div class="summary-header"> Summary · {st.session_state.query}</div>
                    <div class="summary-text">{summary.replace(chr(10), '<br>')}</div>
                </div>
                """, unsafe_allow_html=True)
            except requests.exceptions.ConnectionError:
                st.markdown("""
                <div class="error-card">
                ⚠️ <strong>Cannot connect to backend.</strong><br>
                Make sure the FastAPI server is running:<br>
                <code>cd backend && uvicorn main:app --reload --port 8000</code>
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f"""
                <div class="error-card">
                ⚠️ <strong>Error:</strong> {e}
                </div>
                """, unsafe_allow_html=True)

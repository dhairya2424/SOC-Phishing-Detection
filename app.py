import streamlit as st
import pandas as pd
import joblib, re, tldextract
from urllib.parse import urlparse
from difflib import SequenceMatcher

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="SOC Phishing Detection System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ======================================================
# CUSTOM CSS — Dark Glassmorphism Theme
# ======================================================

st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root variables ── */
:root {
    --bg-primary: #0a0e1a;
    --bg-card: rgba(15, 23, 42, 0.65);
    --bg-card-hover: rgba(20, 30, 55, 0.8);
    --glass-border: rgba(99, 102, 241, 0.15);
    --accent-gradient: linear-gradient(135deg, #6366f1, #8b5cf6, #a78bfa);
    --accent-primary: #818cf8;
    --accent-secondary: #a78bfa;
    --danger: #f87171;
    --danger-bg: rgba(248, 113, 113, 0.08);
    --success: #34d399;
    --success-bg: rgba(52, 211, 153, 0.08);
    --warning: #fbbf24;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --shadow-glow: 0 0 30px rgba(99, 102, 241, 0.08);
}

/* ── Global ── */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary);
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #0a0e1a 0%, #111827 40%, #0f172a 100%);
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%) !important;
    border-right: 1px solid var(--glass-border);
}

[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    background: var(--accent-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* ── Headings ── */
h1 {
    background: var(--accent-gradient) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    font-size: 2.2rem !important;
    padding-bottom: 0.3rem !important;
}

h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-card);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--glass-border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    padding: 10px 28px;
    font-weight: 500;
    color: var(--text-secondary);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stTabs [aria-selected="true"] {
    background: var(--accent-gradient) !important;
    color: #fff !important;
    font-weight: 600;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
}

.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}

.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ── Buttons ── */
.stButton > button,
.stFormSubmitButton > button {
    background: var(--accent-gradient) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.01em;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25) !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
}

.stButton > button:active,
.stFormSubmitButton > button:active {
    transform: translateY(0px) !important;
}

.stDownloadButton > button {
    background: linear-gradient(135deg, #059669, #10b981) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.25) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
[data-testid="stFileUploader"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: border-color 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 2px rgba(129, 140, 248, 0.15) !important;
}

/* ── Slider ── */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent-gradient) !important;
    border: 2px solid #fff !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: 14px;
    padding: 18px 20px;
    backdrop-filter: blur(12px);
    transition: all 0.3s ease;
    box-shadow: var(--shadow-glow);
}

[data-testid="stMetric"]:hover {
    background: var(--bg-card-hover);
    border-color: var(--accent-primary);
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(99, 102, 241, 0.12);
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    font-size: 0.7rem !important;
    letter-spacing: 0.08em;
}

[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--glass-border);
    box-shadow: var(--shadow-glow);
}

/* ── Alert boxes ── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
    backdrop-filter: blur(10px);
}

[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* ── JSON viewer ── */
[data-testid="stJson"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
    padding: 16px !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div {
    background: var(--accent-gradient) !important;
    border-radius: 10px;
}

/* ── Divider ── */
hr {
    border-color: var(--glass-border) !important;
    opacity: 0.5;
}

/* ── Selectbox dropdown ── */
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 10px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: var(--text-muted);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--text-secondary);
}

/* ── Fade-in animation ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}

.block-container {
    animation: fadeInUp 0.5s ease-out;
}

/* ── Custom verdict cards ── */
.verdict-card {
    border-radius: 14px;
    padding: 20px 24px;
    margin: 12px 0;
    backdrop-filter: blur(12px);
    animation: fadeInUp 0.4s ease-out;
}
.verdict-phishing {
    background: var(--danger-bg);
    border: 1px solid rgba(248, 113, 113, 0.25);
    box-shadow: 0 0 25px rgba(248, 113, 113, 0.06);
}
.verdict-legit {
    background: var(--success-bg);
    border: 1px solid rgba(52, 211, 153, 0.25);
    box-shadow: 0 0 25px rgba(52, 211, 153, 0.06);
}
.verdict-card h3 {
    margin: 0 0 6px 0;
    font-size: 1.25rem;
}
.verdict-card p {
    margin: 0;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

/* ── Info pill ── */
.info-pill {
    display: inline-block;
    background: var(--bg-card);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    padding: 6px 16px;
    font-size: 0.82rem;
    color: var(--text-secondary);
    margin: 4px 4px 4px 0;
}
.info-pill strong {
    color: var(--accent-secondary);
}

/* ── Section header ── */
.section-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-muted);
    font-weight: 600;
    margin-bottom: 8px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SESSION STATE
# ======================================================

if "batch_results" not in st.session_state:
    st.session_state.batch_results = None
if "batch_evidence" not in st.session_state:
    st.session_state.batch_evidence = None
if "batch_run" not in st.session_state:
    st.session_state.batch_run = False

# ======================================================
# LOAD MODELS (Cached)
# ======================================================

@st.cache_resource
def load_models():
    return (
        joblib.load("models_new/tfidf.pkl"),
        joblib.load("models_new/logistic.pkl"),
        joblib.load("models_new/rf.pkl"),
        joblib.load("models_new/xgb.pkl"),
        joblib.load("models_new/thresholds.pkl"),
    )

tfidf, logistic, rf, xgb, thresholds = load_models()

# Warm PSL cache
tldextract.extract("google.com")

DEFAULT_THRESHOLDS = {
    "Logistic Regression": thresholds["log_th"],
    "Random Forest": thresholds["rf_th"],
    "XGBoost": thresholds["xgb_th"],
}

# ======================================================
# SIDEBAR CONTROLS
# ======================================================

with st.sidebar:
    st.markdown("## 🛡️ SOC Controls")
    st.markdown("---")

    st.markdown('<p class="section-label">Detection Engine</p>', unsafe_allow_html=True)
    model_mode = st.selectbox(
        "Select Detection Model",
        ["Logistic Regression", "Random Forest", "XGBoost"],
        label_visibility="collapsed",
    )

    st.markdown("")
    st.markdown('<p class="section-label">Confidence Threshold</p>', unsafe_allow_html=True)
    threshold = st.slider(
        f"Threshold — {model_mode}",
        0.0,
        1.0,
        float(DEFAULT_THRESHOLDS[model_mode]),
        0.01,
        label_visibility="collapsed",
    )

    # Show active config as pills
    st.markdown("---")
    st.markdown('<p class="section-label">Active Configuration</p>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="info-pill">Model: <strong>{model_mode}</strong></span>'
        f'<span class="info-pill">Threshold: <strong>{threshold:.3f}</strong></span>',
        unsafe_allow_html=True,
    )

# ======================================================
# FEATURE CONFIG
# ======================================================

BRANDS = [
    "google", "facebook", "amazon", "microsoft", "apple",
    "paypal", "netflix", "instagram", "linkedin", "twitter",
]

RISKY_TLDS = {"tk", "ml", "ga", "cf", "gq"}

KEYWORDS = [
    "login", "verify", "secure", "account",
    "update", "bank", "confirm", "signin",
]

BRAND_ALERT_TH = 0.8

# ======================================================
# FEATURE EXTRACTION
# ======================================================

def brand_similarity(domain):
    best = 0
    for b in BRANDS:
        best = max(best, SequenceMatcher(None, domain, b).ratio())
    return best

def keyword_score(url):
    url_lower = url.lower()
    return sum(k in url_lower for k in KEYWORDS)

def is_ip(domain):
    return int(bool(re.match(r"^(?:\d{1,3}\.){3}\d{1,3}$", domain)))

def extract_features(url):
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    subdomain = ext.subdomain

    feats = {
        "url_length": len(url),
        "num_dots": url.count("."),
        "num_hyphens": url.count("-"),
        "num_digits": sum(c.isdigit() for c in url),
        "has_https_token": int("https" in parsed.path.lower()),
        "is_ip": is_ip(parsed.netloc),
        "keyword_score": keyword_score(url),
        "brand_similarity": brand_similarity(ext.domain),
        "risky_tld": int(ext.suffix in RISKY_TLDS),
        "subdomain_count": 0 if subdomain == "" else subdomain.count(".") + 1,
    }

    return pd.DataFrame([feats]), ext

# ======================================================
# INFERENCE
# ======================================================

def get_probs(url):
    X = tfidf.transform([url])
    log_p = logistic.predict_proba(X)[0][1]

    struct, ext = extract_features(url)

    rf_p = rf.predict_proba(struct)[0][1]
    xgb_p = xgb.predict_proba(struct)[0][1]

    return log_p, rf_p, xgb_p, struct.iloc[0], ext

@st.cache_data(show_spinner=False)
def cached_probs(url):
    return get_probs(url)

def active_score(lp, rfp, xp):
    prob = {
        "Logistic Regression": lp,
        "Random Forest": rfp,
        "XGBoost": xp,
    }[model_mode]

    return prob, int(prob >= threshold)

def verdict_label(pred):
    return "⚠️ Phishing" if pred else "✅ Legitimate"

# ======================================================
# UI — HEADER
# ======================================================

st.title("🛡️ SOC Phishing Detection System")
st.caption("B2B Security Software · Real-time URL threat analysis powered by ensemble machine learning")

st.markdown("")

single_tab, batch_tab = st.tabs([
    "🔎  Single URL Investigation",
    "📂  Batch Investigation",
])

# ================= SINGLE URL =================

with single_tab:

    st.markdown("")
    st.subheader("🔎 Single URL Investigation")
    st.caption("Paste a suspicious URL below to analyse it against multiple detection models.")

    with st.form("single_form"):
        url = st.text_input(
            "Target URL",
            placeholder="https://example-suspicious-site.com/login/verify",
        )
        analyse = st.form_submit_button("⚡ Analyse URL", use_container_width=True)

    if analyse:
        if not url.strip():
            st.warning("⚠️ Please enter a URL to analyse.")
        else:
            with st.spinner("🔍 Running detection models…"):
                lp, rfp, xp, struct, ext = get_probs(url)
                score, pred = active_score(lp, rfp, xp)

            # ── Verdict card ──
            if pred:
                st.markdown(
                    f"""<div class="verdict-card verdict-phishing">
                        <h3 style="color: var(--danger);">⚠️ Phishing Detected</h3>
                        <p>Confidence Score: <strong style="color: var(--danger);">{score:.3f}</strong>
                        &nbsp;·&nbsp; Model: <strong>{model_mode}</strong>
                        &nbsp;·&nbsp; Threshold: <strong>{threshold:.3f}</strong></p>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""<div class="verdict-card verdict-legit">
                        <h3 style="color: var(--success);">✅ Legitimate</h3>
                        <p>Confidence Score: <strong style="color: var(--success);">{score:.3f}</strong>
                        &nbsp;·&nbsp; Model: <strong>{model_mode}</strong>
                        &nbsp;·&nbsp; Threshold: <strong>{threshold:.3f}</strong></p>
                    </div>""",
                    unsafe_allow_html=True,
                )

            st.markdown("")

            # ── Model Comparison & Evidence — two columns ──
            col_left, col_right = st.columns(2, gap="large")

            with col_left:
                st.markdown('<p class="section-label">Model Probability Comparison</p>', unsafe_allow_html=True)
                model_df = pd.DataFrame({
                    "Model": ["Logistic Regression", "Random Forest", "XGBoost"],
                    "Phishing Probability": [round(lp, 4), round(rfp, 4), round(xp, 4)],
                    "Verdict": [
                        verdict_label(int(lp >= threshold)),
                        verdict_label(int(rfp >= threshold)),
                        verdict_label(int(xp >= threshold)),
                    ],
                })
                st.dataframe(model_df, use_container_width=True, hide_index=True)

            with col_right:
                st.markdown('<p class="section-label">Structural Evidence</p>', unsafe_allow_html=True)
                st.json({
                    "Domain": ext.domain,
                    "TLD": ext.suffix,
                    "Subdomain Count": int(struct["subdomain_count"]),
                    "URL Length": int(struct["url_length"]),
                    "Digit Count": int(struct["num_digits"]),
                    "Risky TLD": "Yes" if struct["risky_tld"] else "No",
                    "IP-based Host": "Yes" if struct["is_ip"] else "No",
                    "Keyword Score": int(struct["keyword_score"]),
                    "Brand Similarity": round(float(struct["brand_similarity"]), 3),
                })

# ================= BATCH =================

with batch_tab:

    st.markdown("")
    st.subheader("📂 Batch Investigation")
    st.caption("Upload a CSV file with a column named **url** to scan multiple URLs at once.")

    uploaded = st.file_uploader(
        "Upload CSV with column 'url'",
        type=["csv"],
        label_visibility="collapsed",
    )

    start = st.button("🚀 Start Batch Scan", use_container_width=True)

    if uploaded and start:
        st.session_state.batch_run = True

    if uploaded and st.session_state.batch_run:

        df = pd.read_csv(uploaded)

        if "url" not in df.columns:
            st.error("❌ CSV must contain a column named **url**.")
        else:
            df = df.dropna(subset=["url"]).drop_duplicates(subset=["url"])

            results = []
            evidence = {"keyword": 0, "risky": 0, "brand": 0, "ip": 0}

            progress = st.progress(0, text="Initialising scan…")
            total = len(df)

            for i, u in enumerate(df["url"]):
                progress.progress(
                    (i + 1) / total,
                    text=f"🔍 Scanning URL {i + 1} of {total}…",
                )

                lp, rfp, xp, struct, _ = cached_probs(str(u))
                score, pred = active_score(lp, rfp, xp)

                if struct["keyword_score"] > 0:
                    evidence["keyword"] += 1
                if struct["risky_tld"]:
                    evidence["risky"] += 1
                if struct["brand_similarity"] > BRAND_ALERT_TH:
                    evidence["brand"] += 1
                if struct["is_ip"]:
                    evidence["ip"] += 1

                results.append({
                    "url": u,
                    "logistic_prob": lp,
                    "rf_prob": rfp,
                    "xgb_prob": xp,
                    "active_model": model_mode,
                    "active_threshold": threshold,
                    "active_score": score,
                    "prediction": pred,
                    "verdict": verdict_label(pred),
                })

            progress.empty()
            st.success(f"✅ Scan complete — **{total}** URLs analysed.")

            st.session_state.batch_results = pd.DataFrame(results)
            st.session_state.batch_evidence = evidence
            st.session_state.batch_run = False

    # ── Display cached results ──
    if isinstance(st.session_state.batch_results, pd.DataFrame):

        res = st.session_state.batch_results
        evidence = st.session_state.batch_evidence

        phishing = int(res["prediction"].sum())
        legit = len(res) - phishing

        st.markdown("")
        st.markdown('<p class="section-label">Scan Summary</p>', unsafe_allow_html=True)

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("🔗 Total URLs", len(res))
        m2.metric("⚠️ Phishing", phishing)
        m3.metric("✅ Legitimate", legit)
        m4.metric("🤖 Model", model_mode.split()[0])
        m5.metric("🎯 Threshold", f"{threshold:.3f}")

        # ── Evidence indicators ──
        st.markdown("")
        st.markdown('<p class="section-label">Threat Indicators Detected</p>', unsafe_allow_html=True)
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("🔑 Keyword Hits", evidence["keyword"])
        e2.metric("🌐 Risky TLDs", evidence["risky"])
        e3.metric("🏷️ Brand Mimicry", evidence["brand"])
        e4.metric("📡 IP-based Hosts", evidence["ip"])

        st.markdown("")

        filt = st.selectbox(
            "Filter Results",
            ["All", "Phishing Only", "Legitimate Only"],
        )

        show = res.copy()
        if filt == "Phishing Only":
            show = show[show.prediction == 1]
        elif filt == "Legitimate Only":
            show = show[show.prediction == 0]

        display = show.copy()
        for c in ["logistic_prob", "rf_prob", "xgb_prob", "active_score"]:
            display[c] = display[c].round(3)

        st.dataframe(display, use_container_width=True, hide_index=True)

        st.markdown("")
        st.download_button(
            "📥 Download Investigation Report",
            res.to_csv(index=False).encode("utf-8"),
            "soc_scan_results.csv",
            "text/csv",
            use_container_width=True,
        )
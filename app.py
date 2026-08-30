
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from io import BytesIO
from datetime import datetime, timedelta

# --------------------------- BRAND PROFILE ---------------------------
# Add your real profile URLs here when you want the social buttons active.
GITHUB_URL = "https://github.com/prajwaly849-sudo"
LINKEDIN_URL = "https://www.linkedin.com/in/prajwal-y-r-23b087247"
PORTFOLIO_URL = ""

DEVELOPER_NAME = "Prajwal Y R"
PROJECT_CONTEXT = "Razorpay Internship Portfolio Demo"
# ============================================================
# RevPilot — Ultimate AI Revenue Growth & Campaign Intelligence
# ============================================================

st.set_page_config(
    page_title="RevPilot — AI Revenue Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------- PREMIUM UI ---------------------------

st.markdown("""
<style>
/* ===== RevPilot AI — premium responsive interface ===== */
:root{
    --rp-bg:#070b14;
    --rp-panel:rgba(14,21,35,.78);
    --rp-panel-2:rgba(18,27,45,.88);
    --rp-border:rgba(148,163,184,.14);
    --rp-text:#f8fafc;
    --rp-muted:#94a3b8;
    --rp-purple:#8b5cf6;
    --rp-blue:#38bdf8;
    --rp-green:#34d399;
}

.stApp{
    background:
      radial-gradient(circle at 88% 0%, rgba(99,102,241,.16), transparent 28%),
      radial-gradient(circle at 4% 28%, rgba(14,165,233,.08), transparent 24%),
      linear-gradient(180deg,#060912 0%,#080d18 48%,#060a12 100%);
    color:var(--rp-text);
}

.block-container{
    max-width:1480px;
    padding:2.2rem 2.6rem 3rem;
}

/* Header / top chrome */
[data-testid="stHeader"]{
    background:rgba(6,9,18,.72);
    backdrop-filter:blur(18px);
}
[data-testid="stToolbar"]{right:1rem;}

/* Sidebar */
[data-testid="stSidebar"]{
    background:
      radial-gradient(circle at 10% 0%,rgba(124,58,237,.16),transparent 34%),
      linear-gradient(180deg,#090e19 0%,#070c15 100%);
    border-right:1px solid rgba(148,163,184,.12);
}
[data-testid="stSidebar"] > div:first-child{
    padding:1.1rem .9rem 1.5rem;
}
[data-testid="stSidebar"] .block-container{
    padding:0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > label{
    color:#7f8da5;
    font-size:.72rem;
    font-weight:800;
    letter-spacing:.16em;
    text-transform:uppercase;
    margin:1rem 0 .55rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] > div{
    gap:.25rem;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label{
    border-radius:13px;
    padding:.72rem .78rem;
    margin:.12rem 0;
    border:1px solid transparent;
    transition:all .18s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
    background:rgba(139,92,246,.09);
    border-color:rgba(139,92,246,.18);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
    background:linear-gradient(90deg,rgba(124,58,237,.22),rgba(37,99,235,.10));
    border-color:rgba(139,92,246,.34);
    box-shadow:inset 3px 0 0 #8b5cf6, 0 8px 24px rgba(0,0,0,.12);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{
    font-size:.91rem;
    font-weight:650;
    color:#dbe4f0;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) p{
    color:#fff;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"]{
    background:rgba(15,23,42,.52);
    border:1px dashed rgba(139,92,246,.38);
    border-radius:16px;
    padding:.45rem;
}
[data-testid="stSidebar"] .stButton button{
    border-radius:12px;
}

/* Sidebar brand */
.rp-side-brand{
    padding:1.05rem;
    margin-bottom:1rem;
    border:1px solid rgba(139,92,246,.24);
    border-radius:20px;
    background:
      linear-gradient(135deg,rgba(124,58,237,.18),rgba(15,23,42,.68));
    box-shadow:0 18px 45px rgba(0,0,0,.18);
}
.rp-mark{
    width:42px;height:42px;border-radius:13px;
    display:inline-flex;align-items:center;justify-content:center;
    background:linear-gradient(135deg,#7c3aed,#2563eb);
    font-size:1.25rem;
    box-shadow:0 8px 25px rgba(99,102,241,.28);
    margin-bottom:.7rem;
}
.rp-side-brand h2{
    margin:0;color:#fff;font-size:1.2rem;font-weight:800;
}
.rp-side-brand p{
    margin:.25rem 0 0;color:#8fa0b8;font-size:.78rem;
}
.rp-creator{
    margin-top:.8rem;padding-top:.7rem;
    border-top:1px solid rgba(148,163,184,.12);
    color:#b9c5d6;font-size:.76rem;
}
.rp-creator strong{color:#fff;}

/* Sidebar — upgraded navigation / branding */
[data-testid="stSidebar"]{
    width:310px !important;
    min-width:310px !important;
}
[data-testid="stSidebar"] > div:first-child{
    padding:1rem .85rem 1.35rem;
}
.rp-brand-shell{
    position:relative;
    overflow:hidden;
    padding:1rem;
    margin:.15rem 0 1.1rem;
    border-radius:22px;
    border:1px solid rgba(139,92,246,.30);
    background:
      radial-gradient(circle at 90% 0%,rgba(6,182,212,.16),transparent 34%),
      linear-gradient(145deg,rgba(139,92,246,.18),rgba(7,15,29,.82));
    box-shadow:0 18px 45px rgba(0,0,0,.25);
}
.rp-brand-shell:after{
    content:"";position:absolute;right:-42px;bottom:-62px;width:150px;height:150px;
    border-radius:50%;border:1px solid rgba(6,182,212,.12);
    box-shadow:0 0 0 18px rgba(6,182,212,.03),0 0 0 36px rgba(139,92,246,.025);
}
.rp-logo-row{display:flex;align-items:center;gap:.8rem;position:relative;z-index:1;}
.rp-svg-logo{width:50px;height:50px;flex:0 0 50px;filter:drop-shadow(0 8px 18px rgba(99,102,241,.32));}
.rp-brand-title{font-size:1.14rem;font-weight:850;color:#fff;line-height:1.05;}
.rp-brand-sub{font-size:.72rem;color:#91a1b8;margin-top:.28rem;letter-spacing:.03em;}
.rp-brand-tag{
    display:inline-flex;align-items:center;gap:.38rem;margin-top:.9rem;padding:.42rem .62rem;
    border-radius:999px;border:1px solid rgba(52,211,153,.20);
    background:rgba(16,185,129,.07);color:#6ee7b7;font-size:.66rem;font-weight:800;
}
.rp-brand-tag span{width:6px;height:6px;border-radius:50%;background:#34d399;box-shadow:0 0 10px #34d399;}
.rp-owner{margin-top:.7rem;color:#a9b7ca;font-size:.71rem;line-height:1.45;}
.rp-owner strong{color:#f8fafc;}
.rp-nav-label{margin:.9rem .3rem .55rem;color:#71819a;font-size:.67rem;font-weight:850;letter-spacing:.2em;text-transform:uppercase;}
[data-testid="stSidebar"] [data-testid="stRadio"] label{
    min-height:44px;display:flex;align-items:center;border-radius:14px;
    padding:.55rem .72rem;margin:.18rem 0;border:1px solid transparent;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{
    transform:translateX(2px);background:rgba(139,92,246,.08);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){
    background:linear-gradient(100deg,rgba(139,92,246,.22),rgba(6,182,212,.06));
    border-color:rgba(139,92,246,.28);
    box-shadow:inset 3px 0 0 #8b5cf6,0 8px 24px rgba(0,0,0,.14);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{font-size:.86rem;font-weight:650;}
.rp-side-dataset{
    padding:.82rem;border-radius:16px;border:1px solid rgba(148,163,184,.11);
    background:linear-gradient(145deg,rgba(15,23,42,.72),rgba(10,16,28,.55));
}
.rp-side-stat{display:flex;justify-content:space-between;align-items:end;gap:.5rem;}
.rp-side-stat + .rp-side-stat{margin-top:.7rem;padding-top:.7rem;border-top:1px solid rgba(148,163,184,.09);}
.rp-side-stat .k{font-size:.66rem;color:#71819a;letter-spacing:.1em;text-transform:uppercase;}
.rp-side-stat .v{font-size:1rem;font-weight:850;color:#f8fafc;}
.rp-side-stat .v.accent{color:#a78bfa;}
.rp-socials{display:flex;gap:.42rem;margin-top:.8rem;}
.rp-social{flex:1;text-align:center;padding:.48rem .25rem;border-radius:10px;border:1px solid rgba(148,163,184,.11);background:rgba(15,23,42,.45);font-size:.68rem;font-weight:750;color:#b9c5d6;text-decoration:none;}
.rp-social.active{color:#fff;border-color:rgba(6,182,212,.20);}

.rp-pills{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.7rem;}
.rp-pills span{padding:.45rem .7rem;border-radius:999px;border:1px solid rgba(139,92,246,.25);background:rgba(139,92,246,.08);color:#c4b5fd;font-size:.72rem;font-weight:750;}
.rp-link-row{display:flex;gap:.65rem;flex-wrap:wrap;margin:.7rem 0;}
.rp-link-row a{display:inline-flex;padding:.65rem .9rem;border-radius:12px;border:1px solid rgba(6,182,212,.22);background:rgba(6,182,212,.06);color:#8be9f7 !important;text-decoration:none;font-weight:750;}
/* Hero */
.rp-hero{
    position:relative;
    overflow:hidden;
    padding:2.55rem 2.65rem;
    border-radius:28px;
    border:1px solid rgba(139,92,246,.32);
    background:
      radial-gradient(circle at 92% 18%,rgba(59,130,246,.25),transparent 28%),
      radial-gradient(circle at 72% 90%,rgba(124,58,237,.22),transparent 34%),
      linear-gradient(135deg,rgba(39,20,79,.90),rgba(10,18,34,.96) 64%);
    box-shadow:0 28px 80px rgba(0,0,0,.28);
    margin-bottom:1.8rem;
}
.rp-hero:before{
    content:"";
    position:absolute;inset:-30% -10% auto auto;
    width:380px;height:380px;border-radius:50%;
    background:rgba(99,102,241,.10);
    filter:blur(8px);
}
.rp-eyebrow{
    position:relative;
    color:#a78bfa;
    font-size:.72rem;
    font-weight:850;
    letter-spacing:.22em;
    text-transform:uppercase;
    margin-bottom:.7rem;
}
.rp-hero h1{
    position:relative;
    margin:0;
    font-size:clamp(2.5rem,5vw,4.8rem);
    line-height:.98;
    letter-spacing:-.045em;
    color:#fff;
}
.rp-hero .desc{
    position:relative;
    max-width:760px;
    margin:1.25rem 0 1.35rem;
    color:#b4c0d2;
    font-size:1.03rem;
    line-height:1.75;
}
.rp-status{
    position:relative;
    display:inline-flex;
    align-items:center;
    gap:.55rem;
    padding:.62rem .9rem;
    border-radius:999px;
    border:1px solid rgba(52,211,153,.30);
    background:rgba(16,185,129,.08);
    color:#6ee7b7;
    font-weight:750;
    font-size:.82rem;
}
.rp-dot{
    width:8px;height:8px;border-radius:50%;
    background:#34d399;
    box-shadow:0 0 16px #34d399;
}

/* Section titles */
h1,h2,h3{
    letter-spacing:-.025em;
}
.rp-section{
    margin:1.8rem 0 .85rem;
}
.rp-section h2{
    margin:0;
    font-size:1.55rem;
    color:#f8fafc;
}
.rp-section p{
    margin:.3rem 0 0;
    color:#77869d;
    font-size:.88rem;
}

/* KPI cards */
.rp-kpi{
    min-height:132px;
    padding:1.25rem 1.3rem;
    border-radius:20px;
    border:1px solid rgba(148,163,184,.13);
    background:linear-gradient(145deg,rgba(16,25,41,.90),rgba(8,14,25,.88));
    box-shadow:0 16px 42px rgba(0,0,0,.16);
}
.rp-kpi .label{
    color:#8ea0b9;font-size:.78rem;font-weight:700;
}
.rp-kpi .value{
    margin:.7rem 0 .35rem;
    color:#fff;font-size:2rem;font-weight:850;letter-spacing:-.035em;
}
.rp-kpi .hint{
    color:#64748b;font-size:.73rem;
}

/* Native Streamlit metrics, tables, inputs */
[data-testid="stMetric"]{
    background:linear-gradient(145deg,rgba(16,25,41,.9),rgba(8,14,25,.88));
    border:1px solid rgba(148,163,184,.13);
    padding:1rem 1.05rem;
    border-radius:18px;
}
[data-testid="stMetricLabel"]{color:#8ea0b9!important;}
[data-testid="stMetricValue"]{font-size:1.8rem!important;color:#fff!important;}
[data-testid="stMetricDelta"]{font-size:.75rem;}

[data-testid="stDataFrame"]{
    border:1px solid rgba(148,163,184,.12);
    border-radius:16px;
    overflow:hidden;
}
.stSelectbox,.stMultiSelect,.stNumberInput,.stSlider{
    margin-bottom:.25rem;
}

/* Hide excess Streamlit chrome */
footer{visibility:hidden;}
#MainMenu{visibility:hidden;}

/* Mobile */
@media (max-width: 900px){
    .block-container{padding:1rem .7rem 2rem;}
    .rp-hero{padding:1.65rem 1.25rem;border-radius:22px;margin-bottom:1.25rem;}
    .rp-eyebrow{font-size:.62rem;letter-spacing:.16em;line-height:1.6;}
    .rp-hero h1{font-size:2.35rem;}
    .rp-hero .desc{font-size:.9rem;line-height:1.55;margin:1rem 0 1.1rem;}
    .rp-status{font-size:.75rem;padding:.55rem .75rem;}
    .rp-kpi{min-height:112px;padding:1rem;}
    .rp-kpi .value{font-size:1.65rem;margin:.5rem 0 .25rem;}
    .rp-section{margin:1.35rem 0 .7rem;}
    .rp-section h2{font-size:1.35rem;}

    /* Mobile sidebar: wide enough to read, narrow enough to keep context visible. */
    [data-testid="stSidebar"]{
        width:86vw !important;
        min-width:86vw !important;
        max-width:360px !important;
    }
    [data-testid="stSidebar"] > div:first-child{padding:.75rem .7rem 1rem;}
    .rp-brand-shell{padding:.9rem;border-radius:18px;margin-bottom:.75rem;}
    .rp-svg-logo{width:44px;height:44px;flex-basis:44px;}
    .rp-brand-title{font-size:1.05rem;}
    .rp-brand-sub{font-size:.67rem;}
    .rp-brand-tag{margin-top:.7rem;font-size:.62rem;padding:.38rem .55rem;}
    .rp-owner{font-size:.68rem;margin-top:.55rem;}
    .rp-nav-label{margin:.75rem .25rem .4rem;font-size:.62rem;}
    [data-testid="stSidebar"] [data-testid="stRadio"] label{
        min-height:40px;padding:.5rem .58rem;margin:.12rem 0;border-radius:12px;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] label p{font-size:.8rem;}
    .rp-side-dataset{padding:.7rem;border-radius:14px;}
    .rp-social{font-size:.63rem;padding:.42rem .2rem;}
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA
# ============================================================

@st.cache_data
def create_demo_data():
    data = [
        ["C001",8500,"GROWTH",4,4200,"Email"],["C002",12500,"LOYAL",8,6800,"WhatsApp"],
        ["C003",3200,"STANDARD",2,1800,"Email"],["C004",18500,"HIGH VALUE",10,9200,"Email + WhatsApp"],
        ["C005",7600,"GROWTH",5,3900,"WhatsApp"],["C006",4100,"STANDARD",3,2200,"Email"],
        ["C007",22400,"HIGH VALUE",12,11600,"Email + WhatsApp"],["C008",9800,"LOYAL",7,5100,"WhatsApp"],
        ["C009",2900,"STANDARD",2,1500,"Email"],["C010",14300,"GROWTH",6,7300,"Email"],
        ["C011",5200,"STANDARD",3,2700,"Email"],["C012",16700,"LOYAL",9,8500,"Email + WhatsApp"],
        ["C013",3800,"STANDARD",2,1900,"WhatsApp"],["C014",21100,"HIGH VALUE",11,10900,"Email + WhatsApp"],
        ["C015",6900,"GROWTH",4,3500,"Email"],["C016",4700,"STANDARD",3,2400,"WhatsApp"],
        ["C017",13200,"LOYAL",8,6900,"Email + WhatsApp"],["C018",28700,"HIGH VALUE",13,14200,"Email + WhatsApp"],
        ["C019",34100,"HIGH VALUE",14,16900,"Email + WhatsApp"],["C020",6100,"GROWTH",4,3100,"Email"],
        ["C021",5300,"STANDARD",3,2600,"Email"],["C022",25600,"HIGH VALUE",10,12800,"Email + WhatsApp"],
        ["C023",11800,"LOYAL",7,6200,"WhatsApp"],["C024",7300,"GROWTH",5,3700,"Email"],
        ["C025",4500,"STANDARD",2,2100,"Email"],["C026",15600,"LOYAL",9,7900,"Email + WhatsApp"],
        ["C027",8200,"GROWTH",5,4100,"WhatsApp"],["C028",3600,"STANDARD",2,1750,"Email"],
        ["C029",19800,"HIGH VALUE",11,10100,"Email + WhatsApp"],["C030",9200,"LOYAL",6,4700,"WhatsApp"],
        ["C031",5100,"STANDARD",3,2500,"Email"],["C032",17600,"LOYAL",9,8800,"Email + WhatsApp"],
        ["C033",6600,"GROWTH",4,3300,"Email"],["C034",3900,"STANDARD",2,1900,"WhatsApp"],
        ["C035",23900,"HIGH VALUE",12,12100,"Email + WhatsApp"],["C036",10700,"LOYAL",7,5400,"WhatsApp"],
        ["C037",5800,"STANDARD",3,2900,"Email"],["C038",14900,"GROWTH",6,7600,"Email"],
        ["C039",4300,"STANDARD",2,2050,"WhatsApp"],["C040",312200,"HIGH VALUE",15,156000,"Email + WhatsApp"],
        ["C041",8700,"GROWTH",5,4400,"Email"],["C042",12700,"LOYAL",8,6400,"WhatsApp"],
        ["C043",3400,"STANDARD",2,1650,"Email"],["C044",19300,"HIGH VALUE",10,9800,"Email + WhatsApp"],
        ["C045",7400,"GROWTH",4,3600,"Email"],["C046",4900,"STANDARD",3,2400,"WhatsApp"],
        ["C047",13800,"LOYAL",8,7000,"Email + WhatsApp"],["C048",6800,"GROWTH",4,3400,"Email"],
        ["C049",5500,"STANDARD",3,2700,"WhatsApp"],["C050",59400,"HIGH VALUE",13,30200,"Email + WhatsApp"],
    ]
    return pd.DataFrame(data, columns=["Customer","Customer Value","Segment","Purchases","Total Spend","Channel"])

def normalize_data(df):
    df = df.copy()
    aliases = {
        "customer":"Customer","customer_id":"Customer","customer id":"Customer","id":"Customer",
        "customer_value":"Customer Value","value":"Customer Value","revenue":"Customer Value",
        "segment":"Segment","purchases":"Purchases","purchase_count":"Purchases",
        "total_spend":"Total Spend","spend":"Total Spend","channel":"Channel"
    }
    rename = {}
    for c in df.columns:
        key = str(c).strip().lower()
        if key in aliases:
            rename[c] = aliases[key]
    df = df.rename(columns=rename)
    if "Customer" not in df.columns:
        df["Customer"] = [f"C{i:03d}" for i in range(1, len(df)+1)]
    if "Customer Value" not in df.columns:
        for candidate in ["Amount","Sales","Revenue","Total Value"]:
            if candidate in df.columns:
                df["Customer Value"] = df[candidate]
                break
    if "Customer Value" not in df.columns:
        df["Customer Value"] = 0.0
    if "Purchases" not in df.columns:
        df["Purchases"] = 1
    if "Total Spend" not in df.columns:
        df["Total Spend"] = df["Customer Value"] * 0.5
    if "Segment" not in df.columns:
        q = df["Customer Value"].quantile([.25,.5,.75]).values
        def seg(v):
            if v >= q[2]: return "HIGH VALUE"
            if v >= q[1]: return "LOYAL"
            if v >= q[0]: return "GROWTH"
            return "STANDARD"
        df["Segment"] = df["Customer Value"].apply(seg)
    if "Channel" not in df.columns:
        df["Channel"] = np.where(df["Purchases"] >= 8, "Email + WhatsApp", "Email")
    for c in ["Customer Value","Purchases","Total Spend"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    df["Customer"] = df["Customer"].astype(str)
    df["Segment"] = df["Segment"].astype(str).str.upper()
    df["Channel"] = df["Channel"].astype(str)
    df["Avg Order Value"] = np.where(df["Purchases"] > 0, df["Total Spend"]/df["Purchases"], 0)
    df["Spend Ratio"] = np.where(df["Customer Value"] > 0, df["Total Spend"]/df["Customer Value"], 0)
    df["Value per Purchase"] = np.where(df["Purchases"] > 0, df["Customer Value"]/df["Purchases"], 0)
    return df

# Optional uploaded dataset; demo data is always available.
demo = create_demo_data()
if "dataset" not in st.session_state:
    st.session_state.dataset = demo.copy()

# ============================================================
# SIDEBAR — WORKSPACE
# ============================================================

st.sidebar.markdown("""
<div class="rp-brand-shell">
  <div class="rp-logo-row">
    <svg class="rp-svg-logo" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-label="RevPilot AI logo">
      <defs>
        <linearGradient id="rpG" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#8B5CF6"/>
          <stop offset="100%" stop-color="#06B6D4"/>
        </linearGradient>
      </defs>
      <rect x="3" y="3" width="58" height="58" rx="17" fill="#0B0F19" stroke="url(#rpG)" stroke-width="2"/>
      <path d="M18 39L27 23L34 34L43 18L47 46H39L37 34L31 43L25 34L22 46H15L18 39Z" fill="url(#rpG)"/>
      <circle cx="48" cy="48" r="4" fill="#34D399"/>
    </svg>
    <div>
      <div class="rp-brand-title">RevPilot AI</div>
      <div class="rp-brand-sub">Revenue Intelligence OS</div>
    </div>
  </div>
  <div class="rp-brand-tag"><span></span> Internship portfolio demo</div>
  <div class="rp-owner">Built &amp; Designed by <strong>Prajwal Y R</strong><br/>Creator &amp; Developer • Razorpay Internship Portfolio Demo</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div class="rp-nav-label">Workspace</div>', unsafe_allow_html=True)

customers = normalize_data(st.session_state.dataset)

page = st.sidebar.radio("Navigation", [
    "🏠 Executive Dashboard",
    "👥 Customer Intelligence",
    "🎯 AI Target Customers",
    "🔮 Campaign Prediction",
    "🧪 Campaign Lab",
    "📣 Campaign Generator",
    "💬 AI Messages",
    "👤 Customer 360",
    "📈 Business Analytics",
    "🤖 ML Model Center",
    "📥 Data & Export",
    "✨ About Developer & Project",
], label_visibility="collapsed")

st.sidebar.markdown('<div class="rp-nav-label">Data Source</div>', unsafe_allow_html=True)

uploaded = st.sidebar.file_uploader(
    "Replace dataset (CSV / Excel)",
    type=["csv","xlsx","xls"],
    help="Upload a CSV or Excel dataset to replace the demo data."
)
if uploaded is not None:
    try:
        raw = pd.read_csv(uploaded) if uploaded.name.lower().endswith(".csv") else pd.read_excel(uploaded)
        st.session_state.dataset = normalize_data(raw)
        customers = normalize_data(st.session_state.dataset)
        st.sidebar.success("Dataset loaded successfully.")
    except Exception as e:
        st.sidebar.error(f"Could not load file: {e}")
st.sidebar.markdown(
    f"""
    <div class="rp-side-dataset">
      <div class="rp-side-stat"><div class="k">Customers</div><div class="v">{len(customers):,}</div></div>
      <div class="rp-side-stat"><div class="k">Customer Value</div><div class="v accent">₹{customers['Customer Value'].sum():,.0f}</div></div>
    </div>
    """, unsafe_allow_html=True
)
social_links = []
if GITHUB_URL:
    social_links.append(f'<a class="rp-social active" href="{GITHUB_URL}" target="_blank">GitHub ↗</a>')
if LINKEDIN_URL:
    social_links.append(f'<a class="rp-social active" href="{LINKEDIN_URL}" target="_blank">LinkedIn ↗</a>')
if PORTFOLIO_URL:
    social_links.append(f'<a class="rp-social active" href="{PORTFOLIO_URL}" target="_blank">Portfolio ↗</a>')
if social_links:
    st.sidebar.markdown('<div class="rp-socials">' + ''.join(social_links) + '</div>', unsafe_allow_html=True)
st.sidebar.caption("Demo data is self-contained • No API key required.")

# ============================================================
# SHARED AI / ANALYTICS FUNCTIONS
# ============================================================

SEGMENT_BASE = {"HIGH VALUE": .72, "LOYAL": .68, "GROWTH": .55, "STANDARD": .42}

def rule_response_probability(row):
    seg = str(row["Segment"]).upper()
    base = SEGMENT_BASE.get(seg, .42)
    value_boost = min(max((float(row["Customer Value"])/50000)*.05, 0), .08)
    purchase_boost = min(float(row["Purchases"])/20*.04, .04)
    channel_boost = .02 if "WhatsApp" in str(row["Channel"]) else 0
    return float(min(max(base + value_boost + purchase_boost + channel_boost, .20), .95))

def priority_score(row):
    value = float(row["Customer Value"])
    spend = float(row["Total Spend"])
    purchases = float(row["Purchases"])
    seg_bonus = {"HIGH VALUE":35,"LOYAL":25,"GROWTH":18,"STANDARD":8}.get(str(row["Segment"]).upper(),5)
    value_score = min(value / max(customers["Customer Value"].quantile(.95),1) * 40, 40)
    purchase_score = min(purchases/15*12, 12)
    efficiency = min((spend/max(value,1))*10, 10)
    return round(seg_bonus + value_score + purchase_score + efficiency, 2)

def prediction_table(df, response_boost=0.0, revenue_rate=.20, cost_rate=.02, fixed_cost=500):
    rows = []
    for _, r in df.iterrows():
        p = min(max(rule_response_probability(r)+response_boost, .05), .98)
        expected_revenue = float(r["Customer Value"]) * p * revenue_rate
        cost = max(fixed_cost, float(r["Customer Value"]) * cost_rate)
        roi = ((expected_revenue-cost)/cost)*100 if cost else 0
        if p >= .72: action = "Launch personalized upsell"
        elif p >= .58: action = "Targeted offer + engagement"
        elif p >= .45: action = "Re-engagement campaign"
        else: action = "Low-cost awareness / nurture"
        rows.append({
            "Customer":r["Customer"],"Segment":r["Segment"],
            "Customer Value":float(r["Customer Value"]),"Response Probability":p,
            "Expected Revenue":expected_revenue,"Campaign Cost":cost,
            "Estimated ROI":roi,"Next Best Action":action,
        })
    return pd.DataFrame(rows)

@st.cache_resource
def train_demo_models():
    rng = np.random.default_rng(42)
    base = create_demo_data()
    Xbase = pd.DataFrame({
        "value":base["Customer Value"], "purchases":base["Purchases"],
        "spend":base["Total Spend"], "channel_whatsapp":base["Channel"].str.contains("WhatsApp").astype(int),
        "segment_high":(base["Segment"]=="HIGH VALUE").astype(int),
        "segment_loyal":(base["Segment"]=="LOYAL").astype(int),
        "segment_growth":(base["Segment"]=="GROWTH").astype(int),
    })
    # Create a realistic synthetic historical campaign table from the demo
    # features. This is explicitly a demo/training simulation, not real outcomes.
    n = 1200
    idx = rng.integers(0, len(Xbase), size=n)
    X = Xbase.iloc[idx].reset_index(drop=True).copy()
    noise = rng.normal(0, .07, n)
    z = (
        -1.5 + 0.000018*X["value"] + 0.06*X["purchases"] +
        0.000006*X["spend"] + .28*X["channel_whatsapp"] +
        .45*X["segment_high"] + .25*X["segment_loyal"] +
        .12*X["segment_growth"] + noise
    )
    prob = 1/(1+np.exp(-z))
    y = (rng.random(n) < prob).astype(int)
    revenue = np.maximum(0, X["value"]*(.08 + .28*y + rng.normal(0,.03,n)))
    Xtr,Xte,ytr,yte = train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
    clf = RandomForestClassifier(n_estimators=250,max_depth=7,min_samples_leaf=4,random_state=42,class_weight="balanced")
    clf.fit(Xtr,ytr)
    pred = clf.predict(Xte)
    reg = RandomForestRegressor(n_estimators=200,max_depth=8,min_samples_leaf=4,random_state=42)
    reg.fit(Xtr,revenue[Xtr.index] if hasattr(Xtr,"index") else revenue)
    return clf, reg, accuracy_score(yte,pred), X.columns.tolist()

clf, revenue_model, model_accuracy, model_features = train_demo_models()

def ml_probability(df):
    X = pd.DataFrame({
        "value":df["Customer Value"],"purchases":df["Purchases"],
        "spend":df["Total Spend"],"channel_whatsapp":df["Channel"].str.contains("WhatsApp").astype(int),
        "segment_high":(df["Segment"]=="HIGH VALUE").astype(int),
        "segment_loyal":(df["Segment"]=="LOYAL").astype(int),
        "segment_growth":(df["Segment"]=="GROWTH").astype(int),
    })
    return clf.predict_proba(X)[:,1]

def make_message(row, offer, tone, channel):
    name = row["Customer"]
    value = float(row["Customer Value"])
    segment = row["Segment"]
    opening = {
        "Professional":"Hello",
        "Friendly":"Hi",
        "Premium":"Hello valued customer",
        "Urgent":"Hi",
    }.get(tone,"Hi")
    close = {
        "Professional":"We would be happy to help you explore the option.",
        "Friendly":"Take a look and see what works best for you!",
        "Premium":"We would be delighted to arrange a personalized recommendation.",
        "Urgent":"This opportunity is available for a limited campaign window.",
    }.get(tone,"We would be happy to help.")
    if "WhatsApp" in channel:
        return f"{opening} {name}! Based on your recent customer activity, we selected a personalized {offer} opportunity for you. Your profile is currently in our {segment.lower()} segment. {close}"
    return f"Subject: A personalized {offer} opportunity for you\n\n{opening} {name},\n\nWe noticed your recent purchase activity and selected a personalized {offer} recommendation for you. As a {segment.lower()} customer, you may be a strong fit for this offer.\n\n{close}\n\n— RevPilot"

# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "🏠 Executive Dashboard":
    total_value = customers["Customer Value"].sum()
    total_spend = customers["Total Spend"].sum()
    high_value = int((customers["Segment"]=="HIGH VALUE").sum())
    priority = customers.assign(
        Priority=customers.apply(priority_score,axis=1)
    ).sort_values("Priority",ascending=False)

    predicted = prediction_table(priority.head(min(10,len(priority))))
    total_expected = predicted["Expected Revenue"].sum()
    total_cost = predicted["Campaign Cost"].sum()
    overall_roi = ((total_expected-total_cost)/total_cost*100) if total_cost else 0

    st.markdown("""
    <div class="rp-hero">
      <div class="rp-eyebrow">Revenue Intelligence OS • Internship Portfolio Project</div>
      <h1>RevPilot AI</h1>
      <div class="desc">
        Predict revenue, identify high-value customers, uncover growth opportunities
        and build smarter campaigns from customer data.
      </div>
      <div class="rp-status"><span class="rp-dot"></span> Intelligence engine ready</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="rp-section">
      <h2>Executive Overview</h2>
      <p>A real-time view of customer value, engagement and revenue opportunity.</p>
    </div>
    """, unsafe_allow_html=True)

    a,b,c,d = st.columns(4)
    cards = [
        (a, "Total Customer Value", f"₹{total_value:,.0f}", "Across current dataset"),
        (b, "Customers", f"{len(customers):,}", "Unique customer records"),
        (c, "High-Value Accounts", f"{high_value:,}", "Priority revenue segment"),
        (d, "Estimated ROI", f"{overall_roi:.1f}%", "Top 10 priority campaign"),
    ]
    for col,label,value,hint in cards:
        with col:
            st.markdown(
                f'<div class="rp-kpi"><div class="label">{label}</div>'
                f'<div class="value">{value}</div><div class="hint">{hint}</div></div>',
                unsafe_allow_html=True
            )

    st.markdown("""
    <div class="rp-section">
      <h2>Revenue Intelligence</h2>
      <p>Understand where customer value is concentrated and where growth can be created.</p>
    </div>
    """, unsafe_allow_html=True)

    left,right = st.columns(2)
    with left:
        seg = customers.groupby("Segment",as_index=False)["Customer Value"].sum()
        fig = px.pie(
            seg,names="Segment",values="Customer Value",
            title="Customer Value by Segment",hole=.58
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cbd5e1",
            margin=dict(l=10,r=10,t=55,b=10),
            legend=dict(orientation="h",y=-.08)
        )
        st.plotly_chart(fig,use_container_width=True)
    with right:
        seg_count = customers["Segment"].value_counts().rename_axis("Segment").reset_index(name="Customers")
        fig = px.bar(
            seg_count,x="Segment",y="Customers",
            title="Customer Segment Distribution",text="Customers"
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#cbd5e1",
            margin=dict(l=10,r=10,t=55,b=10)
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig,use_container_width=True)

    st.markdown("""
    <div class="rp-section">
      <h2>Campaign Opportunity Snapshot</h2>
      <p>Projected economics for the highest-priority customers.</p>
    </div>
    """, unsafe_allow_html=True)

    x,y,z = st.columns(3)
    x.metric("Expected Revenue",f"₹{total_expected:,.0f}")
    y.metric("Campaign Cost",f"₹{total_cost:,.0f}")
    z.metric("Estimated ROI",f"{overall_roi:.1f}%")

    st.markdown("""
    <div class="rp-section">
      <h2>Top Revenue Opportunities</h2>
      <p>Customers ranked by RevPilot's transparent priority score.</p>
    </div>
    """, unsafe_allow_html=True)

    show = priority.head(10)[
        ["Customer","Segment","Customer Value","Purchases","Total Spend","Channel","Priority"]
    ]
    st.dataframe(show,use_container_width=True,hide_index=True)

    st.caption("RevPilot AI • Internship portfolio demonstration • Built & Designed by Prajwal Y R")

# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif page == "👥 Customer Intelligence":
    st.title("👥 Customer Intelligence")
    st.caption("Explore customer economics, segments, purchase behavior and value concentration.")

    c1,c2,c3 = st.columns(3)
    seg_filter = c1.multiselect("Segments",sorted(customers["Segment"].unique()),default=sorted(customers["Segment"].unique()))
    min_value = c2.number_input("Minimum customer value",min_value=0.0,value=0.0,step=1000.0)
    min_purchases = c3.number_input("Minimum purchases",min_value=0,value=0,step=1)

    f = customers[customers["Segment"].isin(seg_filter) & (customers["Customer Value"]>=min_value) & (customers["Purchases"]>=min_purchases)].copy()
    f["Priority Score"] = f.apply(priority_score,axis=1)
    st.info(f"Showing {len(f):,} of {len(customers):,} customers.")

    st.dataframe(f.sort_values("Priority Score",ascending=False),use_container_width=True,hide_index=True)

    c1,c2 = st.columns(2)
    with c1:
        fig = px.scatter(f,x="Purchases",y="Customer Value",size="Total Spend",color="Segment",hover_name="Customer",title="Customer Value vs Purchases")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig = px.histogram(f,x="Customer Value",color="Segment",title="Customer Value Distribution",nbins=15)
        st.plotly_chart(fig,use_container_width=True)

# ============================================================
# AI TARGET CUSTOMERS
# ============================================================

elif page == "🎯 AI Target Customers":
    st.title("🎯 AI Target Customers")
    st.caption("A multi-factor priority engine ranks customers by value, engagement and campaign fit.")

    strategy = st.selectbox("Growth strategy",[
        "Maximize Revenue","Upsell / Premium Upgrade","Cross-Sell",
        "Retention","Re-Engagement","High-Value Relationship"
    ])
    limit = st.slider("Customers to target",5,min(25,len(customers)),10)

    work = customers.copy()
    work["Priority Score"] = work.apply(priority_score,axis=1)

    if strategy == "Maximize Revenue":
        work["Strategy Score"] = work["Priority Score"] + work["Customer Value"]/max(work["Customer Value"].max(),1)*25
    elif strategy == "Upsell / Premium Upgrade":
        work["Strategy Score"] = work["Priority Score"] + np.where(work["Segment"].isin(["HIGH VALUE","LOYAL"]),15,0)
    elif strategy == "Cross-Sell":
        work["Strategy Score"] = work["Priority Score"] + np.where(work["Purchases"]<10,8,2)
    elif strategy == "Retention":
        work["Strategy Score"] = work["Priority Score"] + np.where(work["Segment"].isin(["HIGH VALUE","LOYAL"]),18,0)
    elif strategy == "Re-Engagement":
        work["Strategy Score"] = work["Priority Score"] + np.where(work["Segment"].isin(["STANDARD","GROWTH"]),15,0)
    else:
        work["Strategy Score"] = work["Priority Score"] + np.where(work["Segment"]=="HIGH VALUE",20,0)

    targets = work.sort_values("Strategy Score",ascending=False).head(limit)
    st.success(f"✅ {len(targets)} priority customers identified for **{strategy}**.")

    a,b,c,d = st.columns(4)
    a.metric("Targets",len(targets))
    b.metric("Target Value",f"₹{targets['Customer Value'].sum():,.0f}")
    c.metric("Avg Value",f"₹{targets['Customer Value'].mean():,.0f}")
    d.metric("Avg Purchases",f"{targets['Purchases'].mean():.1f}")

    st.dataframe(targets[["Customer","Segment","Customer Value","Purchases","Total Spend","Channel","Priority Score","Strategy Score"]],use_container_width=True,hide_index=True)

    fig = px.bar(targets.sort_values("Strategy Score"),x="Strategy Score",y="Customer",orientation="h",title=f"AI Priority Ranking — {strategy}")
    st.plotly_chart(fig,use_container_width=True)

# ============================================================
# CAMPAIGN PREDICTION
# ============================================================

elif page == "🔮 Campaign Prediction":
    st.title("🔮 Campaign Performance Prediction")
    st.caption("Predict response, expected revenue, campaign cost, ROI and the next-best action.")

    targets = customers.copy()
    targets["Priority Score"] = targets.apply(priority_score,axis=1)
    n = st.slider("Priority customers to forecast",1,min(15,len(targets)),min(5,len(targets)))
    targets = targets.sort_values("Priority Score",ascending=False).head(n)

    boost = st.slider("Campaign quality adjustment", -0.10, 0.15, 0.0, 0.01)
    revenue_rate = st.slider("Revenue realization rate",0.05,0.40,0.20,0.01)
    cost_rate = st.slider("Variable campaign cost rate",0.005,0.08,0.02,0.005)

    pred = prediction_table(targets,boost,revenue_rate,cost_rate)
    pred["ML Response"] = ml_probability(targets)
    pred["Blended Response"] = np.clip(pred["Response Probability"]*.45 + pred["ML Response"]*.55, .05,.98)
    pred["Expected Revenue"] = pred["Customer Value"]*pred["Blended Response"]*revenue_rate
    pred["Estimated ROI"] = (pred["Expected Revenue"]-pred["Campaign Cost"])/pred["Campaign Cost"]*100

    a,b,c,d = st.columns(4)
    a.metric("🎯 Priority Customers",len(pred))
    b.metric("💰 Expected Revenue",f"₹{pred['Expected Revenue'].sum():,.0f}")
    c.metric("💸 Campaign Cost",f"₹{pred['Campaign Cost'].sum():,.0f}")
    total_cost = pred["Campaign Cost"].sum()
    roi = (pred["Expected Revenue"].sum()-total_cost)/total_cost*100 if total_cost else 0
    d.metric("📊 Estimated ROI",f"{roi:.1f}%")

    display = pred.copy()
    for c in ["Customer Value","Expected Revenue","Campaign Cost"]:
        display[c] = display[c].map(lambda x:f"₹{x:,.0f}")
    for c in ["Response Probability","ML Response","Blended Response"]:
        display[c] = display[c].map(lambda x:f"{x*100:.1f}%")
    display["Estimated ROI"] = display["Estimated ROI"].map(lambda x:f"{x:.1f}%")
    st.dataframe(display,use_container_width=True,hide_index=True)

    fig = px.bar(pred,x="Customer",y="Expected Revenue",title="Expected Revenue by Customer",text_auto=".0f")
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("🧠 Prediction Method")
    st.write("RevPilot combines a transparent segment/behavior score with a Random Forest response model trained on a clearly labelled synthetic campaign-history simulation. The model is intended for project demonstration and should be retrained on real historical campaign outcomes before production use.")
    st.progress(float(np.mean(pred["Blended Response"])),text=f"Average predicted response: {np.mean(pred['Blended Response'])*100:.1f}%")

# ============================================================
# CAMPAIGN LAB
# ============================================================

elif page == "🧪 Campaign Lab":
    st.title("🧪 Campaign Lab — What-If Simulator")
    st.caption("Change budget, reach, offer quality and conversion assumptions to test campaign economics before launch.")

    targets = customers.assign(Priority=customers.apply(priority_score,axis=1)).sort_values("Priority",ascending=False)
    c1,c2,c3 = st.columns(3)
    selected = c1.multiselect("Target segments",sorted(customers["Segment"].unique()),default=["HIGH VALUE","LOYAL"])
    budget = c2.number_input("Campaign budget (₹)",500.0,1000000.0,10000.0,500.0)
    quality = c3.slider("Offer quality",0.50,1.50,1.00,0.05)

    reach = st.slider("Reach rate",0.10,1.00,0.80,0.05)
    conversion_lift = st.slider("Conversion lift",0.00,0.50,0.10,0.01)
    revenue_share = st.slider("Revenue captured per conversion",0.05,0.50,0.20,0.01)

    sim = targets[targets["Segment"].isin(selected)].copy()
    sim = sim[sim["Customer Value"] > 0]
    sim["Base Response"] = sim.apply(rule_response_probability,axis=1)
    sim["Sim Response"] = np.clip(sim["Base Response"]*quality*(1+conversion_lift)*reach,.01,.98)
    sim["Expected Revenue"] = sim["Customer Value"]*sim["Sim Response"]*revenue_share
    gross = sim["Expected Revenue"].sum()
    net = gross-budget
    sim_roi = net/budget*100 if budget else 0

    a,b,c,d = st.columns(4)
    a.metric("Reachable Customers",len(sim))
    b.metric("Expected Revenue",f"₹{gross:,.0f}")
    c.metric("Net Opportunity",f"₹{net:,.0f}")
    d.metric("Scenario ROI",f"{sim_roi:.1f}%")

    if sim_roi > 300: st.success("🚀 Strong scenario: economics look attractive.")
    elif sim_roi > 0: st.info("🟢 Positive scenario: test and optimize before scaling.")
    else: st.warning("⚠️ Negative scenario: reduce cost or improve conversion assumptions.")

    st.dataframe(sim[["Customer","Segment","Customer Value","Base Response","Sim Response","Expected Revenue"]].sort_values("Expected Revenue",ascending=False),use_container_width=True,hide_index=True)
    fig = px.scatter(sim,x="Sim Response",y="Expected Revenue",size="Customer Value",color="Segment",hover_name="Customer",title="Scenario Response vs Expected Revenue")
    st.plotly_chart(fig,use_container_width=True)

# ============================================================
# CAMPAIGN GENERATOR
# ============================================================

elif page == "📣 Campaign Generator":
    st.title("📣 AI Campaign Generator")
    st.caption("Turn a target audience into a campaign plan, offer, KPI framework and next-best actions.")

    c1,c2,c3 = st.columns(3)
    goal = c1.selectbox("Campaign goal",["Upsell","Cross-Sell","Retention","Re-Engagement","Premium Upgrade"])
    offer = c2.selectbox("Offer type",["Premium Upgrade","Bundle","Loyalty Reward","Limited-Time Offer","Personalized Recommendation"])
    channel = c3.selectbox("Primary channel",["Email","WhatsApp","Email + WhatsApp"])

    audience = st.selectbox("Audience",["Top Priority Customers","HIGH VALUE","LOYAL","GROWTH","STANDARD"])
    campaign_name = st.text_input("Campaign name",f"RevPilot {goal} Campaign")

    target = customers.copy()
    target["Priority Score"] = target.apply(priority_score,axis=1)
    if audience == "Top Priority Customers":
        target = target.sort_values("Priority Score",ascending=False).head(10)
    else:
        target = target[target["Segment"]==audience].sort_values("Priority Score",ascending=False).head(20)

    if st.button("🚀 Generate Campaign Plan",use_container_width=True):
        total = target["Customer Value"].sum()
        response = target.apply(rule_response_probability,axis=1).mean() if len(target) else 0
        expected = total*response*.20
        st.success(f"Campaign **{campaign_name}** generated for {len(target)} customers.")

        a,b,c = st.columns(3)
        a.metric("Audience",len(target))
        b.metric("Audience Value",f"₹{total:,.0f}")
        c.metric("Expected Revenue",f"₹{expected:,.0f}")

        st.subheader("🎯 Strategy")
        st.write(f"**Objective:** {goal}.  **Offer:** {offer}.  **Channel:** {channel}.")
        st.write("Prioritize the highest-value customers first, personalize the offer using purchase behavior, and use response/ROI thresholds to control campaign spend.")

        st.subheader("📌 KPI Framework")
        kpis = pd.DataFrame([
            ["Reach",len(target),"Customers eligible for campaign"],
            ["Predicted response",f"{response*100:.1f}%","Modelled campaign response"],
            ["Expected revenue",f"₹{expected:,.0f}","Forecasted incremental revenue"],
            ["Target ROI","> 300%","Recommended decision threshold"],
            ["Next action","Scale winners","Move high performers into the next campaign"],
        ],columns=["KPI","Target","Definition"])
        st.table(kpis)

        st.subheader("🗂️ Target Audience")
        st.dataframe(target[["Customer","Segment","Customer Value","Purchases","Channel","Priority Score"]],use_container_width=True,hide_index=True)

# ============================================================
# AI MESSAGES
# ============================================================

elif page == "💬 AI Messages":
    st.title("💬 AI-Generated Customer Messages")
    st.caption("Personalized message drafts based on customer segment, value, campaign goal and channel.")

    c1,c2,c3 = st.columns(3)
    tone = c1.selectbox("Tone",["Professional","Friendly","Premium","Urgent"])
    offer = c2.selectbox("Offer",["premium upgrade","bundle recommendation","loyalty reward","special upgrade","cross-sell opportunity"])
    channel = c3.selectbox("Channel",["Email","WhatsApp","Email + WhatsApp"])

    n = st.slider("Number of customers",1,min(10,len(customers)),5)
    targets = customers.assign(Priority=customers.apply(priority_score,axis=1)).sort_values("Priority",ascending=False).head(n)

    for _,row in targets.iterrows():
        st.subheader(f"👤 {row['Customer']}")
        st.info(make_message(row,offer,tone,channel))
        st.caption(f"Segment: {row['Segment']}  |  Customer Value: ₹{row['Customer Value']:,.0f}  |  Recommended channel: {row['Channel']}")

# ============================================================
# CUSTOMER 360
# ============================================================

elif page == "👤 Customer 360":
    st.title("👤 Customer 360")
    customer_id = st.selectbox("Select customer",customers["Customer"].tolist())
    row = customers[customers["Customer"]==customer_id].iloc[0]
    response = rule_response_probability(row)
    ml = float(ml_probability(pd.DataFrame([row]))[0])
    expected = float(row["Customer Value"])*((response*.45)+(ml*.55))*.20
    cost = max(500,float(row["Customer Value"])*.02)
    roi = (expected-cost)/cost*100 if cost else 0

    a,b,c,d = st.columns(4)
    a.metric("Segment",row["Segment"])
    b.metric("Customer Value",f"₹{row['Customer Value']:,.0f}")
    c.metric("Purchases",f"{row['Purchases']:,.0f}")
    d.metric("Priority Score",f"{priority_score(row):.1f}")

    st.subheader("📊 Customer Economics")
    x,y = st.columns(2)
    with x:
        st.metric("Total Spend",f"₹{row['Total Spend']:,.0f}")
        st.metric("Average Order Value",f"₹{row['Avg Order Value']:,.0f}")
        st.metric("Value per Purchase",f"₹{row['Value per Purchase']:,.0f}")
    with y:
        st.metric("Rule Response",f"{response*100:.1f}%")
        st.metric("ML Response",f"{ml*100:.1f}%")
        st.metric("Forecast ROI",f"{roi:.1f}%")

    st.subheader("🧠 Next-Best Actions")
    if row["Segment"]=="HIGH VALUE":
        actions=["Offer premium upgrade","Assign high-touch relationship treatment","Use Email + WhatsApp personalization"]
    elif row["Segment"]=="LOYAL":
        actions=["Offer loyalty reward","Recommend complementary product","Use personalized cross-sell"]
    elif row["Segment"]=="GROWTH":
        actions=["Nurture toward next purchase","Test bundle offer","Use engagement-focused messaging"]
    else:
        actions=["Use low-cost nurture","Test first conversion offer","Avoid expensive campaign spend"]
    for act in actions:
        st.write("✅",act)

    st.subheader("💬 Personalized Draft")
    st.code(make_message(row,"premium upgrade","Friendly",row["Channel"]))

# ============================================================
# BUSINESS ANALYTICS
# ============================================================

elif page == "📈 Business Analytics":
    st.title("📈 Business Analytics")
    st.caption("Executive-level analysis of value concentration, segment economics and channel mix.")

    byseg = customers.groupby("Segment").agg(
        Customers=("Customer","count"),
        Customer_Value=("Customer Value","sum"),
        Spend=("Total Spend","sum"),
        Purchases=("Purchases","sum")
    ).reset_index()
    byseg["Avg Value"] = byseg["Customer_Value"]/byseg["Customers"]
    byseg["Spend Efficiency"] = byseg["Spend"]/byseg["Customer_Value"].replace(0,np.nan)

    st.dataframe(byseg.round(2),use_container_width=True,hide_index=True)

    c1,c2 = st.columns(2)
    with c1:
        fig=px.bar(byseg,x="Segment",y="Customer_Value",title="Customer Value by Segment",text_auto=".0f")
        st.plotly_chart(fig,use_container_width=True)
    with c2:
        ch=customers.groupby("Channel",as_index=False)["Customer Value"].sum()
        fig=px.pie(ch,names="Channel",values="Customer Value",title="Customer Value by Channel",hole=.45)
        st.plotly_chart(fig,use_container_width=True)

    st.subheader("📌 Key Insights")
    top = customers.sort_values("Customer Value",ascending=False).head(5)
    share = top["Customer Value"].sum()/customers["Customer Value"].sum()*100 if customers["Customer Value"].sum() else 0
    st.write(f"• Top 5 customers represent **{share:.1f}%** of total customer value.")
    st.write(f"• The highest-value customer is **{top.iloc[0]['Customer']}** with ₹{top.iloc[0]['Customer Value']:,.0f}.")
    st.write(f"• **{high_value if 'high_value' in globals() else int((customers['Segment']=='HIGH VALUE').sum())}** customers are classified as HIGH VALUE.")
    best_seg=byseg.sort_values("Avg Value",ascending=False).iloc[0]
    st.write(f"• Highest average customer value segment: **{best_seg['Segment']}** at ₹{best_seg['Avg Value']:,.0f}.")

# ============================================================
# ML MODEL CENTER
# ============================================================

elif page == "🤖 ML Model Center":
    st.title("🤖 ML Model Center")
    st.caption("Transparent machine-learning layer for campaign response and revenue intelligence.")

    a,b,c = st.columns(3)
    a.metric("Model", "Random Forest")
    b.metric("Validation Accuracy", f"{model_accuracy*100:.1f}%")
    c.metric("Features", len(model_features))

    st.warning("⚠️ The training history used here is synthetic because the demo dataset does not contain historical campaign outcomes. For a real deployment, replace the synthetic labels with actual sent/responded/revenue outcomes.")

    importance = pd.DataFrame({"Feature":model_features,"Importance":clf.feature_importances_}).sort_values("Importance",ascending=False)
    fig=px.bar(importance,x="Importance",y="Feature",orientation="h",title="Response Model Feature Importance")
    st.plotly_chart(fig,use_container_width=True)

    st.subheader("📚 Features Used")
    st.write(", ".join(model_features))
    st.subheader("🔬 Model Governance")
    st.write("The app exposes assumptions, response probabilities and forecast formulas so a reviewer can understand why a recommendation was produced. Synthetic training is clearly labelled and should not be presented as production validation.")

# ============================================================
# DATA & EXPORT
# ============================================================

elif page == "✨ About Developer & Project":
    st.markdown("""
    <div class="rp-hero">
      <div class="rp-eyebrow">Developer Profile • Portfolio Project</div>
      <h1>About RevPilot AI</h1>
      <div class="desc">A revenue intelligence prototype created to demonstrate practical analytics, machine learning, campaign intelligence and product-focused UI/UX.</div>
      <div class="rp-status"><span class="rp-dot"></span> Built &amp; Designed by Prajwal Y R</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.95])
    with left:
        st.markdown("""
        <div class="rp-kpi" style="min-height:220px;">
          <div class="label">CREATOR</div>
          <div class="value" style="font-size:2rem;">Prajwal Y R</div>
          <div class="hint">Creator &amp; Developer of RevPilot AI</div>
          <div style="margin-top:1.2rem;color:#a78bfa;font-weight:750;">Razorpay Internship Portfolio Demo</div>
        </div>
        """, unsafe_allow_html=True)
    with right:
        st.markdown("### Project Focus")
        st.write("RevPilot AI turns customer and sales data into actionable revenue decisions through segmentation, prioritisation, campaign prediction, what-if analysis and AI-assisted campaign creation.")
        st.markdown("### Technology Stack")
        st.markdown("""
        <div class="rp-pills">
          <span>Python</span><span>Machine Learning</span><span>Scikit-Learn</span><span>Pandas</span><span>Plotly</span><span>UI/UX Design</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Project Highlights")
    h1,h2,h3,h4 = st.columns(4)
    highlights = [
        (h1,"🎯 Campaign Prediction","Estimate response, revenue, campaign cost and ROI."),
        (h2,"👤 Customer 360","Explore customer value, behaviour and segment context."),
        (h3,"🧪 Campaign Lab","Run what-if scenarios before committing campaign budget."),
        (h4,"🤖 ML Center","Inspect model features, validation and governance notes."),
    ]
    for col,title,body in highlights:
        with col:
            st.markdown(f'<div class="rp-kpi"><div class="label">{title}</div><div class="hint" style="margin-top:.8rem;line-height:1.6;">{body}</div></div>', unsafe_allow_html=True)

    st.markdown("### Developer Links")
    if GITHUB_URL or LINKEDIN_URL or PORTFOLIO_URL:
        links=[]
        if GITHUB_URL: links.append(f'<a href="{GITHUB_URL}" target="_blank">GitHub ↗</a>')
        if LINKEDIN_URL: links.append(f'<a href="{LINKEDIN_URL}" target="_blank">LinkedIn ↗</a>')
        if PORTFOLIO_URL: links.append(f'<a href="{PORTFOLIO_URL}" target="_blank">Portfolio ↗</a>')
        st.markdown('<div class="rp-link-row">' + ''.join(links) + '</div>', unsafe_allow_html=True)
    else:
        st.info("Add your real GitHub, LinkedIn and Portfolio URLs at the top of app.py to activate these buttons.")

    st.markdown("### Portfolio Note")
    st.write("RevPilot AI is presented as an internship portfolio demonstration. Forecasts and model outputs are decision-support estimates and should be validated against real historical campaign outcomes before production use.")

elif page == "📥 Data & Export":
    st.title("📥 Data & Export Center")
    st.caption("Inspect the active dataset and download analysis-ready files.")

    st.dataframe(customers,use_container_width=True,hide_index=True)

    prediction = prediction_table(customers.sort_values("Customer Value",ascending=False).head(min(20,len(customers))))
    csv_bytes = customers.to_csv(index=False).encode("utf-8")
    pred_bytes = prediction.to_csv(index=False).encode("utf-8")

    c1,c2,c3 = st.columns(3)
    c1.download_button("⬇️ Download Customer Data",csv_bytes,"revpilot_customers.csv","text/csv",use_container_width=True)
    c2.download_button("⬇️ Download Forecast",pred_bytes,"revpilot_campaign_forecast.csv","text/csv",use_container_width=True)

    xlsx = BytesIO()
    with pd.ExcelWriter(xlsx,engine="openpyxl") as writer:
        customers.to_excel(writer,index=False,sheet_name="Customers")
        prediction.to_excel(writer,index=False,sheet_name="Forecast")
        customers.groupby("Segment").agg(Customers=("Customer","count"),Value=("Customer Value","sum"),Spend=("Total Spend","sum")).reset_index().to_excel(writer,index=False,sheet_name="Segments")
    c3.download_button("⬇️ Download Excel Report",xlsx.getvalue(),"revpilot_report.xlsx","application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",use_container_width=True)

    st.markdown("---")
    st.subheader("ℹ️ Project Metadata")
    st.write(f"Generated: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    st.write("RevPilot is a decision-support prototype. Forecasts are estimates, not guaranteed outcomes.")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.caption("🚀 RevPilot AI • Revenue Intelligence OS • Built & Designed by Prajwal Y R • Razorpay Internship Portfolio Demo")

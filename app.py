import io
import hashlib
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="RevPilot AI — Revenue Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
LOGO_CANDIDATES = [
    BASE_DIR / "revpilot_logo.png",
    BASE_DIR / "assets" / "revpilot_logo.png",
    BASE_DIR / "revpilot_icon.png",
    BASE_DIR / "assets" / "revpilot_icon.png",
]
GITHUB_URL = "https://github.com/prajwalyr849-sudo"
LINKEDIN_URL = "https://www.linkedin.com/"
PORTFOLIO_URL = GITHUB_URL


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root{--bg:#05070d;--panel:#0a1020;--line:rgba(139,92,246,.24);--purple:#8b5cf6;--cyan:#22d3ee;--green:#34d399;--text:#f8fafc;--muted:#8fa0b8}
    html,body,[class*="css"]{font-family:Inter,sans-serif}
    .stApp{background:radial-gradient(900px 500px at 72% -10%,rgba(124,58,237,.20),transparent 60%),radial-gradient(700px 500px at 5% 25%,rgba(34,211,238,.07),transparent 60%),linear-gradient(180deg,#05070d,#070b15 65%,#05070d);color:var(--text)}
    [data-testid="stHeader"]{background:rgba(5,7,13,.72)}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#060912,#080d18);border-right:1px solid rgba(139,92,246,.18)}
    [data-testid="stSidebar"]>div:first-child{padding:18px 14px 22px}
    .topbar{display:flex;align-items:center;justify-content:space-between;margin:2px 0 22px;padding:10px 2px}.topbar-title{font-size:15px;font-weight:800;letter-spacing:.5px}.topbar-sub{font-size:12px;color:var(--muted);margin-top:3px}
    .live-pill{display:inline-flex;align-items:center;gap:7px;border:1px solid rgba(52,211,153,.28);background:rgba(52,211,153,.08);color:#6ee7b7;border-radius:999px;padding:7px 11px;font-size:12px;font-weight:700}.live-dot{width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 12px #34d399}
    .brand{padding:15px;border:1px solid rgba(139,92,246,.25);border-radius:22px;background:linear-gradient(145deg,rgba(20,17,48,.94),rgba(8,15,28,.94));margin-bottom:18px}.brand-title{font-size:23px;font-weight:800;margin-top:8px}.brand-sub{color:#9faecc;font-size:13px;margin-top:4px}.brand-meta{color:#6ee7b7;font-size:12px;font-weight:700;margin-top:12px}
    .section-label{font-size:10px;letter-spacing:2px;color:#71809a;font-weight:800;margin:20px 0 8px;text-transform:uppercase}
    .hero{position:relative;overflow:hidden;padding:34px 38px;border-radius:28px;border:1px solid rgba(139,92,246,.30);background:linear-gradient(135deg,rgba(34,20,72,.88),rgba(7,15,29,.96));box-shadow:0 25px 70px rgba(0,0,0,.24);margin-bottom:22px}.hero:after{content:"";position:absolute;width:280px;height:280px;border-radius:50%;right:-120px;top:-130px;background:rgba(139,92,246,.14);filter:blur(25px)}
    .eyebrow{position:relative;z-index:1;letter-spacing:3px;color:#a78bfa;font-weight:800;font-size:11px}.hero h1{position:relative;z-index:1;font-size:42px;line-height:1.08;margin:12px 0}.hero p{position:relative;z-index:1;color:#aebbd0;font-size:16px;line-height:1.75;max-width:820px}.hero-actions{position:relative;z-index:1;display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}.hero-chip{padding:8px 12px;border-radius:999px;border:1px solid rgba(139,92,246,.25);background:rgba(139,92,246,.09);color:#ddd6fe;font-size:12px;font-weight:700}
    .metric{height:100%;min-height:118px;padding:20px 20px 17px;border-radius:20px;border:1px solid rgba(139,92,246,.20);background:linear-gradient(145deg,#0d1527,#09101d);box-shadow:inset 0 1px 0 rgba(255,255,255,.02)}.metric-label{font-size:10px;letter-spacing:1.7px;color:#8292ab;font-weight:800;text-transform:uppercase}.metric-value{font-size:28px;font-weight:800;margin-top:10px;letter-spacing:-.5px}.metric-note{font-size:11px;color:#5ee7b7;margin-top:5px}
    .section-title{font-size:25px;font-weight:800;margin:8px 0 16px}.panel{padding:18px;border-radius:22px;border:1px solid rgba(139,92,246,.18);background:rgba(9,15,28,.72);box-shadow:0 16px 50px rgba(0,0,0,.13)}
    .profile{padding:18px;border-radius:20px;border:1px solid rgba(34,211,238,.18);background:linear-gradient(145deg,rgba(10,28,43,.72),rgba(10,15,29,.84))}.profile-name{font-size:22px;font-weight:800}.profile-meta{color:#9eacc0;font-size:13px;margin-top:5px}.profile-value{font-size:25px;font-weight:800;color:#67e8f9;margin-top:12px}
    .empty{padding:75px 30px;text-align:center;border:1px dashed rgba(139,92,246,.28);border-radius:26px;background:rgba(8,14,27,.62)}.empty-icon{font-size:62px}.empty h2{font-size:28px;margin:14px 0 8px}.empty p{color:var(--muted);max-width:650px;margin:0 auto;line-height:1.8}.about-card{height:100%;padding:22px;border-radius:20px;border:1px solid rgba(139,92,246,.18);background:rgba(10,16,30,.72)}.about-card p{color:#94a3b8;line-height:1.65;font-size:13px}.tag{display:inline-block;padding:7px 11px;margin:4px;border-radius:999px;background:rgba(139,92,246,.10);border:1px solid rgba(139,92,246,.20);color:#ddd6fe;font-size:12px}
    .stButton>button,.stDownloadButton>button{border-radius:12px;font-weight:700;border:1px solid rgba(139,92,246,.25)}
    @media(max-width:800px){.hero{padding:26px 22px}.hero h1{font-size:31px}.hero p{font-size:14px}.metric{min-height:104px}.metric-value{font-size:24px}.section-title{font-size:22px}}
    </style>
    """, unsafe_allow_html=True)


def clean_number(series, default=0.0):
    if series is None:
        return pd.Series(dtype="float64")
    s = series.astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce").fillna(default)


def first_existing(df, aliases):
    normalized = {str(c).strip().lower().replace(" ", "_"): c for c in df.columns}
    for alias in aliases:
        key = alias.lower().replace(" ", "_")
        if key in normalized:
            return normalized[key]
    for c in df.columns:
        key = str(c).strip().lower().replace(" ", "_")
        if any(alias.lower().replace(" ", "_") in key for alias in aliases):
            return c
    return None


def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    df.columns = [str(c).strip() for c in df.columns]
    aliases = {
        "Customer ID": ["customer_id", "customerid", "id", "cust_id", "customer"],
        "Name": ["name", "customer_name", "customername", "full_name", "fullname"],
        "Email": ["email", "email_address", "mail"],
        "Phone": ["phone", "mobile", "phone_number", "contact"],
        "City": ["city", "location", "town"],
        "Revenue": ["revenue", "gmv", "sales", "total_revenue", "customer_value", "value", "amount"],
        "Purchases": ["purchases", "orders", "order_count", "transactions", "purchase_count"],
        "Spend": ["spend", "marketing_spend", "ad_spend", "cost", "total_spend"],
        "Channel": ["channel", "source", "acquisition_channel", "marketing_channel"],
        "Segment": ["segment", "customer_segment", "category", "tier"],
    }
    for target, names in aliases.items():
        src = first_existing(df, names)
        if src is not None and src != target:
            df[target] = df[src]
        elif target not in df.columns:
            if target in {"Name", "Email", "Phone", "City", "Channel", "Segment"}:
                df[target] = "Unknown"
            else:
                df[target] = 0

    if df.empty:
        return df

    df["Customer ID"] = df["Customer ID"].astype(str).replace("nan", "Unknown")
    df["Name"] = df["Name"].astype(str).replace("nan", "Unknown")
    for c in ["Email", "Phone", "City", "Channel"]:
        df[c] = df[c].fillna("Unknown").astype(str)

    df["Revenue"] = clean_number(df["Revenue"])
    df["Purchases"] = clean_number(df["Purchases"])
    df["Spend"] = clean_number(df["Spend"])
    df["Purchases"] = df["Purchases"].clip(lower=0)
    df["Revenue"] = df["Revenue"].clip(lower=0)
    df["Spend"] = df["Spend"].clip(lower=0)

    if df["Channel"].eq("Unknown").all():
        channels = np.array(["Organic", "Paid", "Referral", "Direct"])
        df["Channel"] = channels[np.arange(len(df)) % len(channels)]

    segment = df["Segment"].astype(str).str.upper().str.strip()
    valid = {"HIGH VALUE", "LOYAL", "GROWTH", "STANDARD"}
    if not segment.isin(valid).all() or segment.eq("UNKNOWN").all():
        q75, q50, q25 = df["Revenue"].quantile([.75, .50, .25]).tolist()
        if q75 == q25:
            score = df["Revenue"]
            df["Segment"] = np.select(
                [score >= score.mean() * 1.5, df["Purchases"] >= df["Purchases"].median()],
                ["HIGH VALUE", "LOYAL"], default="STANDARD"
            )
        else:
            df["Segment"] = np.select(
                [df["Revenue"] >= q75, (df["Purchases"] >= df["Purchases"].quantile(.65)) & (df["Revenue"] >= q50), df["Revenue"] >= q25],
                ["HIGH VALUE", "LOYAL", "GROWTH"], default="STANDARD"
            )
    else:
        df["Segment"] = segment

    df["Avg Order Value"] = np.divide(df["Revenue"], df["Purchases"].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0)
    df["Spend Ratio"] = np.divide(df["Spend"], df["Revenue"].replace(0, np.nan)).replace([np.inf, -np.inf], np.nan).fillna(0)
    df["Customer Value"] = df["Revenue"]
    return df


@st.cache_data(show_spinner=False)
def demo_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 160
    revenue = np.round(rng.lognormal(8.2, 0.9, n), 2)
    purchases = rng.integers(1, 28, n)
    spend = np.round(revenue * rng.uniform(.02, .18, n), 2)
    return normalize(pd.DataFrame({
        "Customer ID": [f"CUST-{i:04d}" for i in range(1, n + 1)],
        "Name": [f"Customer {i}" for i in range(1, n + 1)],
        "Email": [f"customer{i}@example.com" for i in range(1, n + 1)],
        "Phone": [f"+91 90000 {i:05d}" for i in range(1, n + 1)],
        "City": rng.choice(["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai"], n),
        "Revenue": revenue,
        "Purchases": purchases,
        "Spend": spend,
        "Channel": rng.choice(["Organic", "Paid", "Referral", "Direct"], n),
    }))


def money(v):
    return f"₹{v:,.0f}"


def metric(label, value, note=""):
    st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)


def load_data():
    if "file_signature" not in st.session_state:
        st.session_state.file_signature = None
    if "data" not in st.session_state:
        st.session_state.data = None
    if "filename" not in st.session_state:
        st.session_state.filename = None

    upload = st.sidebar.file_uploader("Upload CSV, XLSX or XLS", type=["csv", "xlsx", "xls"], key="dataset_upload")
    if upload is not None:
        data_bytes = upload.getvalue()
        signature = hashlib.sha256(data_bytes).hexdigest()
        if signature != st.session_state.file_signature:
            with st.spinner("Processing dataset…"):
                st.session_state.data = normalize(parse_uploaded_file(data_bytes, upload.name))
                st.session_state.file_signature = signature
                st.session_state.filename = upload.name
            st.sidebar.success(f"Loaded {len(st.session_state.data):,} rows")
        elif st.session_state.data is not None:
            st.sidebar.success("Dataset ready — cached")
    return st.session_state.data


def sidebar():
    logo = next((p for p in LOGO_CANDIDATES if p.exists()), None)
    if logo:
        st.sidebar.image(str(logo), use_container_width=True)
    st.sidebar.markdown('<div class="brand"><div class="brand-title">RevPilot AI</div><div class="brand-sub">Revenue Intelligence OS</div><div class="brand-meta">● LIVE DATA ENGINE</div></div>', unsafe_allow_html=True)
    st.sidebar.markdown('<div class="section-label">Workspace</div>', unsafe_allow_html=True)
    page = st.sidebar.radio("Navigation", ["🏠 Executive Dashboard","👥 Customer Intelligence","🎯 AI Target Customers","🔮 Campaign Prediction","📈 Revenue Analytics","💬 AI Outreach & Engagement","⚙️ Data & Settings","ℹ️ About"], label_visibility="collapsed")
    st.sidebar.markdown('<div class="section-label">Data source</div>', unsafe_allow_html=True)
    data = load_data()
    st.sidebar.caption(f"✓ {len(data):,} records ready" if data is not None else "Upload CSV, XLSX or XLS")
    st.sidebar.markdown('<div class="section-label">Developer</div>', unsafe_allow_html=True)
    st.sidebar.caption("Prajwal Y R • Razorpay Internship Portfolio Demo")
    return page, data


def landing():
    st.markdown("""
    <div class="topbar"><div><div class="topbar-title">REVPILOT AI</div><div class="topbar-sub">Revenue Intelligence Workspace</div></div><div class="live-pill"><span class="live-dot"></span>Waiting for data</div></div>
    <div class="hero"><div class="eyebrow">AI REVENUE INTELLIGENCE</div><h1>Turn customer data into<br>revenue decisions.</h1><p>RevPilot AI combines customer segmentation, priority scoring, campaign forecasting, interactive analytics and personalized outreach in one focused workspace.</p><div class="hero-actions"><span class="hero-chip">🎯 Smart targeting</span><span class="hero-chip">📊 Revenue analytics</span><span class="hero-chip">🤖 AI outreach</span><span class="hero-chip">⚡ Fast data pipeline</span></div></div>
    <div class="empty"><div class="empty-icon">📂</div><h2>Start with your dataset</h2><p>Upload a CSV, XLSX or XLS file from the sidebar. RevPilot will automatically recognize common customer, revenue, order and marketing columns and build your workspace.</p></div>
    """, unsafe_allow_html=True)


def dashboard(df):
    st.markdown('<div class="topbar"><div><div class="topbar-title">EXECUTIVE OVERVIEW</div><div class="topbar-sub">Live revenue intelligence from your dataset</div></div><div class="live-pill"><span class="live-dot"></span>Dataset active</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Executive Dashboard</div>', unsafe_allow_html=True)
    c=st.columns(4)
    vals=[(f"{len(df):,}","Customers","Live records"),(money(df['Customer Value'].sum()),"Customer Value","Total revenue"),(money(df['Customer Value'].mean()),"Avg Customer Value","Per customer"),(f"{(df['Segment']=='HIGH VALUE').sum():,}","High-Value Customers","Priority segment")]
    for col,(v,l,n) in zip(c,vals):
        with col: metric(l,v,n)
    left,right=st.columns([1.15,.85])
    with left:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        seg=df.groupby('Segment',as_index=False)['Customer Value'].sum().sort_values('Customer Value',ascending=False)
        fig=px.bar(seg,x='Segment',y='Customer Value',text_auto='.2s',title='Customer Value by Segment')
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',margin=dict(l=5,r=5,t=45,b=5),font=dict(size=12))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with right:
        st.markdown('<div class="panel">',unsafe_allow_html=True)
        ch=df.groupby('Channel',as_index=False)['Spend'].sum()
        fig=px.pie(ch,names='Channel',values='Spend',hole=.62,title='Marketing Spend by Channel')
        fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',margin=dict(l=5,r=5,t=45,b=5),showlegend=True)
        st.plotly_chart(fig,use_container_width=True)
        st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">🏆 Top Revenue Customers</div>',unsafe_allow_html=True)
    cols=['Customer ID','Name','Segment','Revenue','Purchases','Spend','Channel']
    st.dataframe(df.nlargest(10,'Revenue')[cols],use_container_width=True,hide_index=True,height=360)


def customer_intelligence(df):
    st.markdown("## 👥 Customer Intelligence")
    options = sorted(df["Segment"].dropna().unique().tolist())
    selected = st.multiselect("Filter segments", options, default=options)
    view = df[df["Segment"].isin(selected)] if selected else df.iloc[0:0]
    c = st.columns(3)
    with c[0]: metric("Customers", f"{len(view):,}")
    with c[1]: metric("Revenue", money(view["Revenue"].sum()))
    with c[2]: metric("Avg Order Value", money(view["Avg Order Value"].mean()))
    st.dataframe(view, use_container_width=True, hide_index=True)


def target_customers(df):
    st.markdown("## 🎯 AI Target Customers")
    st.caption("Priority score = Value 45% + Purchases 25% + Spend Ratio 10% + Segment Bonus 20%.")
    d = df.copy()
    def pct_rank(s):
        return s.rank(pct=True).fillna(0)
    d["Value Score"] = pct_rank(d["Customer Value"]) * 45
    d["Purchase Score"] = pct_rank(d["Purchases"]) * 25
    d["Spend Score"] = (1 - pct_rank(d["Spend Ratio"])) * 10
    bonus = d["Segment"].map({"HIGH VALUE":20,"LOYAL":16,"GROWTH":12,"STANDARD":6}).fillna(0)
    d["Priority Score"] = d["Value Score"] + d["Purchase Score"] + d["Spend Score"] + bonus
    top_n = st.slider("Top customers", 5, min(100, len(d)), min(20, len(d)), 5)
    top = d.nlargest(top_n, "Priority Score").sort_values("Priority Score")
    fig = px.bar(top, x="Priority Score", y="Name", color="Segment", orientation="h", title="AI Priority Ranking", hover_data=["Revenue","Purchases","Spend Ratio"])
    fig.update_layout(template="plotly_dark", margin=dict(l=10,r=10,t=50,b=10), autosize=True)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(d.nlargest(top_n, "Priority Score")[["Customer ID","Name","Segment","Revenue","Purchases","Spend Ratio","Priority Score"]], use_container_width=True, hide_index=True)


def campaign_prediction(df):
    st.markdown("## 🔮 Campaign Prediction")
    a,b,c = st.columns(3)
    with a: quality = st.slider("Campaign quality adjustment", 50, 150, 100, 5) / 100
    with b: realization = st.slider("Revenue realization rate", 20, 100, 70, 5) / 100
    with c: cost_rate = st.slider("Variable cost rate", 1, 40, 12, 1) / 100
    base_response = float(np.clip(.04 + min(0.12, df["Purchases"].mean()/300), .02, .16))
    blended = float(np.clip(base_response * quality, .01, .35))
    audience = len(df)
    expected_orders = audience * blended
    avg_value = float(df["Avg Order Value"].mean()) if len(df) else 0
    expected_revenue = expected_orders * avg_value * realization
    campaign_cost = expected_revenue * cost_rate
    profit = expected_revenue - campaign_cost
    roi = (profit / campaign_cost * 100) if campaign_cost > 0 else 0
    cols = st.columns(4)
    for col,label,val in zip(cols,["Blended Response","Expected Revenue","Campaign Cost","ROI"],[f"{blended*100:.1f}%",money(expected_revenue),money(campaign_cost),f"{roi:.1f}%"]):
        with col: metric(label,val,"Model estimate")
    st.info("Forecasts are estimates for portfolio/demo decision support, not guaranteed outcomes.")


def revenue_analytics(df):
    st.markdown("## 📈 Revenue Analytics")
    numeric = ["Revenue","Customer Value","Purchases","Spend","Avg Order Value","Spend Ratio"]
    metric_name = st.selectbox("Distribution metric", numeric)
    fig = px.histogram(df, x=metric_name, marginal="box", nbins=35, title=f"{metric_name} Distribution")
    fig.update_layout(template="plotly_dark", margin=dict(l=10,r=10,t=50,b=10), autosize=True)
    st.plotly_chart(fig, use_container_width=True)
    fig2 = px.scatter(df, x="Purchases", y="Customer Value", color="Segment", size="Spend", hover_name="Name", title="Purchases vs Customer Value")
    fig2.update_layout(template="plotly_dark", margin=dict(l=10,r=10,t=50,b=10), autosize=True)
    st.plotly_chart(fig2, use_container_width=True)


def make_message(row, objective, tone, channel):
    name = row.get("Name", "Customer")
    segment = row.get("Segment", "STANDARD")
    value = money(float(row.get("Customer Value", 0)))
    openings = {"Professional":"Hello {name},", "Friendly":"Hi {name}! 👋", "Urgent":"Hi {name}, quick opportunity for you:"}
    bodies = {
        "Win-back": f"We noticed it has been a while since your last purchase. Based on your previous value of {value}, we would love to welcome you back with a tailored offer.",
        "Upsell": f"As a valued {segment.lower()} customer, we found an opportunity that may be a strong fit for you. Your customer value with us is {value}.",
        "Exclusive Discount": f"We are offering you an exclusive benefit based on your customer relationship with us. Your previous value is {value}, and we would like to make your next purchase more rewarding.",
        "Loyalty Reward": f"Thank you for being a valued {segment.lower()} customer. Your relationship with us is worth {value}, and we have a special loyalty reward for you.",
    }
    closing = "Would you like me to share the details?"
    body = openings[tone].format(name=name) + "\n\n" + bodies[objective] + "\n\n" + closing
    if channel == "Email":
        return f"Subject: A personalized opportunity for you\n\n{body}\n\nRegards,\nRevPilot AI Team"
    return body


def outreach(df):
    st.markdown("## 💬 AI Outreach & Engagement")
    st.caption("Generate personalized, ready-to-send outreach from the selected customer record.")
    search = st.text_input("🔎 Find customer by name or ID")
    filtered = df
    if search.strip():
        q = search.strip().lower()
        filtered = df[df["Name"].str.lower().str.contains(q, na=False) | df["Customer ID"].str.lower().str.contains(q, na=False)]
    if filtered.empty:
        st.warning("No matching customer found.")
        return
    choices = filtered.index.tolist()
    selected_idx = st.selectbox("Target customer", choices, format_func=lambda i: f"{df.loc[i,'Name']} — {df.loc[i,'Customer ID']} — {df.loc[i,'Segment']}")
    row = df.loc[selected_idx]
    a,b,c = st.columns(3)
    with a: channel = st.selectbox("Outreach type", ["Email","WhatsApp/SMS","Both"])
    with b: objective = st.selectbox("Campaign objective", ["Win-back","Upsell","Exclusive Discount","Loyalty Reward"])
    with c: tone = st.selectbox("Tone", ["Professional","Friendly","Urgent"])
    st.markdown(f"**Customer:** {row['Name']}  •  **Segment:** {row['Segment']}  •  **Value:** {money(float(row['Customer Value']))}")
    if st.button("🤖 Generate AI Message", type="primary", use_container_width=True):
        msg = make_message(row, objective, tone, "Email" if channel == "Email" else "WhatsApp/SMS")
        if channel == "Both":
            st.session_state.generated_message = "EMAIL\n\n" + make_message(row, objective, tone, "Email") + "\n\n---\n\nWHATSAPP/SMS\n\n" + make_message(row, objective, tone, "WhatsApp/SMS")
        else:
            st.session_state.generated_message = msg
    if st.session_state.get("generated_message"):
        st.text_area("Ready-to-send message", st.session_state.generated_message, height=260)
        if st.button("🚀 Send Campaign via API", use_container_width=True):
            if "sent_log" not in st.session_state: st.session_state.sent_log = []
            st.session_state.sent_log.append({"Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"Customer":row["Name"],"Channel":channel,"Objective":objective,"Status":"✓ Simulated API Sent"})
            st.success("Campaign API simulation completed successfully.")
    if st.session_state.get("sent_log"):
        st.markdown("### 📜 Sent Log History")
        st.dataframe(pd.DataFrame(st.session_state.sent_log).iloc[::-1], use_container_width=True, hide_index=True)


def settings(df):
    st.markdown("## ⚙️ Data & Settings")
    c = st.columns(4)
    with c[0]: metric("Rows", f"{len(df):,}")
    with c[1]: metric("Columns", f"{len(df.columns):,}")
    with c[2]: metric("Revenue", money(df["Revenue"].sum()))
    with c[3]: metric("File Status", "Ready")
    st.markdown("### 🔐 Dataset Signature")
    st.code(st.session_state.get("file_signature") or "No uploaded file")
    st.markdown("### 👀 Dynamic Sample Preview")
    rows = st.slider("Preview rows", 5, min(50, len(df)), min(10, len(df)))
    st.dataframe(df.head(rows), use_container_width=True, hide_index=True)
    st.download_button("⬇️ Download Normalized CSV", df.to_csv(index=False).encode("utf-8"), "revpilot_normalized.csv", "text/csv", use_container_width=True)


def about_page():
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">ABOUT REVPILOT AI</div>
      <h1>RevPilot AI 🚀</h1>
      <p>Revenue Intelligence OS</p>
      <p>RevPilot AI transforms customer and sales data into actionable revenue intelligence through segmentation, customer prioritization, campaign prediction, analytics, and personalized outreach.</p>
      <span class="status">● AI-Powered Revenue Intelligence</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("## 🧠 Core Capabilities")
    cards = [
        ("👥 Customer Intelligence","Analyze revenue, purchases, spend, segments and customer-level signals."),
        ("🎯 AI Target Customers","Rank customers using value, purchases, spend ratio and segment signals."),
        ("🔮 Campaign Prediction","Estimate response, revenue realization, campaign cost and ROI."),
        ("📈 Revenue Analytics","Explore distributions and relationships with interactive Plotly charts."),
        ("💬 AI Outreach","Generate personalized Email, WhatsApp/SMS or combined messages."),
        ("🏠 Executive Dashboard","Monitor customer count, value, segments, channels and top revenue customers."),
    ]
    for start in range(0, len(cards), 2):
        cols = st.columns(2)
        for col, (title, text) in zip(cols, cards[start:start+2]):
            with col:
                st.markdown(f'<div class="about-card"><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)
        st.write("")
    st.markdown("## 🛠️ Technology Stack")
    st.markdown('<div style="text-align:center"><span class="tag">🐍 Python</span><span class="tag">⚡ Streamlit</span><span class="tag">🐼 Pandas</span><span class="tag">📊 Plotly</span><span class="tag">🤖 AI / ML</span><span class="tag">🔌 API Integration</span></div>', unsafe_allow_html=True)
    st.markdown("## 📂 Supported Data")
    st.markdown('<div class="card"><p class="small">CSV, XLSX and XLS datasets are normalized automatically. Common aliases such as customer_id, GMV, revenue, orders, spend, phone, email and city are recognized, while missing analytical fields are safely derived.</p></div>', unsafe_allow_html=True)
    st.markdown("## 👨‍💻 Developer")
    st.markdown(f'<div class="about-card" style="text-align:center"><div style="font-size:48px">👨‍💻</div><h2>Prajwal Y R</h2><p>Creator & Developer<br>Razorpay Internship Portfolio Demo</p><div class="linkbox"><a href="{LINKEDIN_URL}" target="_blank">🔗 LinkedIn</a> &nbsp;&nbsp; <a href="{GITHUB_URL}" target="_blank">💻 GitHub</a> &nbsp;&nbsp; <a href="{PORTFOLIO_URL}" target="_blank">🌐 Portfolio / Website</a></div></div>', unsafe_allow_html=True)
    st.markdown("---")
    st.caption("RevPilot AI • Revenue Intelligence OS • Built with Python & Streamlit")


def main():
    inject_css()
    page, df = sidebar()
    if page == "ℹ️ About":
        about_page()
        return
    if df is None or df.empty:
        landing()
        return
    if page == "🏠 Executive Dashboard": dashboard(df)
    elif page == "👥 Customer Intelligence": customer_intelligence(df)
    elif page == "🎯 AI Target Customers": target_customers(df)
    elif page == "🔮 Campaign Prediction": campaign_prediction(df)
    elif page == "📈 Revenue Analytics": revenue_analytics(df)
    elif page == "💬 AI Outreach & Engagement": outreach(df)
    elif page == "⚙️ Data & Settings": settings(df)


if __name__ == "__main__":
    main()

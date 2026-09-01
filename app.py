import io
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Iterable

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
    BASE_DIR / "revpilot_icon.png",
    BASE_DIR / "assets" / "revpilot_logo.png",
    BASE_DIR / "assets" / "revpilot_icon.png",
]
GITHUB_URL = "https://github.com/prajwalyr849-sudo"
LINKEDIN_URL = "https://www.linkedin.com/"
PORTFOLIO_URL = GITHUB_URL


def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root{--bg:#060912;--surface:#0b1120;--surface2:#11182a;--border:rgba(139,92,246,.34);--purple:#8b5cf6;--purple2:#a78bfa;--text:#f8fafc;--muted:#94a3b8;--green:#6ee7b7;}
    html,body,[class*="css"]{font-family:Inter,sans-serif}
    .stApp{background:radial-gradient(circle at 15% 0%,rgba(124,58,237,.16),transparent 28%),radial-gradient(circle at 90% 5%,rgba(37,99,235,.10),transparent 25%),linear-gradient(135deg,var(--bg),#080d18);color:var(--text)}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#070b15,#080d18);border-right:1px solid rgba(139,92,246,.18)}
    [data-testid="stSidebar"]>div:first-child{padding-top:.8rem}
    .logo-wrap{padding:4px 8px 14px;text-align:center}
    .logo-wrap img{max-height:92px;object-fit:contain;border-radius:16px}
    .brand-card,.hero,.card{background:linear-gradient(135deg,rgba(24,15,55,.88),rgba(8,15,30,.92));border:1px solid var(--border);border-radius:28px;box-shadow:0 18px 55px rgba(0,0,0,.20)}
    .brand-card{padding:20px;margin-bottom:18px}.brand-title{font-size:27px;font-weight:800}.brand-sub{color:#a5b4fc;font-size:15px;margin-top:5px}.status{display:inline-block;color:var(--green);font-weight:700;margin-top:14px}
    .hero{padding:42px;margin-bottom:24px}.eyebrow{letter-spacing:3px;color:#a78bfa;font-weight:800;font-size:13px}.hero h1{font-size:48px;margin:12px 0 10px}.hero p{color:#aeb9cc;font-size:18px;line-height:1.8;max-width:850px}
    .card{padding:24px;margin-bottom:18px;background:rgba(10,17,32,.72)}
    .metric{background:linear-gradient(145deg,#10182b,#0b1120);border:1px solid rgba(139,92,246,.28);border-radius:22px;padding:20px;min-height:120px}.metric-label{color:#94a3b8;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:1px}.metric-value{font-size:30px;font-weight:800;margin-top:8px}.metric-note{color:#6ee7b7;font-size:12px;margin-top:5px}
    .section-title{font-size:25px;font-weight:800;margin:24px 0 14px}.small{color:#94a3b8;font-size:14px;line-height:1.7}
    .linkbox a{color:#60a5fa;text-decoration:none;font-weight:600}.linkbox a:hover{text-decoration:underline}
    .about-card{height:100%;background:rgba(15,23,42,.72);border:1px solid rgba(139,92,246,.28);border-radius:22px;padding:25px}.about-card h3{margin-top:0}.about-card p{color:#94a3b8;line-height:1.7}
    .tag{display:inline-block;padding:7px 12px;margin:4px;border-radius:12px;background:rgba(139,92,246,.12);border:1px solid rgba(139,92,246,.25);color:#ddd6fe}
    .stButton>button,.stDownloadButton>button{border-radius:14px;font-weight:700}
    div[data-testid="stFileUploader"]{border-radius:18px}
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(show_spinner=False, max_entries=8)
def parse_uploaded_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    bio = io.BytesIO(file_bytes)
    lower = filename.lower()
    if lower.endswith(".csv"):
        # Keep memory use reasonable for large CSVs while still handling common encodings.
        try:
            return pd.read_csv(bio, low_memory=False)
        except UnicodeDecodeError:
            bio.seek(0)
            return pd.read_csv(bio, low_memory=False, encoding="latin-1")
    if lower.endswith(".xlsx"):
        return pd.read_excel(bio, engine="openpyxl")
    if lower.endswith(".xls"):
        return pd.read_excel(bio, engine="xlrd")
    raise ValueError("Unsupported file type. Upload CSV, XLSX or XLS.")


def clean_number(series: pd.Series, default: float = 0.0) -> pd.Series:
    if series is None:
        return pd.Series(dtype="float64")
    s = series.copy()
    if pd.api.types.is_numeric_dtype(s):
        return pd.to_numeric(s, errors="coerce").fillna(default).astype(float)
    s = s.astype("string")
    # Handle accounting negatives, Indian/US separators and currency symbols.
    s = s.str.replace(r"\(([^)]+)\)", r"-\1", regex=True)
    s = s.str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce").fillna(default).astype(float)


def canonical_name(value) -> str:
    text = str(value).strip().lower()
    text = text.replace("₹", "rs").replace("$", "usd")
    return "".join(ch for ch in text if ch.isalnum())


def first_existing(df: pd.DataFrame, aliases: Iterable[str]) -> Optional[str]:
    lookup = {canonical_name(c): c for c in df.columns}
    aliases = list(aliases)
    for alias in aliases:
        key = canonical_name(alias)
        if key in lookup:
            return lookup[key]
    # Fuzzy matching for headers such as Total GMV, Order Amount, Customer Email Address.
    for c in df.columns:
        key = canonical_name(c)
        for alias in aliases:
            a = canonical_name(alias)
            if a and (a in key or key in a):
                return c
    return None


def choose_numeric_source(df: pd.DataFrame, candidates: Iterable[str]) -> Optional[str]:
    src = first_existing(df, candidates)
    if src is not None:
        return src
    # If no named alias exists, pick a likely numeric amount column by name.
    for c in df.columns:
        key = canonical_name(c)
        if any(token in key for token in ("amount", "gmv", "sales", "revenue", "value", "price", "total")):
            if pd.api.types.is_numeric_dtype(df[c]):
                return c
    return None


def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    df = raw.copy()
    if df.empty:
        return df
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "Customer ID": ["customer_id", "customerid", "cust_id", "customer code", "customer number", "user_id", "userid", "id"],
        "Name": ["name", "customer_name", "customername", "full_name", "fullname", "customer name", "buyer_name", "buyer"],
        "Email": ["email", "email_address", "mail", "customer_email", "customer email address"],
        "Phone": ["phone", "mobile", "phone_number", "contact", "mobile_number", "contact_number"],
        "City": ["city", "location", "town", "customer_city", "shipping_city", "billing_city"],
        "Revenue": [
            "revenue", "gmv", "gross merchandise value", "gross_merchandise_value", "sales",
            "sales_amount", "total_sales", "total_revenue", "customer_value", "customer value",
            "value", "amount", "order_amount", "order value", "order_value", "total_amount",
            "grand_total", "net_sales", "net_amount", "transaction_amount", "purchase_amount",
            "selling_price", "sale_price", "price", "revenue_amount", "total_price",
        ],
        "Purchases": [
            "purchases", "orders", "order_count", "transactions", "purchase_count", "orders_count",
            "quantity", "qty", "units", "items", "number_of_orders", "total_orders",
        ],
        "Spend": [
            "spend", "marketing_spend", "ad_spend", "advertising_spend", "cost", "total_spend",
            "campaign_spend", "acquisition_spend", "marketing_cost",
        ],
        "Channel": ["channel", "source", "acquisition_channel", "marketing_channel", "sales_channel", "order_channel"],
        "Segment": ["segment", "customer_segment", "category", "tier", "customer_tier"],
    }

    # Map standard fields from raw variations.
    for target, names in aliases.items():
        src = first_existing(df, names)
        if src is not None and src != target:
            df[target] = df[src]
        elif target not in df.columns:
            if target in {"Name", "Email", "Phone", "City", "Channel", "Segment"}:
                df[target] = "Unknown"
            else:
                df[target] = 0.0

    # Revenue fallback: some commerce datasets use a generic numeric amount field.
    if "Revenue" in df.columns:
        revenue_source = choose_numeric_source(df.drop(columns=["Revenue"], errors="ignore"), aliases["Revenue"])
        revenue_now = clean_number(df["Revenue"])
        if revenue_source is not None and (revenue_now.eq(0).mean() > 0.98 or revenue_now.sum() == 0):
            df["Revenue"] = clean_number(df[revenue_source])
        else:
            df["Revenue"] = revenue_now

    # Purchases fallback: if there is no order count, one row is treated as one transaction.
    df["Purchases"] = clean_number(df["Purchases"])
    if df["Purchases"].eq(0).all():
        order_source = first_existing(df, ["order_id", "order number", "transaction_id", "invoice_id"])
        if order_source is not None:
            df["Purchases"] = 1.0

    df["Spend"] = clean_number(df["Spend"])
    df["Revenue"] = clean_number(df["Revenue"]).clip(lower=0)
    df["Purchases"] = df["Purchases"].clip(lower=0)
    df["Spend"] = df["Spend"].clip(lower=0)

    for c in ["Customer ID", "Name", "Email", "Phone", "City", "Channel"]:
        df[c] = df[c].fillna("Unknown").astype(str).replace({"nan": "Unknown", "None": "Unknown"})

    # Auto-generate a stable channel when none is supplied.
    channel_clean = df["Channel"].astype(str).str.strip()
    if channel_clean.eq("").all() or channel_clean.str.upper().eq("UNKNOWN").all():
        channels = np.array(["Organic", "Paid", "Referral", "Direct"])
        df["Channel"] = channels[np.arange(len(df)) % len(channels)]
    else:
        df["Channel"] = channel_clean.replace("", "Unknown")

    # Normalize/derive segments using revenue + purchase behavior.
    valid = {"HIGH VALUE", "LOYAL", "GROWTH", "STANDARD"}
    supplied_segment = df["Segment"].fillna("Unknown").astype(str).str.upper().str.strip()
    if supplied_segment.isin(valid).all() and not supplied_segment.eq("UNKNOWN").all():
        df["Segment"] = supplied_segment
    else:
        revenue = df["Revenue"]
        purchases = df["Purchases"]
        q75, q50, q25 = revenue.quantile([0.75, 0.50, 0.25]).tolist()
        p65 = purchases.quantile(0.65)
        if revenue.nunique(dropna=True) <= 1 and purchases.nunique(dropna=True) <= 1:
            df["Segment"] = "STANDARD"
        else:
            df["Segment"] = np.select(
                [
                    revenue >= q75,
                    (purchases >= p65) & (revenue >= q50),
                    revenue >= q25,
                ],
                ["HIGH VALUE", "LOYAL", "GROWTH"],
                default="STANDARD",
            )

    purchases_safe = df["Purchases"].replace(0, np.nan)
    revenue_safe = df["Revenue"].replace(0, np.nan)
    df["Avg Order Value"] = (df["Revenue"] / purchases_safe).replace([np.inf, -np.inf], np.nan).fillna(0)
    df["Spend Ratio"] = (df["Spend"] / revenue_safe).replace([np.inf, -np.inf], np.nan).fillna(0)
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


def money(v) -> str:
    try:
        value = float(v)
    except (TypeError, ValueError):
        value = 0.0
    return f"₹{value:,.0f}"


def metric(label, value, note=""):
    st.markdown(
        f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def get_logo_path():
    return next((p for p in LOGO_CANDIDATES if p.exists()), None)


def load_data():
    for key, default in [("file_signature", None), ("data", None), ("filename", None), ("file_size", 0)]:
        if key not in st.session_state:
            st.session_state[key] = default

    upload = st.sidebar.file_uploader(
        "Upload CSV, XLSX or XLS",
        type=["csv", "xlsx", "xls"],
        key="dataset_upload",
        help="Upload a customer/sales dataset. RevPilot automatically normalizes common column names.",
    )
    if upload is not None:
        data_bytes = upload.getvalue()
        signature = hashlib.sha256(data_bytes).hexdigest()
        if signature != st.session_state.file_signature:
            with st.spinner("Processing dataset…"):
                raw = parse_uploaded_file(data_bytes, upload.name)
                st.session_state.data = normalize(raw)
                st.session_state.file_signature = signature
                st.session_state.filename = upload.name
                st.session_state.file_size = len(data_bytes)
                st.session_state.generated_message = None
            st.sidebar.success(f"Loaded {len(st.session_state.data):,} rows")
        elif st.session_state.data is not None:
            st.sidebar.success("Dataset ready — cached")
    return st.session_state.data


def sidebar():
    logo = get_logo_path()
    if logo:
        st.sidebar.markdown('<div class="logo-wrap">', unsafe_allow_html=True)
        st.sidebar.image(str(logo), use_container_width=True)
        st.sidebar.markdown('</div>', unsafe_allow_html=True)
    else:
        st.sidebar.markdown('<div class="logo-wrap"><div style="font-size:64px">🚀</div></div>', unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div class="brand-card">
      <div class="brand-title">RevPilot AI</div>
      <div class="brand-sub">Revenue Intelligence OS</div>
      <div class="status">● Live Data Mode</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("### 🧭 WORKSPACE")
    page = st.sidebar.radio("Navigation", [
        "🏠 Executive Dashboard",
        "👥 Customer Intelligence",
        "🎯 AI Target Customers",
        "🔮 Campaign Prediction",
        "📈 Revenue Analytics",
        "💬 AI Outreach & Engagement",
        "⚙️ Data & Settings",
        "ℹ️ About",
    ], label_visibility="collapsed")

    st.sidebar.divider()
    st.sidebar.markdown("### 📁 UPLOAD DATASET")
    st.sidebar.caption("CSV, XLSX or XLS • 200MB per file")
    data = load_data()

    st.sidebar.divider()
    st.sidebar.markdown("### 👨‍💻 DEVELOPER")
    st.sidebar.markdown(
        f'<div class="linkbox">🔗 <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a><br><br>💻 <a href="{GITHUB_URL}" target="_blank">GitHub</a><br><br>🌐 <a href="{PORTFOLIO_URL}" target="_blank">Portfolio / Website</a></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.caption("Prajwal Y R | Razorpay Internship Portfolio Demo")
    return page, data


def landing():
    st.markdown("""
    <div class="hero">
      <div class="eyebrow">AI REVENUE INTELLIGENCE</div>
      <h1>RevPilot AI 🚀</h1>
      <p>Turn customer and sales data into actionable revenue intelligence using segmentation, priority scoring, campaign prediction, interactive analytics, and personalized outreach.</p>
      <span class="status">● Waiting for Dataset</span>
    </div>
    <div class="card" style="text-align:center;padding:70px 30px;">
      <div style="font-size:70px">📁</div>
      <h1>Upload your real dataset to begin</h1>
      <p class="small" style="font-size:17px">Upload a CSV, XLSX, or XLS file using the sidebar. RevPilot AI will normalize common headers and build the workspace automatically.</p>
    </div>
    """, unsafe_allow_html=True)


def chart_layout(fig):
    fig.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=55, b=10), autosize=True, height=430)
    return fig


def dashboard(df):
    st.markdown("<div class='section-title'>🏠 Executive Dashboard</div>", unsafe_allow_html=True)
    c = st.columns(4)
    with c[0]: metric("Total Customers", f"{len(df):,}", "Live dataset")
    with c[1]: metric("Customer Value", money(df["Customer Value"].sum()), "Total revenue")
    with c[2]: metric("Avg Value", money(df["Customer Value"].mean()), "Per customer")
    with c[3]: metric("High-Value Count", f"{(df['Segment']=='HIGH VALUE').sum():,}", "Top segment")

    left, right = st.columns(2)
    with left:
        seg = df.groupby("Segment", as_index=False)["Customer Value"].sum().sort_values("Customer Value", ascending=False)
        fig = px.bar(seg, x="Segment", y="Customer Value", title="Value by Segment", text_auto=".2s")
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with right:
        ch = df.groupby("Channel", as_index=False)["Spend"].sum()
        if ch["Spend"].sum() <= 0:
            ch = df["Channel"].value_counts().rename_axis("Channel").reset_index(name="Customers")
            fig = px.pie(ch, names="Channel", values="Customers", title="Customers by Channel", hole=.45)
        else:
            fig = px.pie(ch, names="Channel", values="Spend", title="Spend by Channel", hole=.45)
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown("### 🏆 Top 10 Revenue Customers")
    cols = ["Customer ID", "Name", "Segment", "Revenue", "Purchases", "Spend", "Channel"]
    st.dataframe(df.nlargest(10, "Revenue")[cols], use_container_width=True, hide_index=True)


def customer_intelligence(df):
    st.markdown("## 👥 Customer Intelligence")
    options = sorted(df["Segment"].dropna().unique().tolist())
    selected = st.multiselect("Filter segments", options, default=options)
    view = df[df["Segment"].isin(selected)] if selected else df.iloc[0:0]
    c = st.columns(4)
    with c[0]: metric("Customers", f"{len(view):,}")
    with c[1]: metric("Revenue", money(view["Revenue"].sum()))
    with c[2]: metric("Avg Order Value", money(view["Avg Order Value"].mean()))
    with c[3]: metric("Avg Customer Value", money(view["Customer Value"].mean()))
    st.dataframe(view, use_container_width=True, hide_index=True)


def pct_rank(s):
    if len(s) <= 1:
        return pd.Series(np.ones(len(s)), index=s.index)
    return s.rank(pct=True).fillna(0)


def target_customers(df):
    st.markdown("## 🎯 AI Target Customers")
    st.caption("Priority score = Value 45% + Purchases 25% + Spend Ratio 10% + Segment Bonus 20%.")
    d = df.copy()
    d["Value Score"] = pct_rank(d["Customer Value"]) * 45
    d["Purchase Score"] = pct_rank(d["Purchases"]) * 25
    # Lower spend ratio is generally more attractive for revenue growth.
    d["Spend Score"] = (1 - pct_rank(d["Spend Ratio"])) * 10
    bonus = d["Segment"].map({"HIGH VALUE": 20, "LOYAL": 16, "GROWTH": 12, "STANDARD": 6}).fillna(0)
    d["Priority Score"] = d["Value Score"] + d["Purchase Score"] + d["Spend Score"] + bonus
    max_top = max(5, min(100, len(d)))
    top_n = st.slider("Top customers", 5, max_top, min(20, max_top), 5)
    top = d.nlargest(top_n, "Priority Score").sort_values("Priority Score")
    fig = px.bar(top, x="Priority Score", y="Name", color="Segment", orientation="h", title="AI Priority Ranking", hover_data=["Revenue", "Purchases", "Spend Ratio"])
    st.plotly_chart(chart_layout(fig), use_container_width=True)
    st.dataframe(d.nlargest(top_n, "Priority Score")[["Customer ID", "Name", "Segment", "Revenue", "Purchases", "Spend Ratio", "Priority Score"]], use_container_width=True, hide_index=True)


def campaign_prediction(df):
    st.markdown("## 🔮 Campaign Prediction")
    a, b, c = st.columns(3)
    with a: quality = st.slider("Campaign quality adjustment", 50, 150, 100, 5) / 100
    with b: realization = st.slider("Revenue realization rate", 20, 100, 70, 5) / 100
    with c: cost_rate = st.slider("Variable cost rate", 1, 40, 12, 1) / 100
    base_response = float(np.clip(0.04 + min(0.12, df["Purchases"].mean() / 300), 0.02, 0.16))
    blended = float(np.clip(base_response * quality, 0.01, 0.35))
    audience = len(df)
    expected_orders = audience * blended
    avg_value = float(df["Avg Order Value"].mean()) if len(df) else 0
    expected_revenue = expected_orders * avg_value * realization
    campaign_cost = expected_revenue * cost_rate
    profit = expected_revenue - campaign_cost
    roi = (profit / campaign_cost * 100) if campaign_cost > 0 else 0
    cols = st.columns(4)
    for col, label, val in zip(cols, ["Blended Response", "Expected Revenue", "Campaign Cost", "ROI"], [f"{blended*100:.1f}%", money(expected_revenue), money(campaign_cost), f"{roi:.1f}%"]):
        with col: metric(label, val, "Model estimate")
    st.info("Forecasts are estimates for portfolio/demo decision support, not guaranteed outcomes.")


def revenue_analytics(df):
    st.markdown("## 📈 Revenue Analytics")
    numeric = ["Revenue", "Customer Value", "Purchases", "Spend", "Avg Order Value", "Spend Ratio"]
    metric_name = st.selectbox("Distribution metric", numeric)
    fig = px.histogram(df, x=metric_name, marginal="box", nbins=35, title=f"{metric_name} Distribution")
    st.plotly_chart(chart_layout(fig), use_container_width=True)
    size = df["Spend"].clip(lower=0)
    fig2 = px.scatter(df, x="Purchases", y="Customer Value", color="Segment", size=size if size.sum() > 0 else None, hover_name="Name", title="Purchases vs Customer Value")
    st.plotly_chart(chart_layout(fig2), use_container_width=True)


def make_message(row, objective, tone, channel):
    name = str(row.get("Name", "Customer"))
    segment = str(row.get("Segment", "STANDARD"))
    value = money(float(row.get("Customer Value", 0)))
    openings = {
        "Professional": "Hello {name},",
        "Friendly": "Hi {name}! 👋",
        "Urgent": "Hi {name}, quick opportunity for you:",
    }
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
        names = df["Name"].astype(str).str.lower()
        ids_ = df["Customer ID"].astype(str).str.lower()
        filtered = df[names.str.contains(q, na=False) | ids_.str.contains(q, na=False)]
    if filtered.empty:
        st.warning("No matching customer found.")
        return
    choices = filtered.index.tolist()
    selected_idx = st.selectbox("Target customer", choices, format_func=lambda i: f"{df.loc[i,'Name']} — {df.loc[i,'Customer ID']} — {df.loc[i,'Segment']}")
    row = df.loc[selected_idx]
    a, b, c = st.columns(3)
    with a: channel = st.selectbox("Outreach type", ["Email", "WhatsApp/SMS", "Both"])
    with b: objective = st.selectbox("Campaign objective", ["Win-back", "Upsell", "Exclusive Discount", "Loyalty Reward"])
    with c: tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent"])
    st.markdown(f"**Customer:** {row['Name']}  •  **Segment:** {row['Segment']}  •  **Value:** {money(float(row['Customer Value']))}")
    if st.button("🤖 Generate AI Message", type="primary", use_container_width=True):
        if channel == "Both":
            st.session_state.generated_message = "EMAIL\n\n" + make_message(row, objective, tone, "Email") + "\n\n---\n\nWHATSAPP/SMS\n\n" + make_message(row, objective, tone, "WhatsApp/SMS")
        else:
            st.session_state.generated_message = make_message(row, objective, tone, "Email" if channel == "Email" else "WhatsApp/SMS")
    if st.session_state.get("generated_message"):
        st.text_area("Ready-to-send message", st.session_state.generated_message, height=260)
        if st.button("🚀 Send Campaign via API", use_container_width=True):
            if "sent_log" not in st.session_state:
                st.session_state.sent_log = []
            st.session_state.sent_log.append({
                "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Customer": row["Name"],
                "Channel": channel,
                "Objective": objective,
                "Status": "✓ Simulated API Sent",
            })
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
    if st.session_state.get("filename"):
        size_mb = st.session_state.get("file_size", 0) / (1024 * 1024)
        st.caption(f"File: {st.session_state.filename} • {size_mb:.2f} MB")
    st.markdown("### 👀 Dynamic Sample Preview")
    max_rows = max(5, min(50, len(df)))
    rows = st.slider("Preview rows", 5, max_rows, min(10, max_rows))
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
        ("👥 Customer Intelligence", "Analyze revenue, purchases, spend, segments and customer-level signals."),
        ("🎯 AI Target Customers", "Rank customers using value, purchases, spend ratio and segment signals."),
        ("🔮 Campaign Prediction", "Estimate response, revenue realization, campaign cost and ROI."),
        ("📈 Revenue Analytics", "Explore distributions and relationships with interactive Plotly charts."),
        ("💬 AI Outreach", "Generate personalized Email, WhatsApp/SMS or combined messages."),
        ("🏠 Executive Dashboard", "Monitor customer count, value, segments, channels and top revenue customers."),
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
    st.markdown('<div class="card"><p class="small">CSV, XLSX and XLS datasets are normalized automatically. Common aliases such as customer_id, GMV, revenue, orders, spend, phone, email, city, amount, sales and order value are recognized. Missing analytical fields are safely derived.</p></div>', unsafe_allow_html=True)

    st.markdown("## 🔗 Developer")
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

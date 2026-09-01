import io
import hashlib
import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RevPilot AI — Revenue Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME / CSS
# ============================================================

st.markdown(
    """
    <style>
    :root {
        --bg-1: #060912;
        --bg-2: #080d18;
        --panel: rgba(15, 23, 42, 0.78);
        --panel-strong: rgba(17, 24, 39, 0.94);
        --border: rgba(139, 92, 246, 0.34);
        --border-soft: rgba(148, 163, 184, 0.15);
        --text: #f8fafc;
        --muted: #94a3b8;
        --purple: #a78bfa;
        --green: #6ee7b7;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(124, 58, 237, 0.16), transparent 28%),
            radial-gradient(circle at 90% 15%, rgba(59, 130, 246, 0.10), transparent 25%),
            linear-gradient(180deg, var(--bg-1), var(--bg-2));
        color: var(--text);
    }

    .block-container {
        max-width: 1500px;
        padding: 2rem 2.2rem 3.5rem;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #050812, #080d18);
        border-right: 1px solid rgba(139, 92, 246, 0.16);
    }

    [data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(17, 24, 39, .90), rgba(10, 15, 27, .90));
        border: 1px solid var(--border-soft);
        border-radius: 18px;
        padding: 1rem 1.15rem;
        min-height: 115px;
        box-shadow: 0 10px 35px rgba(0,0,0,.16);
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--text);
        font-weight: 800;
    }

    .hero {
        padding: 2.35rem 2.5rem;
        border-radius: 28px;
        border: 1px solid var(--border);
        background:
            linear-gradient(135deg, rgba(39, 20, 79, .86), rgba(10, 18, 34, .95));
        box-shadow: 0 20px 60px rgba(0,0,0,.20);
        margin-bottom: 1.5rem;
    }

    .hero-kicker {
        color: var(--purple);
        font-size: .78rem;
        font-weight: 850;
        letter-spacing: .18em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }

    .hero h1 {
        color: var(--text);
        font-size: clamp(2.2rem, 5vw, 4.25rem);
        line-height: 1;
        margin: 0 0 .9rem 0;
        letter-spacing: -.04em;
    }

    .hero p {
        color: #b8c3d4;
        max-width: 850px;
        line-height: 1.7;
        margin: 0;
    }

    .status-badge {
        display: inline-block;
        margin-top: 1.2rem;
        padding: .45rem .75rem;
        border-radius: 999px;
        color: var(--green);
        background: rgba(110, 231, 183, .07);
        border: 1px solid rgba(110, 231, 183, .25);
        font-size: .82rem;
        font-weight: 750;
        box-shadow: 0 0 24px rgba(110, 231, 183, .07);
    }

    .sidebar-card {
        padding: 1.2rem;
        border-radius: 22px;
        border: 1px solid var(--border);
        background: linear-gradient(145deg, rgba(124,58,237,.15), rgba(7,15,29,.88));
        margin-bottom: 1.2rem;
    }

    .sidebar-title {
        color: white;
        font-size: 1.35rem;
        font-weight: 850;
        margin: .25rem 0;
    }

    .sidebar-subtitle {
        color: #91a1b8;
        margin-bottom: .75rem;
    }

    .live {
        color: var(--green);
        font-weight: 750;
        font-size: .88rem;
    }

    .credit {
        color: #a9b7ca;
        font-size: .76rem;
        line-height: 1.65;
        margin-top: .9rem;
    }

    .section-title {
        color: white;
        font-size: 1.35rem;
        font-weight: 800;
        margin: 1.4rem 0 .8rem;
    }

    .feature-card {
        height: 100%;
        padding: 1.2rem;
        border-radius: 20px;
        border: 1px solid var(--border-soft);
        background: rgba(15, 23, 42, .65);
    }

    .feature-card h3 {
        color: white;
        margin-top: 0;
        font-size: 1.05rem;
    }

    .feature-card p {
        color: var(--muted);
        line-height: 1.55;
        font-size: .9rem;
    }

    .tech-badge {
        display: inline-block;
        padding: .45rem .7rem;
        margin: .25rem .25rem .25rem 0;
        border-radius: 999px;
        border: 1px solid rgba(167,139,250,.28);
        background: rgba(167,139,250,.08);
        color: #ddd6fe;
        font-weight: 700;
        font-size: .82rem;
    }

    .landing {
        text-align: center;
        padding: 3.5rem 1.5rem;
        border-radius: 28px;
        border: 1px dashed rgba(139,92,246,.38);
        background: rgba(15,23,42,.48);
    }

    .landing h2 {
        color: white;
        margin-bottom: .5rem;
    }

    .landing p {
        color: var(--muted);
        max-width: 680px;
        margin: auto;
        line-height: 1.65;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    @media (max-width: 800px) {
        .block-container {
            padding: 1rem;
        }
        .hero {
            padding: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

CURRENCY_COLUMNS = {
    "Customer Value",
    "Total Spend",
    "Avg Order Value",
}


def money(value):
    if pd.isna(value):
        return "₹0"
    return f"₹{value:,.0f}"


def safe_ratio(numerator, denominator):
    numerator = pd.to_numeric(numerator, errors="coerce").fillna(0)
    denominator = pd.to_numeric(denominator, errors="coerce").fillna(0)
    return np.divide(
        numerator,
        denominator,
        out=np.zeros(len(numerator), dtype=float),
        where=denominator.to_numpy() != 0,
    )


def hero(title, description, status="● Live Data Mode"):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">AI Revenue Intelligence</div>
            <h1>{title}</h1>
            <p>{description}</p>
            <div class="status-badge">{status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def page_title(title, subtitle=""):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)


# ============================================================
# DATA READER
# ============================================================

@st.cache_data(show_spinner=False, max_entries=3)
def read_uploaded_file(file_bytes, file_name):
    """Read a CSV/XLSX/XLS file once and cache it by content."""
    name = file_name.lower()

    if name.endswith(".csv"):
        return pd.read_csv(
            io.BytesIO(file_bytes),
            low_memory=False,
        )

    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(file_bytes))

    raise ValueError("Unsupported file format. Upload CSV, XLSX, or XLS.")


# ============================================================
# NORMALIZATION ENGINE
# ============================================================

@st.cache_data(show_spinner=False, max_entries=3)
def normalize(df):
    """Normalize common sales/customer schemas into RevPilot fields."""
    if df is None or df.empty:
        raise ValueError("The uploaded file contains no rows.")

    df = df.copy()

    # Normalize whitespace/casing before alias matching.
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "customer": "Customer",
        "customer id": "Customer",
        "customer_id": "Customer",
        "customerid": "Customer",
        "customer name": "Customer",
        "customer_name": "Customer",
        "name": "Customer",
        "user": "Customer",
        "user id": "Customer",
        "userid": "Customer",
        "id": "Customer",

        "customer value": "Customer Value",
        "customer_value": "Customer Value",
        "customervalue": "Customer Value",
        "value": "Customer Value",
        "revenue": "Customer Value",
        "sales": "Customer Value",
        "sale": "Customer Value",
        "amount": "Customer Value",
        "gmv": "Customer Value",
        "total value": "Customer Value",
        "total_value": "Customer Value",
        "order value": "Customer Value",
        "order_value": "Customer Value",
        "lifetime value": "Customer Value",
        "lifetime_value": "Customer Value",

        "segment": "Segment",
        "customer segment": "Segment",
        "customer_segment": "Segment",

        "purchases": "Purchases",
        "purchase": "Purchases",
        "purchase count": "Purchases",
        "purchase_count": "Purchases",
        "orders": "Purchases",
        "order count": "Purchases",
        "order_count": "Purchases",
        "transactions": "Purchases",
        "transaction count": "Purchases",
        "transaction_count": "Purchases",
        "quantity": "Purchases",
        "units": "Purchases",

        "total spend": "Total Spend",
        "total_spend": "Total Spend",
        "spend": "Total Spend",
        "total sales": "Total Spend",
        "total_sales": "Total Spend",
        "spent": "Total Spend",

        "channel": "Channel",
        "campaign channel": "Channel",
        "campaign_channel": "Channel",

        "email": "Email",
        "e-mail": "Email",
        "email address": "Email",
        "email_address": "Email",

        "phone": "Phone",
        "mobile": "Phone",
        "mobile number": "Phone",
        "mobile_number": "Phone",
        "phone number": "Phone",
        "phone_number": "Phone",

        "city": "City",
        "state": "State",
        "country": "Country",
    }

    rename_map = {}
    for column in df.columns:
        key = str(column).strip().lower()
        if key in aliases:
            rename_map[column] = aliases[key]

    df = df.rename(columns=rename_map)

    # If aliases created duplicate standardized columns, combine them.
    for standard in [
        "Customer",
        "Customer Value",
        "Purchases",
        "Total Spend",
        "Segment",
        "Channel",
        "Email",
        "Phone",
        "City",
        "State",
        "Country",
    ]:
        duplicate_positions = [
            i for i, col in enumerate(df.columns) if col == standard
        ]
        if len(duplicate_positions) > 1:
            combined = df.iloc[:, duplicate_positions].bfill(axis=1).iloc[:, 0]
            keep = [
                i for i, col in enumerate(df.columns)
                if col != standard or i == duplicate_positions[0]
            ]
            df = df.iloc[:, keep].copy()
            df[standard] = combined

    # Required customer identifier fallback.
    if "Customer" not in df.columns:
        df["Customer"] = [
            f"Customer {i:,}" for i in range(1, len(df) + 1)
        ]

    # Required value fallback.
    if "Customer Value" not in df.columns:
        # Try a numeric-looking business column before defaulting to zero.
        candidates = []
        for column in df.columns:
            if column in {"Customer", "Segment", "Channel", "Email", "Phone"}:
                continue
            converted = pd.to_numeric(df[column], errors="coerce")
            if converted.notna().sum() > 0:
                candidates.append((converted.notna().sum(), column))

        if candidates:
            candidates.sort(reverse=True)
            df["Customer Value"] = pd.to_numeric(
                df[candidates[0][1]], errors="coerce"
            )
        else:
            df["Customer Value"] = 0.0

    # Purchase fallback.
    if "Purchases" not in df.columns:
        df["Purchases"] = 1

    # Numeric cleanup.
    for column in ["Customer Value", "Purchases", "Total Spend"]:
        if column in df.columns:
            # Remove common currency/commas from strings.
            cleaned = (
                df[column]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("₹", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.strip()
            )
            df[column] = pd.to_numeric(cleaned, errors="coerce").fillna(0)

    # Total Spend fallback.
    if "Total Spend" not in df.columns:
        df["Total Spend"] = df["Customer Value"] * 0.50

    # Segment fallback using quartiles.
    if "Segment" not in df.columns:
        values = df["Customer Value"].fillna(0)

        if values.nunique() <= 1:
            df["Segment"] = "STANDARD"
        else:
            q1, q2, q3 = values.quantile([0.25, 0.50, 0.75]).values

            def make_segment(value):
                if value >= q3:
                    return "HIGH VALUE"
                if value >= q2:
                    return "LOYAL"
                if value >= q1:
                    return "GROWTH"
                return "STANDARD"

            df["Segment"] = values.apply(make_segment)

    # Channel fallback based on purchase frequency.
    if "Channel" not in df.columns:
        purchases = df["Purchases"].fillna(0)

        df["Channel"] = np.select(
            [
                purchases >= 8,
                purchases >= 4,
            ],
            [
                "Email + WhatsApp",
                "Email",
            ],
            default="WhatsApp",
        )

    # Text cleanup.
    df["Customer"] = df["Customer"].fillna("").astype(str)
    df["Segment"] = (
        df["Segment"]
        .fillna("STANDARD")
        .astype(str)
        .str.upper()
        .str.strip()
    )
    df["Channel"] = (
        df["Channel"]
        .fillna("Email")
        .astype(str)
        .str.strip()
    )

    for column in ["Email", "Phone", "City", "State", "Country"]:
        if column in df.columns:
            df[column] = df[column].fillna("").astype(str)

    # Derived metrics with zero-division protection.
    df["Avg Order Value"] = safe_ratio(
        df["Total Spend"],
        df["Purchases"],
    )

    df["Spend Ratio"] = safe_ratio(
        df["Total Spend"],
        df["Customer Value"],
    )

    df["Spend Ratio"] = (
        pd.Series(df["Spend Ratio"], index=df.index)
        .replace([np.inf, -np.inf], 0)
        .fillna(0)
        .clip(lower=0)
    )

    return df


# ============================================================
# SESSION STATE / UPLOAD
# ============================================================

if "dataset" not in st.session_state:
    st.session_state.dataset = None

if "file_name" not in st.session_state:
    st.session_state.file_name = None

if "file_size" not in st.session_state:
    st.session_state.file_size = None

if "file_hash" not in st.session_state:
    st.session_state.file_hash = None

if "upload_error" not in st.session_state:
    st.session_state.upload_error = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    # Resolve assets relative to app.py so the logo works on Render,
    # regardless of the process working directory.
    APP_DIR = Path(__file__).resolve().parent
    logo_path = APP_DIR / "revpilot_logo.png"
    icon_path = APP_DIR / "revpilot_icon.png"

    # Use Streamlit's native image renderer for local repository assets.
    # This is more reliable than putting a local file path inside HTML.
    if logo_path.is_file():
        st.image(str(logo_path), width=210)
    elif icon_path.is_file():
        st.image(str(icon_path), width=90)
    else:
        st.markdown('<div style="font-size:3rem;">🚀</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="sidebar-card">
            <div class="sidebar-title">RevPilot AI</div>
            <div class="sidebar-subtitle">Revenue Intelligence OS</div>
            <div class="live">● Live Data Mode</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🧭 WORKSPACE")
    page = st.radio(
        "WORKSPACE",
        [
            "🏠 Executive Dashboard",
            "👥 Customer Intelligence",
            "🎯 AI Target Customers",
            "🔮 Campaign Prediction",
            "📊 Revenue Analytics",
            "💬 AI Outreach & Engagement",
            "⚙️ Data & Settings",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### 📁 Upload Dataset")

    uploaded = st.file_uploader(
        "CSV, XLSX or XLS",
        type=["csv", "xlsx", "xls"],
        help="CSV is recommended for the fastest processing of large datasets.",
    )

    if uploaded is not None:
        file_bytes = uploaded.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        signature = (uploaded.name, len(file_bytes), file_hash)

        previous_signature = (
            st.session_state.file_name,
            st.session_state.file_size,
            st.session_state.file_hash,
        )

        if signature != previous_signature:
            try:
                with st.spinner(f"⚡ Processing {uploaded.name}..."):
                    raw_data = read_uploaded_file(file_bytes, uploaded.name)
                    clean_data = normalize(raw_data)

                st.session_state.dataset = clean_data
                st.session_state.file_name = uploaded.name
                st.session_state.file_size = len(file_bytes)
                st.session_state.file_hash = file_hash
                st.session_state.upload_error = None
                st.success(f"Loaded {len(clean_data):,} rows.")

            except Exception as exc:
                st.session_state.dataset = None
                st.session_state.upload_error = str(exc)
                st.error(f"Upload failed: {exc}")

    if st.session_state.dataset is not None:
        st.caption(
            f"Active: {st.session_state.file_name} · "
            f"{len(st.session_state.dataset):,} rows"
        )

    if st.button(
        "🗑️ Clear Dataset",
        use_container_width=True,
        disabled=st.session_state.dataset is None,
    ):
        st.session_state.dataset = None
        st.session_state.file_name = None
        st.session_state.file_size = None
        st.session_state.file_hash = None
        st.session_state.upload_error = None
        st.rerun()

    st.divider()
    st.markdown("### 🔗 Developer")
    st.markdown("🔗 [LinkedIn](https://www.linkedin.com/)")
    st.markdown("💻 [GitHub](https://github.com/prajwalyr849-sudo/revpilot-ai)")
    st.markdown("🌐 [Portfolio / Website](https://prajwalyr.dev)")
    st.caption("Prajwal Y R · Razorpay Internship Portfolio Demo")


# ============================================================
# LANDING STATE
# ============================================================

if st.session_state.dataset is None and page not in {
    "ℹ️ About & Creator",
}:
    hero(
        "RevPilot AI 🚀",
        "Turn customer and sales data into actionable revenue intelligence "
        "using segmentation, priority scoring, campaign prediction, and "
        "interactive analytics.",
        "● Waiting for Dataset",
    )

    st.markdown(
        """
        <div class="landing">
            <div style="font-size:3rem;">📁</div>
            <h2>Upload your real dataset to begin</h2>
            <p>
                RevPilot does not preload fake demo customers.
                Upload a CSV, XLSX, or XLS file using the sidebar.
                The dashboard will appear automatically after processing.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


customers = st.session_state.dataset


# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "🏠 Executive Dashboard":

    hero(
        "RevPilot AI 🚀",
        "A revenue intelligence workspace for discovering customer value, "
        "prioritizing opportunities, and forecasting campaign outcomes.",
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Total Customers",
        f"{len(customers):,}",
    )
    b.metric(
        "Total Value",
        money(customers["Customer Value"].sum()),
    )
    c.metric(
        "Avg Value",
        money(customers["Customer Value"].mean()),
    )
    d.metric(
        "High-Value Count",
        f"{(customers['Segment'] == 'HIGH VALUE').sum():,}",
    )

    st.markdown(
        '<div class="section-title">Revenue Overview</div>',
        unsafe_allow_html=True,
    )

    x, y = st.columns(2)

    with x:
        segment_data = (
            customers.groupby(
                "Segment",
                as_index=False,
                dropna=False,
            )["Customer Value"]
            .sum()
            .sort_values("Customer Value", ascending=False)
        )

        fig = px.bar(
            segment_data,
            x="Segment",
            y="Customer Value",
            title="Value by Segment",
            labels={
                "Customer Value": "Customer Value",
                "Segment": "Segment",
            },
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=420,
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    with y:
        channel_data = (
            customers.groupby(
                "Channel",
                as_index=False,
                dropna=False,
            )["Total Spend"]
            .sum()
        )

        fig = px.pie(
            channel_data,
            names="Channel",
            values="Total Spend",
            title="Spend by Channel",
            hole=.45,
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=60, b=20),
            height=420,
        )
        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    page_title("Top 10 Revenue Customers")

    top10 = (
        customers
        .sort_values("Customer Value", ascending=False)
        .head(10)
        .copy()
    )

    st.dataframe(
        top10,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# CUSTOMER INTELLIGENCE
# ============================================================

elif page == "👥 Customer Intelligence":

    hero(
        "Customer Intelligence",
        "Filter customer populations by segment and inspect the underlying "
        "records without loading unnecessary demo data.",
    )

    options = sorted(
        customers["Segment"].dropna().unique().tolist()
    )

    selected = st.multiselect(
        "Segment filter",
        options=options,
        default=options,
    )

    filtered = customers[
        customers["Segment"].isin(selected)
    ].copy()

    a, b, c = st.columns(3)

    a.metric(
        "Customers",
        f"{len(filtered):,}",
    )
    b.metric(
        "Total Value",
        money(filtered["Customer Value"].sum()),
    )
    c.metric(
        "Total Spend",
        money(filtered["Total Spend"].sum()),
    )

    page_title(
        "Paginated Customer View",
        "Use the controls below to browse the filtered raw dataset.",
    )

    page_size = st.selectbox(
        "Rows per page",
        [25, 50, 100, 250],
        index=2,
    )

    total_rows = len(filtered)
    total_pages = max(
        1,
        math.ceil(total_rows / page_size),
    )

    page_number = st.number_input(
        "Page",
        min_value=1,
        max_value=total_pages,
        value=1,
        step=1,
    )

    start = (page_number - 1) * page_size
    end = start + page_size

    st.caption(
        f"Page {page_number} of {total_pages} · "
        f"Showing rows {start + 1:,}–{min(end, total_rows):,} "
        f"of {total_rows:,}"
        if total_rows
        else "No customers match the selected segments."
    )

    st.dataframe(
        filtered.iloc[start:end],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# AI TARGET CUSTOMERS
# ============================================================

elif page == "🎯 AI Target Customers":

    hero(
        "AI Target Customers",
        "Rank customers using a transparent multi-variable opportunity "
        "score designed for revenue prioritization.",
    )

    w = customers.copy()

    max_value = max(
        float(w["Customer Value"].max()),
        1.0,
    )
    max_purchases = max(
        float(w["Purchases"].max()),
        1.0,
    )

    value_score = (
        w["Customer Value"] / max_value
    ).clip(0, 1)

    purchase_score = (
        w["Purchases"] / max_purchases
    ).clip(0, 1)

    spend_score = w["Spend Ratio"].clip(0, 1)

    segment_bonus = (
        w["Segment"]
        .map(
            {
                "HIGH VALUE": 1.00,
                "LOYAL": 0.85,
                "GROWTH": 0.65,
                "STANDARD": 0.40,
            }
        )
        .fillna(0.40)
    )

    # Required formula:
    # (Value * .45) + (Purchase * .25) + (Spend * .10) + (Segment * .20)
    w["Strategy Score"] = (
        value_score * 0.45
        + purchase_score * 0.25
        + spend_score * 0.10
        + segment_bonus * 0.20
    ) * 100

    max_targets = max(
        1,
        min(len(w), 100),
    )

    default_targets = min(
        10,
        max_targets,
    )

    target_count = st.slider(
        "Priority customers to show",
        min_value=1,
        max_value=max_targets,
        value=default_targets,
    )

    targets = (
        w
        .sort_values(
            "Strategy Score",
            ascending=False,
        )
        .head(target_count)
        .copy()
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Targets",
        f"{len(targets):,}",
    )
    b.metric(
        "Target Value",
        money(targets["Customer Value"].sum()),
    )
    c.metric(
        "Avg Value",
        money(targets["Customer Value"].mean()),
    )
    d.metric(
        "Avg Score",
        f"{targets['Strategy Score'].mean():.1f}",
    )

    display_columns = [
        "Customer",
        "Segment",
        "Customer Value",
        "Purchases",
        "Total Spend",
        "Channel",
        "Strategy Score",
    ]

    st.dataframe(
        targets[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    chart_data = targets.sort_values(
        "Strategy Score",
        ascending=True,
    )

    fig = px.bar(
        chart_data,
        x="Strategy Score",
        y="Customer",
        color="Segment",
        orientation="h",
        title="AI Customer Priority Ranking",
        labels={
            "Strategy Score": "Priority Score",
            "Customer": "Customer",
        },
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        height=max(420, target_count * 30),
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# CAMPAIGN PREDICTION
# ============================================================

elif page == "🔮 Campaign Prediction":

    hero(
        "Campaign Prediction",
        "Model campaign outcomes interactively using customer priority, "
        "campaign quality, revenue realization, and variable cost assumptions.",
    )

    w = customers.copy()

    w["Priority Score"] = (
        w["Customer Value"].rank(pct=True) * 0.65
        + w["Purchases"].rank(pct=True) * 0.35
    ) * 100

    max_targets = max(
        1,
        min(len(w), 100),
    )

    default_targets = min(
        10,
        max_targets,
    )

    n = st.slider(
        "Customers to forecast",
        min_value=1,
        max_value=max_targets,
        value=default_targets,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        boost = st.slider(
            "Campaign quality boost",
            min_value=0.0,
            max_value=1.0,
            value=0.20,
            step=0.05,
        )

    with c2:
        revenue_rate = st.slider(
            "Revenue realization rate",
            min_value=0.05,
            max_value=1.00,
            value=0.40,
            step=0.05,
        )

    with c3:
        cost_rate = st.slider(
            "Variable cost rate",
            min_value=0.00,
            max_value=0.20,
            value=0.03,
            step=0.01,
        )

    targets = (
        w
        .sort_values(
            "Priority Score",
            ascending=False,
        )
        .head(n)
        .copy()
    )

    base_response = (
        targets["Priority Score"] / 100 * 0.70
        + targets["Purchases"].rank(pct=True) * 0.20
        + (targets["Segment"] == "HIGH VALUE").astype(float) * 0.10
    )

    targets["Blended Response Rate"] = np.clip(
        (
            base_response * 100
            + boost * 25
        ) * 0.85
        + boost * 15,
        0,
        100,
    )

    targets["Expected Revenue"] = (
        targets["Customer Value"]
        * targets["Blended Response Rate"]
        / 100
        * revenue_rate
    )

    targets["Variable Cost"] = (
        targets["Expected Revenue"]
        * cost_rate
    )

    targets["Expected ROI"] = np.where(
        targets["Variable Cost"] > 0,
        (
            targets["Expected Revenue"]
            - targets["Variable Cost"]
        ) / targets["Variable Cost"],
        0,
    )

    a, b, c, d = st.columns(4)

    a.metric(
        "Expected Revenue",
        money(targets["Expected Revenue"].sum()),
    )
    b.metric(
        "Variable Cost",
        money(targets["Variable Cost"].sum()),
    )
    c.metric(
        "Avg Response",
        f"{targets['Blended Response Rate'].mean():.1f}%",
    )
    d.metric(
        "Avg ROI",
        f"{targets['Expected ROI'].mean():.1f}x",
    )

    st.dataframe(
        targets[
            [
                "Customer",
                "Segment",
                "Customer Value",
                "Blended Response Rate",
                "Expected Revenue",
                "Variable Cost",
                "Expected ROI",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# REVENUE ANALYTICS
# ============================================================

elif page == "📊 Revenue Analytics":

    hero(
        "Revenue Analytics",
        "Explore metric distributions and customer-level relationships "
        "through interactive Plotly Express visualizations.",
    )

    metric = st.selectbox(
        "Distribution metric",
        [
            "Customer Value",
            "Total Spend",
            "Purchases",
            "Avg Order Value",
            "Spend Ratio",
        ],
    )

    fig = px.histogram(
        customers,
        x=metric,
        color="Segment",
        marginal="box",
        title=f"{metric} Distribution",
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        height=470,
    )
    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    scatter = px.scatter(
        customers,
        x="Purchases",
        y="Customer Value",
        size="Total Spend",
        color="Segment",
        hover_name="Customer",
        title="Purchases vs Customer Value",
        labels={
            "Purchases": "Purchases",
            "Customer Value": "Customer Value",
        },
    )
    scatter.update_layout(
        margin=dict(l=20, r=20, t=60, b=20),
        height=520,
    )
    st.plotly_chart(
        scatter,
        use_container_width=True,
    )


# ============================================================
# ABOUT & CREATOR
# ============================================================

elif page == "ℹ️ About & Creator":

    hero(
        "About RevPilot AI",
        "RevPilot AI is a revenue intelligence application that transforms "
        "customer and sales data into practical prioritization and campaign insights.",
        "● Portfolio Project",
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>🎯 Project Mission</h3>
            <p>
                Help revenue and growth teams move from raw customer data
                to clear, explainable decisions: which customers matter most,
                where value is concentrated, and what a campaign could generate.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Key Features</div>',
        unsafe_allow_html=True,
    )

    features = [
        (
            "📈 Executive Dashboard",
            "High-level customer value, segment, channel, and top-customer visibility.",
        ),
        (
            "👥 Customer Intelligence",
            "Segment filtering and paginated access to the underlying customer records.",
        ),
        (
            "🎯 AI Targeting",
            "Explainable weighted scoring across value, purchases, spend, and segment.",
        ),
        (
            "🔮 Campaign Prediction",
            "Interactive response, revenue, variable-cost, and ROI scenario modeling.",
        ),
        (
            "📊 Revenue Analytics",
            "Distribution and relationship analysis using interactive Plotly charts.",
        ),
        (
            "⚡ Fast Data Layer",
            "Cached file parsing and content-signature state management for uploads.",
        ),
    ]

    cols = st.columns(3)

    for index, (title, description) in enumerate(features):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="feature-card">
                    <h3>{title}</h3>
                    <p>{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div class="section-title">Technology Stack</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Pandas</span>
        <span class="tech-badge">Plotly Express</span>
        <span class="tech-badge">NumPy</span>
        <span class="tech-badge">Python</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">Creator</div>',
        unsafe_allow_html=True,
    )

    st.write("**Prajwal Y R — Creator & Developer**")
    st.caption("Context: Razorpay Internship Portfolio Demo")

    b1, b2, b3 = st.columns(3)

    with b1:
        st.link_button(
            "🔗 LinkedIn",
            "https://www.linkedin.com/",
            use_container_width=True,
        )

    with b2:
        st.link_button(
            "💻 GitHub",
            "https://github.com/",
            use_container_width=True,
        )

    with b3:
        st.link_button(
            "🌐 Portfolio",
            "https://prajwalyr.dev",
            use_container_width=True,
        )


# ============================================================
# DATA & SETTINGS
# ============================================================

elif page == "⚙️ Data & Settings":

    hero(
        "Data & Settings",
        "Inspect the active dataset, upload metadata, and verify the "
        "normalized fields used by the RevPilot intelligence layer.",
    )

    if customers is not None:

        file_size_mb = (
            st.session_state.file_size / (1024 * 1024)
            if st.session_state.file_size
            else 0
        )

        a, b, c, d = st.columns(4)

        a.metric(
            "Active Rows",
            f"{len(customers):,}",
        )

        b.metric(
            "Columns",
            f"{len(customers.columns):,}",
        )

        c.metric(
            "File Size",
            f"{file_size_mb:.2f} MB",
        )

        d.metric(
            "Missing Cells",
            f"{int(customers.isna().sum().sum()):,}",
        )

        page_title("File Metadata")

        metadata = pd.DataFrame(
            {
                "Property": [
                    "File Name",
                    "Rows",
                    "Columns",
                    "File Size",
                    "Customer Field",
                    "Value Field",
                    "Purchase Field",
                    "Segment Field",
                    "Channel Field",
                ],
                "Value": [
                    st.session_state.file_name or "—",
                    f"{len(customers):,}",
                    f"{len(customers.columns):,}",
                    f"{file_size_mb:.2f} MB",
                    "Customer",
                    "Customer Value",
                    "Purchases",
                    "Segment",
                    "Channel",
                ],
            }
        )

        st.dataframe(
            metadata,
            use_container_width=True,
            hide_index=True,
        )

        page_title(
            "100-Row Preview",
            "Preview of the normalized active dataset.",
        )

        st.dataframe(
            customers.head(100),
            use_container_width=True,
            hide_index=True,
        )

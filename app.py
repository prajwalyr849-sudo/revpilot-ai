import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# RevPilot AI — Revenue Intelligence
# ============================================================

st.set_page_config(
    page_title="RevPilot AI — Revenue Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "assets"
LOGO = ASSET_DIR / "revpilot_logo.png"
ICON = ASSET_DIR / "revpilot_icon.png"

GITHUB_URL = "https://github.com/prajwaly849-sudo"
LINKEDIN_URL = "https://www.linkedin.com/in/prajwal-y-r-23b087247"
PORTFOLIO_URL = "https://revpilot-ai-1.onrender.com/"

DEVELOPER_NAME = "Prajwal Y R"
PROJECT_CONTEXT = "Razorpay Internship Portfolio Demo"


# --------------------------- THEME ---------------------------
st.markdown(
    """
<style>
:root {
    --bg: #060912;
    --panel: #0b1220;
    --panel2: #0f1728;
    --border: rgba(110, 130, 190, .22);
    --text: #edf4ff;
    --muted: #91a0ba;
    --cyan: #22d3ee;
    --blue: #5b8cff;
    --green: #35e0a1;
}

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 75% 0%, #101d3b 0%, var(--bg) 38%);
    color: var(--text);
}

[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080d19 0%, #060912 100%);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1rem; }

.block-container {
    max-width: 1500px;
    padding: 1.4rem 2rem 3rem;
}

.brand {
    padding: 12px 4px 18px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 18px;
}
.brand img {
    width: 190px;
    max-width: 100%;
    border-radius: 12px;
}
.brand-title {
    font-size: 1.25rem;
    font-weight: 800;
    margin-top: 8px;
}
.brand-subtitle {
    color: var(--muted);
    font-size: .82rem;
}

.section-label {
    color: #71809d;
    font-size: .68rem;
    font-weight: 800;
    letter-spacing: .14em;
    margin: 18px 0 8px;
}

.hero {
    background: linear-gradient(135deg, rgba(22, 31, 69, .95), rgba(8, 15, 31, .96));
    border: 1px solid rgba(83, 103, 210, .38);
    border-radius: 24px;
    padding: 22px 26px;
    box-shadow: 0 20px 60px rgba(0,0,0,.24);
}
.hero img {
    width: min(560px, 100%);
    border-radius: 14px;
}
.hero h1 { margin: 12px 0 4px; font-size: 2rem; }
.hero p { color: var(--muted); margin: 0; }

.card {
    background: linear-gradient(145deg, rgba(16,25,45,.95), rgba(8,14,27,.95));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 18px;
    height: 100%;
}
.card-title { color: var(--muted); font-size: .82rem; }
.card-value { font-size: 1.65rem; font-weight: 800; margin-top: 6px; }

.status {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(53,224,161,.1);
    color: var(--green);
    border: 1px solid rgba(53,224,161,.25);
    font-weight: 700;
    font-size: .78rem;
}

div[data-testid="stFileUploader"] {
    border-radius: 16px;
}
div[data-testid="stMetric"] {
    background: rgba(12,20,36,.75);
    border: 1px solid var(--border);
    padding: 14px;
    border-radius: 14px;
}
a { color: #65c7ff !important; }

@media (max-width: 800px) {
    .block-container { padding: 1rem .8rem 2rem; }
    .hero { padding: 18px; }
    .hero h1 { font-size: 1.55rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------- HELPERS ---------------------------
def money(value):
    value = float(value or 0)
    if abs(value) >= 1_000_000:
        return f"₹{value/1_000_000:.2f}M"
    if abs(value) >= 100_000:
        return f"₹{value/100_000:.2f}L"
    return f"₹{value:,.0f}"


def normalise_columns(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "Customer Value": ["Customer Value", "customer_value", "CustomerValue", "Revenue", "revenue"],
        "Segment": ["Segment", "segment", "Customer Segment", "customer_segment"],
        "Customer": ["Customer", "customer", "Customer Name", "customer_name", "Name", "name"],
        "Region": ["Region", "region", "Location", "location"],
        "Campaign": ["Campaign", "campaign", "Campaign Name", "campaign_name"],
    }

    for target, options in aliases.items():
        if target not in df.columns:
            for col in options:
                if col in df.columns:
                    df[target] = df[col]
                    break

    if "Customer Value" not in df.columns:
        numeric = df.select_dtypes(include="number").columns.tolist()
        if numeric:
            df["Customer Value"] = pd.to_numeric(df[numeric[0]], errors="coerce")
        else:
            df["Customer Value"] = 0

    df["Customer Value"] = pd.to_numeric(
        df["Customer Value"], errors="coerce"
    ).fillna(0)

    if "Segment" not in df.columns:
        df["Segment"] = "UNCLASSIFIED"

    if "Customer" not in df.columns:
        df["Customer"] = [f"Customer {i+1}" for i in range(len(df))]

    if "Region" not in df.columns:
        df["Region"] = "Unknown"

    return df


def load_file(uploaded):
    if uploaded.name.lower().endswith(".csv"):
        return pd.read_csv(uploaded, low_memory=False)
    return pd.read_excel(uploaded)


def save_dataset(df):
    st.session_state.dataset = normalise_columns(df)
    st.session_state.filename = st.session_state.get("filename", "Uploaded dataset")


def nav_button(label, page):
    if st.sidebar.button(label, use_container_width=True, key=f"nav_{page}"):
        st.session_state.page = page


# --------------------------- STATE ---------------------------
if "page" not in st.session_state:
    st.session_state.page = "Executive Dashboard"
if "dataset" not in st.session_state:
    st.session_state.dataset = None
if "filename" not in st.session_state:
    st.session_state.filename = ""


# --------------------------- SIDEBAR ---------------------------
with st.sidebar:
    st.markdown('<div class="brand">', unsafe_allow_html=True)
    if ICON.exists():
        st.image(str(ICON), width=64)
    st.markdown('<div class="brand-title">RevPilot AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="brand-subtitle">Revenue Intelligence OS</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">WORKSPACE</div>', unsafe_allow_html=True)
    nav_button("🏠  Executive Dashboard", "Executive Dashboard")
    nav_button("👥  Customer Intelligence", "Customer Intelligence")
    nav_button("🎯  AI Target Customers", "AI Target Customers")
    nav_button("🔮  Campaign Prediction", "Campaign Prediction")
    nav_button("📊  Revenue Analytics", "Revenue Analytics")

    st.markdown('<div class="section-label">DATA</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload CSV, XLSX or XLS",
        type=["csv", "xlsx", "xls"],
        label_visibility="visible",
    )

    if uploaded is not None:
        try:
            df_uploaded = load_file(uploaded)
            st.session_state.dataset = normalise_columns(df_uploaded)
            st.session_state.filename = uploaded.name
            st.success(f"Loaded {len(st.session_state.dataset):,} rows.")
        except Exception as exc:
            st.error(f"Could not read file: {exc}")

    if st.session_state.dataset is not None:
        if st.sidebar.button("🗑️ Clear Dataset", use_container_width=True):
            st.session_state.dataset = None
            st.session_state.filename = ""
            st.rerun()

    st.markdown('<div class="section-label">DEVELOPER</div>', unsafe_allow_html=True)
    st.markdown(
        f'<a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a>  ·  '
        f'<a href="{GITHUB_URL}" target="_blank">GitHub</a>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-label">ABOUT</div>', unsafe_allow_html=True)
    nav_button("ℹ️  About & Creator", "About & Creator")
    nav_button("⚙️  Data & Settings", "Data & Settings")


# --------------------------- DATA GATE ---------------------------
customers = st.session_state.dataset

if customers is None:
    st.markdown(
        '<div class="hero">'
        '<span class="status">● Live Data Mode</span>'
        '<h1>RevPilot AI 🚀</h1>'
        '<p>Revenue intelligence workspace for discovering customer value, '
        'prioritising opportunities, and forecasting growth.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.info("Upload your CSV, XLSX or XLS dataset from the sidebar to begin.")
    with c2:
        st.markdown(
            '<div class="card"><div class="card-title">CREATOR</div>'
            '<div class="card-value">Prajwal Y R</div>'
            '<div class="card-title">Razorpay Internship Portfolio Demo</div></div>',
            unsafe_allow_html=True,
        )
    st.stop()


# --------------------------- EXECUTIVE DASHBOARD ---------------------------
if st.session_state.page == "Executive Dashboard":
    st.markdown(
        '<div class="hero"><span class="status">● Live Data Mode</span>'
        '<h1>Executive Dashboard</h1>'
        '<p>One-screen view of customer value, segments and revenue opportunities.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    total = len(customers)
    total_value = customers["Customer Value"].sum()
    avg_value = customers["Customer Value"].mean()
    high_value = int((customers["Customer Value"] >= customers["Customer Value"].quantile(.75)).sum())

    a, b, c, d = st.columns(4)
    a.metric("Total Customers", f"{total:,}")
    b.metric("Total Value", money(total_value))
    c.metric("Average Value", money(avg_value))
    d.metric("High-Value Customers", f"{high_value:,}")

    left, right = st.columns(2)
    with left:
        seg = customers["Segment"].value_counts().reset_index()
        seg.columns = ["Segment", "Customers"]
        fig = px.bar(seg, x="Segment", y="Customers", title="Customer Segments")
        fig.update_layout(template="plotly_dark", height=360)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        top = customers.nlargest(10, "Customer Value")[["Customer", "Customer Value"]]
        fig = px.bar(
            top.sort_values("Customer Value"),
            x="Customer Value",
            y="Customer",
            orientation="h",
            title="Top 10 Customer Opportunities",
        )
        fig.update_layout(template="plotly_dark", height=360)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Customer Snapshot")
    st.dataframe(
        customers.sort_values("Customer Value", ascending=False).head(25),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------- CUSTOMER INTELLIGENCE ---------------------------
elif st.session_state.page == "Customer Intelligence":
    st.title("👥 Customer Intelligence")
    min_value = st.slider(
        "Minimum customer value",
        0.0,
        float(max(customers["Customer Value"].max(), 1)),
        float(customers["Customer Value"].median()),
    )
    view = customers[customers["Customer Value"] >= min_value].copy()
    st.write(f"Showing **{len(view):,}** customers.")
    st.dataframe(
        view.sort_values("Customer Value", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------- AI TARGET CUSTOMERS ---------------------------
elif st.session_state.page == "AI Target Customers":
    st.title("🎯 AI Target Customers")
    st.caption("Rule-based prioritisation using customer value and segment signals.")

    q75 = customers["Customer Value"].quantile(.75)
    targets = customers[customers["Customer Value"] >= q75].copy()
    targets["Priority Score"] = (
        targets["Customer Value"].rank(pct=True) * 70
        + targets["Customer Value"].apply(lambda x: 30 if x >= q75 else 0)
    ).round(1)

    st.metric("Recommended Targets", f"{len(targets):,}")
    st.dataframe(
        targets.sort_values("Priority Score", ascending=False).head(100),
        use_container_width=True,
        hide_index=True,
    )


# --------------------------- CAMPAIGN PREDICTION ---------------------------
elif st.session_state.page == "Campaign Prediction":
    st.title("🔮 Campaign Prediction")
    st.caption("Simple opportunity forecast based on customer value distribution.")

    q25 = customers["Customer Value"].quantile(.25)
    q50 = customers["Customer Value"].quantile(.50)
    q75 = customers["Customer Value"].quantile(.75)

    c1, c2, c3 = st.columns(3)
    c1.metric("Low Value", money(q25))
    c2.metric("Median Value", money(q50))
    c3.metric("High Value", money(q75))

    buckets = pd.cut(
        customers["Customer Value"],
        bins=[-float("inf"), q25, q50, q75, float("inf")],
        labels=["Low", "Emerging", "Growth", "High"],
    ).value_counts().reset_index()
    buckets.columns = ["Opportunity", "Customers"]

    fig = px.bar(buckets, x="Opportunity", y="Customers", title="Campaign Opportunity Pool")
    fig.update_layout(template="plotly_dark", height=420)
    st.plotly_chart(fig, use_container_width=True)


# --------------------------- REVENUE ANALYTICS ---------------------------
elif st.session_state.page == "Revenue Analytics":
    st.title("📊 Revenue Analytics")

    region = customers.groupby("Region", dropna=False)["Customer Value"].sum().reset_index()
    region = region.sort_values("Customer Value", ascending=False)

    fig = px.bar(
        region.head(15),
        x="Region",
        y="Customer Value",
        title="Revenue Value by Region",
    )
    fig.update_layout(template="plotly_dark", height=430)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Value Distribution")
    fig = px.histogram(
        customers,
        x="Customer Value",
        nbins=40,
        title="Customer Value Distribution",
    )
    fig.update_layout(template="plotly_dark", height=400)
    st.plotly_chart(fig, use_container_width=True)


# --------------------------- ABOUT ---------------------------
elif st.session_state.page == "About & Creator":
    st.title("ℹ️ About & Creator")
    if LOGO.exists():
        st.image(str(LOGO), use_container_width=True)
    st.markdown(
        f"""
**RevPilot AI** is a revenue intelligence portfolio application.

**Creator & Developer:** {DEVELOPER_NAME}  
**Context:** {PROJECT_CONTEXT}

- LinkedIn: {LINKEDIN_URL}
- GitHub: {GITHUB_URL}
- Live App: {PORTFOLIO_URL}
"""
    )


# --------------------------- SETTINGS ---------------------------
elif st.session_state.page == "Data & Settings":
    st.title("⚙️ Data & Settings")
    st.write(f"**Active file:** {st.session_state.filename or 'None'}")
    st.write(f"**Rows:** {len(customers):,}")
    st.write(f"**Columns:** {len(customers.columns):,}")

    if st.button("📥 Download Processed CSV"):
        csv = customers.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="revpilot_processed.csv",
            mime="text/csv",
        )

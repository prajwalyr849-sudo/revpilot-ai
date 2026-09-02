import io
import json
import re
import hashlib
import time
import platform
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

try:
    import psutil
except ImportError:
    psutil = None


# ============================================================
# RevPilot AI — Revenue Intelligence
# Enterprise Streamlit / Razorpay Blade-inspired architecture
# ============================================================

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
LINKEDIN_URL = "https://www.linkedin.com/in/prajwal-y-r-23b087247"
PORTFOLIO_URL = "https://prajwalyr.dev"

DEVELOPER_NAME = "Prajwal Y R"
PROJECT_CONTEXT = "Razorpay Internship Portfolio Demo"

BLADE_BG = "#0B132B"
BLADE_PRUSSIAN = "#012652"
BLADE_SURFACE = "#1C2541"
BLADE_BLUE = "#0D94FB"


# --------------------------- SESSION STATE ---------------------------

def init_state():
    defaults = {
        "file_signature": None,
        "data": None,
        "filename": None,
        "generated_message": "",
        "generated_payload": "",
        "sent_log": [],
        "audit_log": [],
        "idempotency_keys": set(),
        "notes": "",
        "meddpicc": {},
        "selected_customer_id": None,
        "optimistic_campaign": False,
        "campaign_error": None,
        "command_result": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


# --------------------------- CSS ---------------------------

def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        :root {
            --bg: #0B132B;
            --bg2: #012652;
            --surface: #1C2541;
            --surface2: #16203A;
            --blue: #0D94FB;
            --blue2: #46B4FF;
            --text: #F4F7FB;
            --muted: #A7B1C4;
            --border: rgba(255,255,255,0.08);
            --green: #6EE7B7;
            --amber: #FBBF24;
            --red: #FB7185;
        }

        html, body, [class*="css"] {
            font-family: Inter, Roboto, sans-serif;
        }

        .stApp {
            background: var(--bg);
            color: var(--text);
        }

        [data-testid="stHeader"] {
            background: rgba(11,19,43,0.96);
        }

        [data-testid="stSidebar"] {
            background: #081126;
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] > div:first-child {
            padding-top: 0.7rem;
        }

        .blade-card,
        .metric-card,
        .hero,
        .table-shell,
        .audit-shell {
            border: 1px solid var(--border);
            border-radius: 4px !important;
            background: var(--surface);
            box-shadow: none !important;
        }

        .blade-card {
            padding: 16px;
            margin-bottom: 12px;
        }

        .hero {
            padding: 24px;
            margin-bottom: 14px;
            background: linear-gradient(135deg, #012652 0%, #0B132B 72%);
        }

        .hero h1 {
            margin: 5px 0 6px;
            font-size: clamp(28px, 4vw, 42px);
            letter-spacing: -1.2px;
        }

        .hero p {
            color: var(--muted);
            max-width: 900px;
            line-height: 1.65;
            margin: 0;
        }

        .eyebrow {
            color: var(--blue2);
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 1.8px;
            font-family: "JetBrains Mono", monospace;
        }

        .metric-card {
            padding: 14px;
            min-height: 92px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 11px;
            font-weight: 700;
            letter-spacing: .8px;
            text-transform: uppercase;
        }

        .metric-value,
        .mono,
        .money,
        .timestamp,
        .latency,
        .hash,
        .priority {
            font-family: "JetBrains Mono", monospace !important;
            font-variant-numeric: tabular-nums;
        }

        .metric-value {
            font-size: 24px;
            font-weight: 700;
            margin-top: 6px;
        }

        .metric-note {
            color: #91A0B8;
            font-size: 11px;
            margin-top: 3px;
        }

        .section-title {
            font-size: 21px;
            font-weight: 800;
            margin: 17px 0 10px;
        }

        .small {
            color: var(--muted);
            font-size: 13px;
            line-height: 1.6;
        }

        .status-ok,
        .status-warn,
        .status-danger,
        .status-info {
            display: inline-block;
            border-radius: 4px;
            padding: 4px 7px;
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            font-weight: 700;
            margin: 2px 3px 2px 0;
            border: 1px solid transparent;
        }

        .status-ok {
            color: var(--green);
            border-color: rgba(110,231,183,.28);
            background: rgba(110,231,183,.08);
        }

        .status-warn {
            color: var(--amber);
            border-color: rgba(251,191,36,.28);
            background: rgba(251,191,36,.08);
        }

        .status-danger {
            color: var(--red);
            border-color: rgba(251,113,133,.28);
            background: rgba(251,113,133,.08);
        }

        .status-info {
            color: var(--blue2);
            border-color: rgba(13,148,251,.28);
            background: rgba(13,148,251,.08);
        }

        .brand {
            padding: 11px;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--bg2);
            margin-bottom: 10px;
        }

        .brand-title {
            font-size: 20px;
            font-weight: 800;
        }

        .brand-sub {
            color: #B9C5D8;
            font-size: 12px;
            margin-top: 2px;
        }

        .live {
            color: var(--green);
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            margin-top: 8px;
        }

        .audit-row {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 10px;
            padding: 7px 0;
            border-bottom: 1px solid var(--border);
            font-size: 10px;
        }

        .audit-row:last-child {
            border-bottom: 0;
        }

        .audit-key {
            color: #8795AD;
            font-family: "JetBrains Mono", monospace;
        }

        .audit-value {
            color: #DDE6F4;
            font-family: "JetBrains Mono", monospace;
            text-align: right;
        }

        .table-shell {
            padding: 4px;
        }

        .signal-box {
            border-left: 3px solid var(--blue);
            border-radius: 4px;
            background: rgba(13,148,251,.07);
            padding: 10px 12px;
            margin: 7px 0;
        }

        .command-hint {
            color: #91A0B8;
            font-family: "JetBrains Mono", monospace;
            font-size: 10px;
            text-align: center;
            margin-top: 8px;
        }

        /* Strict geometry for Streamlit controls */
        .stButton > button,
        .stDownloadButton > button,
        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] > div,
        textarea,
        input,
        .stTextInput input,
        .stNumberInput input {
            border-radius: 4px !important;
        }

        .stButton > button {
            min-height: 36px;
            font-weight: 700;
            border: 1px solid var(--border);
            box-shadow: none !important;
        }

        .stButton > button[kind="primary"] {
            background: var(--blue);
            border-color: var(--blue);
            color: white;
        }

        .stButton > button:hover {
            border-color: var(--blue);
        }

        div[data-testid="stMetric"] {
            border-radius: 4px !important;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border);
            border-radius: 4px !important;
        }

        .stAlert {
            border-radius: 4px !important;
        }

        @media (max-width: 800px) {
            .hero {
                padding: 18px;
            }
            .metric-value {
                font-size: 20px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# --------------------------- OBSERVABILITY ---------------------------

def memory_mb():
    if psutil is not None:
        try:
            return psutil.Process().memory_info().rss / (1024 * 1024)
        except Exception:
            pass
    return 0.0


def dataframe_mb(df):
    if df is None:
        return 0.0
    try:
        return float(df.memory_usage(deep=True).sum() / (1024 * 1024))
    except Exception:
        return 0.0


def audit(event, latency_ms=0.0, status=200, payload_size=0, tokens=0, detail=""):
    row = {
        "Time": datetime.now().strftime("%H:%M:%S.%f")[:-3],
        "Event": str(event),
        "Latency": f"{latency_ms:.1f} ms",
        "HTTP": int(status),
        "Payload": f"{payload_size:,} B",
        "Tokens": int(tokens),
        "Detail": str(detail)[:120],
    }
    st.session_state.audit_log.append(row)
    st.session_state.audit_log = st.session_state.audit_log[-80:]


def current_request_signature():
    headers = {}
    try:
        headers = dict(st.context.headers)
    except Exception:
        headers = {}
    raw = headers.get("X-Idempotency-Key") or headers.get("x-idempotency-key")
    return raw


def validate_idempotency_key(key=None):
    supplied = key or current_request_signature()
    if supplied is None:
        supplied = f"streamlit-{st.session_state.get('file_signature') or 'no-file'}-{datetime.now().strftime('%Y%m%d%H%M')}"
    supplied = str(supplied).strip()
    valid = bool(re.fullmatch(r"[A-Za-z0-9._:-]{8,128}", supplied))
    if not valid:
        audit("idempotency.reject", status=400, detail="Invalid X-Idempotency-Key")
        raise ValueError("Invalid X-Idempotency-Key. Use 8–128 safe characters.")
    return supplied


# --------------------------- DATA PIPELINE ---------------------------

@st.cache_data(show_spinner=False, max_entries=8)
def parse_uploaded_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    started = time.perf_counter()
    bio = io.BytesIO(file_bytes)
    lower = filename.lower()

    if lower.endswith(".csv"):
        try:
            return pd.read_csv(bio, low_memory=False)
        except UnicodeDecodeError:
            bio.seek(0)
            return pd.read_csv(bio, encoding="latin1", low_memory=False)

    if lower.endswith(".xlsx"):
        return pd.read_excel(bio, engine="openpyxl")

    if lower.endswith(".xls"):
        return pd.read_excel(bio, engine="xlrd")

    raise ValueError("Unsupported file type. Upload CSV, XLSX or XLS.")


def clean_number(series, default=0.0):
    if series is None:
        return pd.Series(dtype="float64")
    s = series.astype(str).str.strip()
    s = s.str.replace(",", "", regex=False)
    s = s.str.replace(r"[₹$€£%]", "", regex=True)
    s = s.str.replace(r"[^0-9.\-]", "", regex=True)
    return pd.to_numeric(s, errors="coerce").fillna(default)


def normalized_key(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def first_existing(df, aliases):
    mapping = {normalized_key(c): c for c in df.columns}
    aliases_norm = [normalized_key(a) for a in aliases]

    for alias in aliases_norm:
        if alias in mapping:
            return mapping[alias]

    for col in df.columns:
        key = normalized_key(col)
        if any(alias in key for alias in aliases_norm):
            return col

    return None


def _text_series(df, target, aliases, default="Unknown"):
    src = first_existing(df, aliases)
    if src is not None:
        return df[src].fillna(default).astype(str).replace({"nan": default, "None": default})
    return pd.Series(default, index=df.index, dtype="object")


def _number_series(df, aliases):
    src = first_existing(df, aliases)
    if src is None:
        return pd.Series(0.0, index=df.index, dtype="float64")
    return clean_number(df[src])


@st.cache_data(show_spinner=False, max_entries=8)
def normalize(raw: pd.DataFrame) -> pd.DataFrame:
    if raw is None:
        return pd.DataFrame()

    df = raw.copy()
    df.columns = [str(c).strip() for c in df.columns]

    aliases = {
        "Customer ID": ["customer_id", "customerid", "cust_id", "client_id", "user_id", "userid", "account_id", "customer"],
        "Name": ["name", "customer_name", "customername", "full_name", "fullname", "user_name", "client_name"],
        "Email": ["email", "email_address", "mail", "emailid"],
        "Phone": ["phone", "mobile", "phone_number", "mobile_number", "contact_number"],
        "City": ["city", "location", "town", "billing_city", "shipping_city"],
        "Revenue": [
            "revenue", "gmv", "sales", "total_revenue", "customer_value", "customer_value_total",
            "value", "amount", "total_amount", "purchase_amount", "order_value", "net_sales",
            "net_revenue", "transaction_amount", "transaction_value", "income"
        ],
        "Purchases": [
            "purchases", "purchase", "orders", "order_count", "transactions",
            "transaction_count", "purchase_count", "quantity", "qty", "frequency"
        ],
        "Spend": [
            "spend", "marketing_spend", "ad_spend", "cost", "total_spend",
            "campaign_spend", "acquisition_cost"
        ],
        "Channel": [
            "channel", "source", "acquisition_channel", "marketing_channel",
            "sales_channel", "medium"
        ],
        "Segment": ["segment", "customer_segment", "category", "tier", "customer_tier", "classification"],
    }

    # Canonical fields
    df["Customer ID"] = _text_series(df, "Customer ID", aliases["Customer ID"])
    df["Name"] = _text_series(df, "Name", aliases["Name"])
    df["Email"] = _text_series(df, "Email", aliases["Email"])
    df["Phone"] = _text_series(df, "Phone", aliases["Phone"])
    df["City"] = _text_series(df, "City", aliases["City"])
    df["Channel"] = _text_series(df, "Channel", aliases["Channel"])
    df["Segment"] = _text_series(df, "Segment", aliases["Segment"])

    df["Revenue"] = _number_series(df, aliases["Revenue"])
    df["Purchases"] = _number_series(df, aliases["Purchases"])
    df["Spend"] = _number_series(df, aliases["Spend"])

    # Revenue fallback: Unit Price * Quantity
    if float(df["Revenue"].sum()) == 0:
        unit_src = first_existing(df, ["unit_price", "price", "selling_price", "item_price", "rate"])
        qty_src = first_existing(df, ["quantity", "qty", "units"])
        if unit_src is not None and qty_src is not None:
            df["Revenue"] = clean_number(df[unit_src]) * clean_number(df[qty_src])

    # Purchase fallback: each row is a transaction when no explicit count exists
    if float(df["Purchases"].sum()) == 0 and len(df):
        df["Purchases"] = 1.0

    # Clean numeric bounds
    for col in ["Revenue", "Purchases", "Spend"]:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(0).clip(lower=0)

    # If this is clearly transaction-level data, aggregate customer metrics while
    # preserving representative contact/channel fields.
    customer_id_count = df["Customer ID"].nunique(dropna=True)
    if len(df) > 0 and customer_id_count < len(df) * 0.85 and customer_id_count > 1:
        agg = (
            df.groupby("Customer ID", dropna=False, sort=False)
            .agg(
                Name=("Name", "first"),
                Email=("Email", "first"),
                Phone=("Phone", "first"),
                City=("City", "first"),
                Revenue=("Revenue", "sum"),
                Purchases=("Purchases", "sum"),
                Spend=("Spend", "sum"),
                Channel=("Channel", "first"),
                Segment=("Segment", "first"),
            )
            .reset_index()
        )
        df = agg

    # Channel fallback based on purchase frequency.
    if df["Channel"].replace("Unknown", np.nan).isna().all() or df["Channel"].eq("Unknown").all():
        p = df["Purchases"]
        q75 = p.quantile(.75)
        q50 = p.quantile(.50)
        df["Channel"] = np.select(
            [p >= q75, p >= q50],
            ["Organic", "Referral"],
            default="Direct",
        )

    # Segment fallback using revenue quartiles and purchase frequency.
    valid = {"HIGH VALUE", "LOYAL", "GROWTH", "STANDARD"}
    segment = df["Segment"].astype(str).str.upper().str.strip()
    if not segment.isin(valid).all() or segment.eq("UNKNOWN").all():
        q75, q50, q25 = df["Revenue"].quantile([.75, .50, .25]).tolist()
        purchase_q65 = df["Purchases"].quantile(.65)
        df["Segment"] = np.select(
            [
                df["Revenue"] >= q75,
                (df["Purchases"] >= purchase_q65) & (df["Revenue"] >= q50),
                df["Revenue"] >= q25,
            ],
            ["HIGH VALUE", "LOYAL", "GROWTH"],
            default="STANDARD",
        )
    else:
        df["Segment"] = segment

    revenue_safe = df["Revenue"].replace(0, np.nan)
    purchase_safe = df["Purchases"].replace(0, np.nan)

    df["Customer Value"] = df["Revenue"]
    df["Avg Order Value"] = (df["Revenue"] / purchase_safe).replace([np.inf, -np.inf], np.nan).fillna(0)
    df["Spend Ratio"] = (df["Spend"] / revenue_safe).replace([np.inf, -np.inf], np.nan).fillna(0)

    # Deterministic data types and ordering.
    df["Customer ID"] = df["Customer ID"].astype(str).replace({"nan": "Unknown"})
    df["Name"] = df["Name"].astype(str).replace({"nan": "Unknown"})
    for col in ["Email", "Phone", "City", "Channel"]:
        df[col] = df[col].fillna("Unknown").astype(str)

    return df.reset_index(drop=True)


@st.cache_data(show_spinner=False)
def demo_data() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 160
    revenue = np.round(rng.lognormal(8.2, 0.9, n), 2)
    purchases = rng.integers(1, 28, n)
    spend = np.round(revenue * rng.uniform(.02, .18, n), 2)
    raw = pd.DataFrame(
        {
            "Customer ID": [f"CUST-{i:04d}" for i in range(1, n + 1)],
            "Name": [f"Customer {i}" for i in range(1, n + 1)],
            "Email": [f"customer{i}@example.com" for i in range(1, n + 1)],
            "Phone": [f"+91 90000 {i:05d}" for i in range(1, n + 1)],
            "City": rng.choice(["Bengaluru", "Mumbai", "Delhi", "Hyderabad", "Chennai"], n),
            "Revenue": revenue,
            "Purchases": purchases,
            "Spend": spend,
            "Channel": rng.choice(["Organic", "Paid", "Referral", "Direct"], n),
        }
    )
    return normalize(raw)


def money(value):
    try:
        return f"₹{float(value):,.0f}"
    except Exception:
        return "₹0"


def metric(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chart_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=46, b=10),
        autosize=True,
        font=dict(family="Inter"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)")
    return fig


def load_data():
    upload = st.sidebar.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx", "xls"],
        key="dataset_upload",
    )

    if upload is not None:
        started = time.perf_counter()
        file_bytes = upload.getvalue()
        signature = hashlib.sha256(file_bytes).hexdigest()

        if signature != st.session_state.file_signature:
            try:
                raw = parse_uploaded_file(file_bytes, upload.name)
                normalized = normalize(raw)
                st.session_state.data = normalized
                st.session_state.file_signature = signature
                st.session_state.filename = upload.name
                latency = (time.perf_counter() - started) * 1000
                audit(
                    "dataset.normalize",
                    latency_ms=latency,
                    status=200,
                    payload_size=len(file_bytes),
                    tokens=0,
                    detail=f"{upload.name} → {len(normalized):,} rows",
                )
                st.sidebar.success(f"Loaded {len(normalized):,} rows")
            except Exception as exc:
                audit(
                    "dataset.normalize",
                    latency_ms=(time.perf_counter() - started) * 1000,
                    status=422,
                    payload_size=len(file_bytes),
                    detail=str(exc),
                )
                st.sidebar.error(f"Dataset error: {exc}")
                return st.session_state.data
        elif st.session_state.data is not None:
            st.sidebar.caption("Dataset ready • cached")

    return st.session_state.data


# --------------------------- MEDDPICC ENGINE ---------------------------

MEDDPICC_FIELDS = [
    "Metrics",
    "Economic Buyer",
    "Decision Criteria",
    "Decision Process",
    "Paperwork",
    "Implied Pain",
    "Champion",
    "Competition",
]

MEDDPICC_PATTERNS = {
    "Metrics": [
        r"\b(?:metric|metrics|kpi|revenue|gmv|roi|growth|target|quota|saving|savings|increase|decrease|conversion)\b",
        r"\b\d+(?:\.\d+)?\s*(?:%|percent|crore|lakh|k|m|million|billion)\b",
    ],
    "Economic Buyer": [
        r"\b(?:economic buyer|budget owner|final approver|approver|cfo|ceo|vp finance|finance head)\b",
    ],
    "Decision Criteria": [
        r"\b(?:decision criteria|requirements|must have|must-have|security|pricing|integration|compliance|sla)\b",
    ],
    "Decision Process": [
        r"\b(?:decision process|procurement process|approval process|timeline|next step|evaluation|committee)\b",
    ],
    "Paperwork": [
        r"\b(?:paperwork|contract|agreement|msa|nda|legal|purchase order|po|dpa|terms)\b",
    ],
    "Implied Pain": [
        r"\b(?:pain|problem|challenge|issue|manual|slow|lost|churn|risk|bottleneck|inefficient|costly)\b",
    ],
    "Champion": [
        r"\b(?:champion|sponsor|advocate|internal owner|project owner)\b",
    ],
    "Competition": [
        r"\b(?:competitor|competition|alternative|incumbent|versus|vs\.|replace|replacement)\b",
    ],
}


def extract_meddpicc(notes):
    text = (notes or "").strip()
    result = {}

    for field in MEDDPICC_FIELDS:
        matches = []
        for pattern in MEDDPICC_PATTERNS[field]:
            matches.extend(re.findall(pattern, text, flags=re.IGNORECASE))
        result[field] = {
            "satisfied": bool(matches),
            "evidence": sorted(set(matches))[:8],
        }

    # Pull useful sentences as lightweight evidence.
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    for field, patterns in MEDDPICC_PATTERNS.items():
        evidence = []
        for sentence in sentences:
            if any(re.search(p, sentence, re.IGNORECASE) for p in patterns):
                evidence.append(sentence[:240])
        if evidence:
            result[field]["evidence_text"] = evidence[:2]
        else:
            result[field]["evidence_text"] = []

    satisfied = sum(v["satisfied"] for v in result.values())
    health = round((satisfied / len(MEDDPICC_FIELDS)) * 100)

    missing_critical = [
        field for field in ["Economic Buyer", "Champion", "Decision Process"]
        if not result[field]["satisfied"]
    ]

    result["_health"] = health
    result["_missing_critical"] = missing_critical
    return result


def meddpicc_panel(notes_key="meddpicc_notes"):
    st.markdown("### MEDDPICC Signal Extractor")
    notes = st.text_area(
        "Raw meeting notes",
        value=st.session_state.get("notes", ""),
        height=170,
        placeholder=(
            "Paste meeting notes. Example: CFO owns the budget; success metric is 20% "
            "GMV growth; security and API integration are required; procurement will "
            "review the MSA next week; the operations lead is our champion."
        ),
        key=notes_key,
    )
    st.session_state.notes = notes

    c1, c2 = st.columns([1, 1])
    with c1:
        extract_clicked = st.button("Extract MEDDPICC Signals", type="primary", use_container_width=True)
    with c2:
        clear_clicked = st.button("Clear Notes", use_container_width=True)

    if clear_clicked:
        st.session_state.notes = ""
        st.session_state.meddpicc = {}
        st.rerun()

    if extract_clicked:
        started = time.perf_counter()
        try:
            key = validate_idempotency_key()
            if key in st.session_state.idempotency_keys:
                st.warning("Duplicate submission detected — using the existing extraction.")
            else:
                # Optimistic UI: display an immediate working state, then commit.
                st.session_state.meddpicc = {"_status": "processing"}
                payload_bytes = len(notes.encode("utf-8"))
                extracted = extract_meddpicc(notes)
                st.session_state.meddpicc = extracted
                st.session_state.idempotency_keys.add(key)
                latency = (time.perf_counter() - started) * 1000
                audit(
                    "meddpicc.extract",
                    latency_ms=latency,
                    status=200,
                    payload_size=payload_bytes,
                    tokens=max(1, len(notes.split())),
                    detail=f"health={extracted['_health']}%",
                )
        except Exception as exc:
            st.session_state.meddpicc = {}
            audit(
                "meddpicc.extract",
                latency_ms=(time.perf_counter() - started) * 1000,
                status=400,
                payload_size=len(notes.encode("utf-8")),
                detail=str(exc),
            )
            st.error(str(exc))

    result = st.session_state.get("meddpicc") or {}
    if not result or result.get("_status") == "processing":
        if result.get("_status") == "processing":
            st.info("Extracting structured MEDDPICC signals…")
        return

    health = result.get("_health", 0)
    if health >= 75:
        st.success(f"Deal Health Score: {health}%")
    elif health >= 50:
        st.warning(f"Deal Health Score: {health}%")
    else:
        st.error(f"Deal Health Score: {health}%")

    cols = st.columns(4)
    for i, field in enumerate(MEDDPICC_FIELDS):
        data = result[field]
        with cols[i % 4]:
            if data["satisfied"]:
                st.markdown(f'<span class="status-ok">✓ {field.upper()}</span>', unsafe_allow_html=True)
            else:
                cls = "status-danger" if field in ["Economic Buyer", "Champion"] else "status-warn"
                st.markdown(f'<span class="{cls}">! MISSING {field.upper()}</span>', unsafe_allow_html=True)
            if data.get("evidence_text"):
                st.caption(data["evidence_text"][0])
            elif data["evidence"]:
                st.caption(", ".join(data["evidence"]))
            else:
                st.caption("No supporting signal found.")

    missing = result.get("_missing_critical", [])
    if missing:
        st.error("Critical gaps: " + " • ".join(missing))


# --------------------------- RISK SIGNALS ---------------------------

@st.cache_data(show_spinner=False)
def enrich_risk_signals(df):
    d = df.copy()
    revenue = d["Customer Value"]
    spend_ratio = d["Spend Ratio"]
    purchase = d["Purchases"]

    p99 = revenue.quantile(.99) if len(d) else 0
    p75 = revenue.quantile(.75) if len(d) else 0
    p25_purchase = purchase.quantile(.25) if len(d) else 0

    signals = []
    for _, row in d.iterrows():
        tags = []
        if row["Customer Value"] >= p99 and p99 > 0:
            tags.append(("TOP 1% GMV", "ok"))
        if row["Customer Value"] >= p75 and p75 > 0:
            tags.append(("HIGH VALUE", "ok"))
        if row["Purchases"] <= p25_purchase and row["Customer Value"] > p75:
            tags.append(("HIGH CHURN RISK", "danger"))
        if row["Spend Ratio"] > 0.20:
            tags.append(("HIGH ACQUISITION COST", "warn"))
        if row["Segment"] == "GROWTH":
            tags.append(("GROWTH SIGNAL", "info"))
        if not row["Email"] or row["Email"] == "Unknown":
            tags.append(("MISSING CONTACT", "warn"))
        if not tags:
            tags.append(("STANDARD", "info"))
        signals.append(tags)

    d["Risk Signals"] = signals
    d["Risk Signal Text"] = [" | ".join(x[0] for x in tags) for tags in signals]
    return d


def signal_html(tags):
    parts = []
    for text, kind in tags:
        parts.append(f'<span class="status-{kind}">{text}</span>')
    return "".join(parts)


# --------------------------- SIDEBAR ---------------------------

def system_health(df):
    st.sidebar.markdown("### SYSTEM HEALTH")
    expanded = st.sidebar.expander("Audit & Runtime", expanded=False)

    with expanded:
        file_hash = st.session_state.get("file_signature") or "NO_DATASET"
        st.markdown(
            f"""
            <div class="audit-shell" style="padding:10px;">
                <div class="audit-row"><span class="audit-key">RUNTIME</span><span class="audit-value">{platform.python_version()}</span></div>
                <div class="audit-row"><span class="audit-key">MEMORY</span><span class="audit-value">{memory_mb():.1f} MB</span></div>
                <div class="audit-row"><span class="audit-key">DATAFRAME</span><span class="audit-value">{dataframe_mb(df):.2f} MB</span></div>
                <div class="audit-row"><span class="audit-key">ROWS</span><span class="audit-value">{len(df):,}</span></div>
                <div class="audit-row"><span class="audit-key">SHA256</span><span class="audit-value">{file_hash[:16]}…</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.audit_log:
            st.markdown("**Recent execution events**")
            audit_df = pd.DataFrame(st.session_state.audit_log[::-1]).head(12)
            st.dataframe(audit_df, use_container_width=True, hide_index=True, height=260)
        else:
            st.caption("No execution events yet.")


def sidebar(df):
    logo = next((p for p in LOGO_CANDIDATES if p.exists()), None)
    if logo:
        st.sidebar.image(str(logo), width=150)
    else:
        st.sidebar.markdown("<div style='font-size:36px'>🚀</div>", unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        <div class="brand">
            <div class="brand-title">RevPilot AI</div>
            <div class="brand-sub">Revenue Intelligence OS</div>
            <div class="live">● LIVE DATA MODE</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    system_health(df)

    st.sidebar.markdown("### WORKSPACE")
    page = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Executive Dashboard",
            "👥 Customer Intelligence",
            "🎯 AI Target Customers",
            "🔮 Campaign Prediction",
            "📈 Revenue Analytics",
            "💬 AI Outreach & Engagement",
            "⚙️ Data & Settings",
            "ℹ️ About",
        ],
        label_visibility="collapsed",
    )

    st.sidebar.markdown("### DATA")
    data = load_data()

    st.sidebar.divider()
    st.sidebar.markdown("### DEVELOPER")
    st.sidebar.markdown(
        f"""
        <div class="small">
            <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a><br>
            <a href="{GITHUB_URL}" target="_blank">GitHub</a><br>
            <a href="{PORTFOLIO_URL}" target="_blank">Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.caption(f"{DEVELOPER_NAME} | {PROJECT_CONTEXT}")

    return page, data


# --------------------------- COMMAND PALETTE ---------------------------

@st.dialog("Command Palette")
def command_palette():
    st.caption("Use the command box to jump or execute an action.")
    command = st.text_input(
        "Command",
        placeholder="dashboard, customers, targets, outreach, extract, clear",
        key="command_palette_input",
    ).strip().lower()

    if st.button("Run Command", type="primary", use_container_width=True):
        routes = {
            "dashboard": "🏠 Executive Dashboard",
            "customers": "👥 Customer Intelligence",
            "customer": "👥 Customer Intelligence",
            "targets": "🎯 AI Target Customers",
            "campaign": "🔮 Campaign Prediction",
            "analytics": "📈 Revenue Analytics",
            "outreach": "💬 AI Outreach & Engagement",
            "settings": "⚙️ Data & Settings",
            "about": "ℹ️ About",
        }
        if command in routes:
            st.session_state.command_result = routes[command]
            st.success(f"Navigate to {routes[command]}")
            st.rerun()
        elif command in {"clear", "clear notes"}:
            st.session_state.notes = ""
            st.session_state.meddpicc = {}
            st.success("Notes cleared.")
        elif command in {"extract", "extract meddpicc"}:
            if st.session_state.notes.strip():
                st.session_state.meddpicc = extract_meddpicc(st.session_state.notes)
                st.success("MEDDPICC extraction completed.")
            else:
                st.warning("Add meeting notes first.")
        else:
            st.warning("Unknown command. Try dashboard, customers, targets, outreach, extract, or clear.")


def command_palette_launcher():
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("⌘K", use_container_width=True):
            command_palette()
    st.markdown('<div class="command-hint">Command palette: Ctrl + K / Cmd + K • Use the ⌘K control to open</div>', unsafe_allow_html=True)


# --------------------------- PAGES ---------------------------

def landing():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">REVENUE INTELLIGENCE OS</div>
            <h1>RevPilot AI</h1>
            <p>Enterprise customer intelligence for prioritization, campaign planning, revenue analytics, MEDDPICC deal signals, and CRM-ready outreach.</p>
            <br>
            <span class="status-info">● WAITING FOR DATASET</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric("DATA INGESTION", "CSV / XLSX / XLS", "Cached parsing")
    with c2:
        metric("INTELLIGENCE", "MEDDPICC + AI", "Signal extraction")
    with c3:
        metric("OPERATIONS", "CRM READY", "Webhook payloads")

    st.markdown(
        """
        <div class="blade-card">
            <div class="section-title">Start with your revenue data</div>
            <div class="small">
                Upload a dataset from the sidebar. RevPilot AI automatically normalizes common
                customer, revenue, order, spend, channel and contact fields. A deterministic
                demo dataset remains available through Data & Settings for offline product review.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard(df):
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">EXECUTIVE CONTROL PLANE</div>
            <h1>Revenue command center</h1>
            <p>High-density view of customer value, revenue concentration, channels and priority accounts.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    avg_customer_value = df["Customer Value"].sum() / max(len(df), 1)
    high_value = int((df["Segment"] == "HIGH VALUE").sum())
    total_purchases = df["Purchases"].sum()
    aov = df["Revenue"].sum() / max(total_purchases, 1)

    c = st.columns(5)
    with c[0]: metric("Customers", f"{len(df):,}", "Active rows")
    with c[1]: metric("Revenue", money(df["Revenue"].sum()), "Customer value")
    with c[2]: metric("Avg Customer Value", money(avg_customer_value), "Revenue / customer")
    with c[3]: metric("High-Value", f"{high_value:,}", "Segment")
    with c[4]: metric("AOV", money(aov), "Revenue / purchase")

    left, right = st.columns(2)

    with left:
        seg = (
            df.groupby("Segment", as_index=False)["Customer Value"]
            .sum()
            .sort_values("Customer Value", ascending=False)
        )
        fig = px.bar(seg, x="Segment", y="Customer Value", title="Customer Value by Segment", text_auto=".2s")
        st.plotly_chart(chart_theme(fig), use_container_width=True)

    with right:
        ch = df.groupby("Channel", as_index=False)["Revenue"].sum()
        fig = px.pie(ch, names="Channel", values="Revenue", title="Revenue Mix by Channel", hole=.55)
        st.plotly_chart(chart_theme(fig), use_container_width=True)

    st.markdown("### Top Revenue Accounts")
    cols = ["Customer ID", "Name", "Segment", "Revenue", "Purchases", "Spend", "Channel"]
    top = df.nlargest(10, "Revenue")[cols].copy()
    top["Revenue"] = top["Revenue"].map(money)
    top["Spend"] = top["Spend"].map(money)
    st.dataframe(top, use_container_width=True, hide_index=True)


def customer_intelligence(df):
    st.markdown("## 👥 Customer Intelligence")
    st.caption("Customer-level operating view with segmentation and automated risk signals.")

    options = sorted(df["Segment"].dropna().unique().tolist())
    selected = st.multiselect("Segments", options, default=options)

    view = df[df["Segment"].isin(selected)].copy() if selected else df.iloc[0:0].copy()
    enriched = enrich_risk_signals(view)

    c = st.columns(4)
    with c[0]: metric("Customers", f"{len(view):,}")
    with c[1]: metric("Revenue", money(view["Revenue"].sum()))
    with c[2]: metric("Avg Value", money(view["Customer Value"].mean() if len(view) else 0))
    with c[3]: metric("Avg AOV", money(view["Avg Order Value"].mean() if len(view) else 0))

    search = st.text_input("Search customer", placeholder="Name, customer ID, email")
    if search.strip():
        q = search.lower().strip()
        enriched = enriched[
            enriched["Name"].str.lower().str.contains(q, na=False)
            | enriched["Customer ID"].str.lower().str.contains(q, na=False)
            | enriched["Email"].str.lower().str.contains(q, na=False)
        ]

    page_size = st.selectbox("Rows", [25, 50, 100, 250], index=1)
    page_num = st.number_input(
        "Page",
        min_value=1,
        max_value=max(1, int(np.ceil(len(enriched) / page_size))),
        value=1,
    )
    start = (page_num - 1) * page_size
    page_df = enriched.iloc[start:start + page_size].copy()

    display_cols = [
        "Customer ID", "Name", "Segment", "Customer Value",
        "Purchases", "Avg Order Value", "Spend Ratio", "Channel",
        "City", "Risk Signal Text"
    ]
    st.dataframe(page_df[display_cols], use_container_width=True, hide_index=True)

    st.markdown("### MEDDPICC Deal Notes")
    meddpicc_panel()


def target_customers(df):
    st.markdown("## 🎯 AI Target Customers")
    st.caption("Priority = Value 45% + Purchases 25% + Spend Ratio 10% + Segment Bonus 20%.")

    d = enrich_risk_signals(df.copy())

    def pct_rank(s):
        return s.rank(pct=True).fillna(0)

    d["Value Score"] = pct_rank(d["Customer Value"]) * 45
    d["Purchase Score"] = pct_rank(d["Purchases"]) * 25

    # Lower acquisition spend relative to revenue is preferred.
    spend_rank = pct_rank(d["Spend Ratio"])
    d["Spend Score"] = (1 - spend_rank) * 10

    bonus = d["Segment"].map(
        {"HIGH VALUE": 20, "LOYAL": 16, "GROWTH": 12, "STANDARD": 6}
    ).fillna(0)

    d["Segment Bonus"] = bonus
    d["Priority Score"] = (
        d["Value Score"] +
        d["Purchase Score"] +
        d["Spend Score"] +
        d["Segment Bonus"]
    ).clip(0, 100)

    top_n = st.slider(
        "Target accounts",
        5,
        min(100, max(5, len(d))),
        min(20, len(d)),
        5,
    )

    top = d.nlargest(top_n, "Priority Score").sort_values("Priority Score")

    fig = px.bar(
        top,
        x="Priority Score",
        y="Name",
        color="Segment",
        orientation="h",
        title="AI Priority Ranking",
        hover_data=["Revenue", "Purchases", "Spend Ratio", "Risk Signal Text"],
    )
    st.plotly_chart(chart_theme(fig), use_container_width=True)

    top_display = d.nlargest(top_n, "Priority Score")[
        [
            "Customer ID", "Name", "Segment", "Revenue", "Purchases",
            "Spend Ratio", "Priority Score", "Risk Signal Text"
        ]
    ].copy()
    top_display["Risk Signals"] = [
        signal_html(tags) for tags in d.nlargest(top_n, "Priority Score")["Risk Signals"]
    ]

    st.dataframe(top_display.drop(columns=["Risk Signals"]), use_container_width=True, hide_index=True)

    st.markdown("### MEDDPICC + Risk Signals")
    meddpicc_panel("target_meddpicc_notes")


def campaign_prediction(df):
    st.markdown("## 🔮 Campaign Prediction")
    st.caption("Deterministic scenario model for portfolio/demo decision support.")

    a, b, c = st.columns(3)
    with a:
        quality = st.slider("Campaign quality adjustment", 50, 150, 100, 5) / 100
    with b:
        realization = st.slider("Revenue realization rate", 20, 100, 70, 5) / 100
    with c:
        cost_rate = st.slider("Variable cost rate", 1, 40, 12, 1) / 100

    base_response = float(
        np.clip(
            .04 + min(.12, float(df["Purchases"].mean()) / 300),
            .02,
            .16,
        )
    )
    blended = float(np.clip(base_response * quality, .01, .35))
    audience = len(df)
    expected_orders = audience * blended
    avg_order_value = float(df["Avg Order Value"].mean()) if len(df) else 0
    expected_revenue = expected_orders * avg_order_value * realization
    campaign_cost = expected_revenue * cost_rate
    contribution = expected_revenue - campaign_cost
    roi = (contribution / campaign_cost) if campaign_cost > 0 else 0

    cols = st.columns(5)
    values = [
        (cols[0], "Response", f"{blended * 100:.1f}%", "Blended rate"),
        (cols[1], "Expected Orders", f"{expected_orders:,.0f}", "Model estimate"),
        (cols[2], "Expected Revenue", money(expected_revenue), "Realized"),
        (cols[3], "Campaign Cost", money(campaign_cost), "Variable"),
        (cols[4], "ROI Multiplier", f"{roi:.2f}x", "Contribution / cost"),
    ]
    for col, label, value, note in values:
        with col:
            metric(label, value, note)

    scenario = pd.DataFrame(
        {
            "Scenario": ["Conservative", "Base", "Optimistic"],
            "Quality": [max(.5, quality - .15), quality, min(1.5, quality + .15)],
        }
    )
    scenario["Response"] = np.clip(base_response * scenario["Quality"], .01, .35)
    scenario["Revenue"] = scenario["Response"] * audience * avg_order_value * realization
    fig = px.bar(scenario, x="Scenario", y="Revenue", title="Revenue Scenario")
    st.plotly_chart(chart_theme(fig), use_container_width=True)

    st.info("Forecasts are estimates for decision support and are not guaranteed outcomes.")


def revenue_analytics(df):
    st.markdown("## 📈 Revenue Analytics")
    numeric = [
        "Revenue",
        "Customer Value",
        "Purchases",
        "Spend",
        "Avg Order Value",
        "Spend Ratio",
    ]
    metric_name = st.selectbox("Distribution metric", numeric)

    chart_df = df
    if len(df) > 100_000:
        chart_df = df.sample(100_000, random_state=42)

    fig = px.histogram(
        chart_df,
        x=metric_name,
        marginal="box",
        nbins=40,
        title=f"{metric_name} Distribution",
    )
    st.plotly_chart(chart_theme(fig), use_container_width=True)

    scatter = chart_df
    fig2 = px.scatter(
        scatter,
        x="Purchases",
        y="Customer Value",
        color="Segment",
        size="Spend",
        hover_name="Name",
        title="Purchases vs Customer Value",
    )
    st.plotly_chart(chart_theme(fig2), use_container_width=True)


# --------------------------- OUTREACH + WEBHOOK ---------------------------

def make_message(row, objective, tone, channel):
    name = row.get("Name", "Customer")
    segment = row.get("Segment", "STANDARD")
    value = money(float(row.get("Customer Value", 0)))

    openings = {
        "Professional": f"Hello {name},",
        "Friendly": f"Hi {name}! 👋",
        "Urgent": f"Hi {name}, quick opportunity for you:",
    }

    bodies = {
        "Win-back": (
            f"We noticed it has been a while since your last purchase. "
            f"As a {segment.lower()} customer with previous value of {value}, "
            f"we would like to welcome you back with a tailored offer."
        ),
        "Upsell": (
            f"As a valued {segment.lower()} customer, we identified an opportunity "
            f"that may be a strong fit. Your current customer value is {value}."
        ),
        "Exclusive Discount": (
            f"We have an exclusive benefit based on your customer relationship with us. "
            f"Your previous value is {value}, and we would like to make your next purchase more rewarding."
        ),
        "Loyalty Reward": (
            f"Thank you for being a valued {segment.lower()} customer. "
            f"Your relationship with us is worth {value}, and we have a special loyalty reward for you."
        ),
    }

    body = openings[tone] + "\n\n" + bodies[objective] + "\n\nWould you like me to share the details?"

    if channel == "Email":
        return f"Subject: A personalized opportunity for you\n\n{body}\n\nRegards,\nRevPilot AI Team"

    return body


def build_crm_payload(row, objective, tone, channel, message):
    payload = {
        "event": "customer_outreach.created",
        "source": "revpilot_ai",
        "version": "1.0",
        "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "idempotency_key": validate_idempotency_key(),
        "customer": {
            "customer_id": str(row.get("Customer ID", "")),
            "name": str(row.get("Name", "")),
            "email": str(row.get("Email", "")),
            "phone": str(row.get("Phone", "")),
            "city": str(row.get("City", "")),
            "segment": str(row.get("Segment", "")),
            "customer_value": float(row.get("Customer Value", 0)),
            "purchases": float(row.get("Purchases", 0)),
            "channel": str(row.get("Channel", "")),
        },
        "campaign": {
            "objective": objective,
            "tone": tone,
            "outreach_type": channel,
        },
        "content": {
            "message": message,
        },
        "metadata": {
            "app": "RevPilot AI — Revenue Intelligence",
            "environment": "portfolio-demo",
        },
    }
    return payload


def outreach(df):
    st.markdown("## 💬 AI Outreach & Engagement")
    st.caption("Personalized messaging plus a CRM-ready webhook payload.")

    search = st.text_input("Search customer", placeholder="Name, ID or email")
    filtered = df

    if search.strip():
        q = search.strip().lower()
        filtered = df[
            df["Name"].str.lower().str.contains(q, na=False)
            | df["Customer ID"].str.lower().str.contains(q, na=False)
            | df["Email"].str.lower().str.contains(q, na=False)
        ]

    if filtered.empty:
        st.warning("No matching customer found.")
        return

    choices = filtered.index.tolist()
    selected_idx = st.selectbox(
        "Target customer",
        choices,
        format_func=lambda i: (
            f"{df.loc[i, 'Name']} — {df.loc[i, 'Customer ID']} — "
            f"{df.loc[i, 'Segment']}"
        ),
    )

    row = df.loc[selected_idx]

    left, right = st.columns([1, 2])
    with left:
        st.markdown(
            f"""
            <div class="blade-card">
                <div class="eyebrow">CUSTOMER PROFILE</div>
                <h3>{row["Name"]}</h3>
                <div class="small">{row["Customer ID"]} • {row["Segment"]}</div>
                <hr>
                <div class="mono">VALUE&nbsp;&nbsp;&nbsp; {money(row["Customer Value"])}</div>
                <div class="mono">PURCHASE {row["Purchases"]:,.0f}</div>
                <div class="mono">AOV&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {money(row["Avg Order Value"])}</div>
                <div class="mono">CHANNEL&nbsp;&nbsp; {row["Channel"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        a, b, c = st.columns(3)
        with a:
            channel = st.selectbox("Outreach type", ["Email", "WhatsApp/SMS", "Both"])
        with b:
            objective = st.selectbox(
                "Campaign objective",
                ["Win-back", "Upsell", "Exclusive Discount", "Loyalty Reward"],
            )
        with c:
            tone = st.selectbox("Tone", ["Professional", "Friendly", "Urgent"])

        if st.button("Generate AI Message", type="primary", use_container_width=True):
            started = time.perf_counter()
            try:
                key = validate_idempotency_key()
                if key in st.session_state.idempotency_keys:
                    st.warning("Duplicate generation request detected.")
                else:
                    # Optimistic state
                    previous = st.session_state.generated_message
                    st.session_state.optimistic_campaign = True
                    msg_email = make_message(row, objective, tone, "Email")
                    msg_sms = make_message(row, objective, tone, "WhatsApp/SMS")
                    generated = (
                        f"EMAIL\n\n{msg_email}\n\n---\n\nWHATSAPP/SMS\n\n{msg_sms}"
                        if channel == "Both"
                        else (msg_email if channel == "Email" else msg_sms)
                    )
                    st.session_state.generated_message = generated
                    st.session_state.optimistic_campaign = False
                    st.session_state.idempotency_keys.add(key)
                    audit(
                        "outreach.generate",
                        latency_ms=(time.perf_counter() - started) * 1000,
                        status=200,
                        payload_size=len(generated.encode("utf-8")),
                        tokens=len(generated.split()),
                        detail=f"{row['Customer ID']} / {channel}",
                    )
            except Exception as exc:
                st.session_state.generated_message = previous
                st.session_state.optimistic_campaign = False
                st.session_state.campaign_error = str(exc)
                audit(
                    "outreach.generate",
                    latency_ms=(time.perf_counter() - started) * 1000,
                    status=400,
                    detail=str(exc),
                )
                st.error(f"Generation rolled back: {exc}")

    if st.session_state.get("generated_message"):
        st.text_area(
            "Ready-to-send message",
            st.session_state.generated_message,
            height=260,
        )

        b1, b2, b3 = st.columns(3)
        with b1:
            if st.button("Export CRM Webhook Payload", type="primary", use_container_width=True):
                started = time.perf_counter()
                try:
                    message = st.session_state.generated_message
                    payload = build_crm_payload(row, objective, tone, channel, message)
                    st.session_state.generated_payload = json.dumps(payload, indent=2, ensure_ascii=False)
                    audit(
                        "crm.webhook.build",
                        latency_ms=(time.perf_counter() - started) * 1000,
                        status=200,
                        payload_size=len(st.session_state.generated_payload.encode("utf-8")),
                        tokens=len(st.session_state.generated_payload.split()),
                        detail="Salesforce/HubSpot compatible structure",
                    )
                except Exception as exc:
                    audit(
                        "crm.webhook.build",
                        latency_ms=(time.perf_counter() - started) * 1000,
                        status=400,
                        detail=str(exc),
                    )
                    st.error(str(exc))

        with b2:
            if st.button("Send Campaign via API", use_container_width=True):
                started = time.perf_counter()
                previous_log = list(st.session_state.sent_log)
                try:
                    key = validate_idempotency_key()
                    if key in st.session_state.idempotency_keys:
                        raise ValueError("Duplicate idempotency key — request rejected.")
                    # Optimistic append.
                    entry = {
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Customer": row["Name"],
                        "Customer ID": row["Customer ID"],
                        "Channel": channel,
                        "Objective": objective,
                        "HTTP": 200,
                        "Status": "SIMULATED_SENT",
                    }
                    st.session_state.sent_log.append(entry)
                    st.session_state.idempotency_keys.add(key)
                    audit(
                        "campaign.send",
                        latency_ms=(time.perf_counter() - started) * 1000,
                        status=200,
                        payload_size=len(st.session_state.generated_message.encode("utf-8")),
                        tokens=len(st.session_state.generated_message.split()),
                        detail=f"optimistic commit {row['Customer ID']}",
                    )
                    st.success("Campaign API simulation completed.")
                except Exception as exc:
                    # Graceful rollback
                    st.session_state.sent_log = previous_log
                    audit(
                        "campaign.send",
                        latency_ms=(time.perf_counter() - started) * 1000,
                        status=409,
                        detail=f"rollback: {exc}",
                    )
                    st.error(f"Send failed — state rolled back: {exc}")

        with b3:
            st.download_button(
                "Download Message",
                st.session_state.generated_message.encode("utf-8"),
                file_name=f"revpilot_{row['Customer ID']}_outreach.txt",
                mime="text/plain",
                use_container_width=True,
            )

    if st.session_state.get("generated_payload"):
        st.markdown("### CRM Webhook Payload")
        st.code(st.session_state.generated_payload, language="json")
        st.download_button(
            "Download CRM JSON",
            st.session_state.generated_payload.encode("utf-8"),
            file_name=f"revpilot_{row['Customer ID']}_crm_webhook.json",
            mime="application/json",
            use_container_width=True,
        )

    if st.session_state.get("sent_log"):
        st.markdown("### Campaign Audit History")
        st.dataframe(
            pd.DataFrame(st.session_state.sent_log[::-1]),
            use_container_width=True,
            hide_index=True,
        )


def settings(df):
    st.markdown("## ⚙️ Data & Settings")

    c = st.columns(5)
    with c[0]: metric("Rows", f"{len(df):,}", "Active customer rows")
    with c[1]: metric("Columns", f"{len(df.columns):,}", "Normalized fields")
    with c[2]: metric("Revenue", money(df["Revenue"].sum()), "Customer value")
    with c[3]: metric("Memory", f"{dataframe_mb(df):.1f} MB", "DataFrame footprint")
    with c[4]: metric("Status", "READY", "Pipeline healthy")

    st.markdown("### Dataset Signature")
    st.code(st.session_state.get("file_signature") or "DEMO / NO UPLOAD")

    st.markdown("### Dynamic Preview")
    rows = st.slider("Preview rows", 5, min(100, max(5, len(df))), min(25, max(5, len(df))))
    st.dataframe(df.head(rows), use_container_width=True, hide_index=True)

    st.download_button(
        "Download Normalized CSV",
        df.to_csv(index=False).encode("utf-8"),
        "revpilot_normalized.csv",
        "text/csv",
        use_container_width=True,
    )

    st.markdown("### Pipeline Contract")
    st.markdown(
        """
        <div class="blade-card">
            <div class="small">
                <b>Idempotency:</b> payload submissions validate <span class="mono">X-Idempotency-Key</span>.
                &nbsp; <b>Cache:</b> parsing and normalization are cached by Streamlit.
                &nbsp; <b>Observability:</b> execution latency, status, payload size and token estimates are retained in-session.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def about_page():
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">PRODUCT OVERVIEW</div>
            <h1>RevPilot AI</h1>
            <p>Revenue Intelligence OS for customer prioritization, revenue analytics, campaign planning, MEDDPICC signals and CRM-ready engagement.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        metric("INTELLIGENCE", "MEDDPICC", "Deal gap engine")
    with c2:
        metric("PRIORITIZATION", "0–100", "Customer score")
    with c3:
        metric("OPERATIONS", "CRM JSON", "Webhook-ready")

    st.markdown("### Product Capabilities")
    capabilities = [
        ("Customer Intelligence", "Segment customers, inspect value, purchases, AOV, spend and risk signals."),
        ("AI Targeting", "Rank accounts using weighted value, purchase, spend and segment factors."),
        ("Campaign Prediction", "Model response, expected revenue, variable cost and ROI multiplier."),
        ("MEDDPICC Extraction", "Convert raw meeting notes into structured signals and identify critical deal gaps."),
        ("AI Outreach", "Generate personalized messages by channel, objective and tone."),
        ("CRM Webhooks", "Export structured JSON payloads for Salesforce/HubSpot-style synchronization."),
        ("Observability", "Track latency, HTTP status, payload size, token estimate and memory footprint."),
        ("Performance", "Cache parsing and normalization and avoid re-processing unchanged files."),
    ]

    for start in range(0, len(capabilities), 2):
        cols = st.columns(2)
        for col, (title, desc) in zip(cols, capabilities[start:start + 2]):
            with col:
                st.markdown(
                    f"""
                    <div class="blade-card">
                        <h3>{title}</h3>
                        <div class="small">{desc}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("### Technology")
    st.markdown(
        """
        <div class="blade-card">
            <span class="status-info">Python</span>
            <span class="status-info">Streamlit</span>
            <span class="status-info">Pandas</span>
            <span class="status-info">NumPy</span>
            <span class="status-info">Plotly</span>
            <span class="status-info">API Integration</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Developer")
    st.markdown(
        f"""
        <div class="blade-card">
            <h3>{DEVELOPER_NAME}</h3>
            <div class="small">{PROJECT_CONTEXT}</div>
            <br>
            <a href="{LINKEDIN_URL}" target="_blank">LinkedIn</a>
            &nbsp; • &nbsp;
            <a href="{GITHUB_URL}" target="_blank">GitHub</a>
            &nbsp; • &nbsp;
            <a href="{PORTFOLIO_URL}" target="_blank">Portfolio</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------- MAIN ---------------------------

def main():
    inject_css()

    # The command palette can safely be opened from a normal Streamlit control.
    if st.session_state.get("command_result"):
        page_override = st.session_state.command_result
        st.session_state.command_result = ""
    else:
        page_override = None

    # Load data after the sidebar controls so the sidebar remains responsive.
    page, df = sidebar(st.session_state.data)
    if page_override:
        page = page_override

    command_palette_launcher()

    # Demo fallback remains available without pretending it is live customer data.
    if page == "ℹ️ About":
        about_page()
        return

    if df is None or df.empty:
        landing()
        st.markdown("### Offline demo")
        if st.button("Load deterministic demo dataset", use_container_width=True):
            started = time.perf_counter()
            st.session_state.data = demo_data()
            st.session_state.filename = "demo_data"
            st.session_state.file_signature = hashlib.sha256(
                b"revpilot-deterministic-demo-v1"
            ).hexdigest()
            audit(
                "demo.load",
                latency_ms=(time.perf_counter() - started) * 1000,
                status=200,
                detail=f"{len(st.session_state.data):,} rows",
            )
            st.rerun()
        return

    if page == "🏠 Executive Dashboard":
        dashboard(df)
    elif page == "👥 Customer Intelligence":
        customer_intelligence(df)
    elif page == "🎯 AI Target Customers":
        target_customers(df)
    elif page == "🔮 Campaign Prediction":
        campaign_prediction(df)
    elif page == "📈 Revenue Analytics":
        revenue_analytics(df)
    elif page == "💬 AI Outreach & Engagement":
        outreach(df)
    elif page == "⚙️ Data & Settings":
        settings(df)


if __name__ == "__main__":
    main()

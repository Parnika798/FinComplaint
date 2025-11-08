import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------
st.set_page_config(
    page_title="Banking Complaint Intelligence Dashboard",
    layout="wide"
)

# --------------------------------------------------------
# Load Custom CSS (FIXED & IMPROVED)
# --------------------------------------------------------
def load_css():
    css = """
    <style>

    /* Reset Streamlit spacing */
    .stApp, .main, .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Background */
    .stApp {
        background-color: #f4f7fb !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Sidebar */
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        height: 100vh;
        width: 260px;
        background: linear-gradient(180deg, #003366 0%, #005095 100%);
        padding: 30px 20px;
        color: white;
        z-index: 100;
    }

    .sidebar-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 25px;
        color: #fff;
    }

    .nav-button {
        padding: 12px 16px;
        margin-bottom: 12px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 16px;
        font-weight: 600;
        transition: 0.2s;
        background: rgba(255,255,255,0.12);
    }
    .nav-button:hover {
        background: rgba(255,255,255,0.25);
    }
    .nav-active {
        background: rgba(255,255,255,0.35) !important;
        color: #002744 !important;
    }

    /* Shift main content right to prevent overlap */
    .main-container {
        margin-left: 280px !important;
        padding: 30px;
    }

    /* Top bar */
    .top-nav {
        width: 100%;
        padding: 22px 32px;
        background: linear-gradient(90deg, #003366 0%, #004a85 100%);
        border-radius: 12px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    .top-nav-title {
        font-size: 32px;
        font-weight: 900;
    }
    .top-nav-sub {
        font-size: 15px;
        margin-top: -6px;
        color: #dbe7f3;
    }

    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.88);
        backdrop-filter: blur(8px);
        padding: 28px;
        border-radius: 18px;
        margin-bottom: 25px;
        box-shadow: 0 6px 26px rgba(0,0,0,0.06);
        border: 1px solid #e8edf3;
    }

    /* Upload Box */
    .upload-box {
        border: 2px dashed #7d9ecb;
        padding: 40px;
        text-align: center;
        border-radius: 18px;
        background: #f0f5fb;
        transition: 0.2s ease;
    }
    .upload-box:hover {
        background: #e6eff8;
        border-color: #004a85;
    }

    /* Buttons */
    .stButton > button {
        background: #004a85 !important;
        color: white !important;
        padding: 0.7rem 1.6rem !important;
        font-size: 17px !important;
        border-radius: 8px !important;
        border: none !important;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: #003a6c !important;
        transform: translateY(-2px);
    }

    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 22px;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 3px 12px rgba(0,0,0,0.07);
        border: 1px solid #e6e9ef;
    }
    .kpi-number {
        font-size: 34px;
        font-weight: 800;
        color: #002f5e;
    }
    .kpi-label {
        font-size: 15px;
        color: #4b6285;
        margin-top: -6px;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --------------------------------------------------------
# Load Model
# --------------------------------------------------------
@st.cache_resource
def load_components():
    pipeline = joblib.load("model/clf_pipeline1.pkl")
    label_encoder = joblib.load("model/label_encoder1.pkl")
    id2label = {i: label for i, label in enumerate(label_encoder.classes_)}
    return pipeline, label_encoder, id2label

pipeline, label_encoder, id2label = load_components()

def predict_category(text):
    pred = pipeline.predict([str(text)])[0]
    return id2label[pred]


# --------------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------------
st.markdown("""
<div class="sidebar">
    <div class="sidebar-title">Complaint AI</div>
    <div class="nav-button" onclick="window.location.href='/?page=upload'">Upload Data</div>
    <div class="nav-button" onclick="window.location.href='/?page=insights'">Insights</div>
    <div class="nav-button" onclick="window.location.href='/?page=download'">Download</div>
</div>
""", unsafe_allow_html=True)

page = st.experimental_get_query_params().get("page", ["upload"])[0]

# --------------------------------------------------------
# MAIN CONTENT START
# --------------------------------------------------------
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Top Banner
st.markdown("""
<div class="top-nav">
    <div class="top-nav-title">Banking Complaint Intelligence Dashboard</div>
    <div class="top-nav-sub">Enterprise-grade analytics for customer grievance management</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# PAGE LOGIC
# --------------------------------------------------------
if page == "upload":

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Complaint File")

    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)

        if "complaint_text" not in df.columns:
            st.error("Missing 'complaint_text' column.")
        else:
            df["predicted_category"] = df["complaint_text"].apply(predict_category)
            st.session_state["df"] = df
            st.success("File processed successfully.")
            st.dataframe(df.head(), use_container_width=True)


elif page == "insights":

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:

        df = st.session_state["df"]

        st.subheader("Key Metrics")

        total = len(df)
        top_category = df["predicted_category"].value_counts().idxmax()
        unique = df["predicted_category"].nunique()

        k1, k2, k3 = st.columns(3)
        k1.markdown(f'<div class="kpi-card"><div class="kpi-number">{total}</div><div class="kpi-label">Total Complaints</div></div>', unsafe_allow_html=True)
        k2.markdown(f'<div class="kpi-card"><div class="kpi-number">{top_category}</div><div class="kpi-label">Most Frequent Category</div></div>', unsafe_allow_html=True)
        k3.markdown(f'<div class="kpi-card"><div class="kpi-number">{unique}</div><div class="kpi-label">Unique Categories</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("Category Breakdown")

        counts = df["predicted_category"].value_counts().reset_index()
        counts.columns = ["Category", "Count"]

        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(px.bar(counts, x="Category", y="Count", color="Category", text_auto=True), use_container_width=True)
        with c2:
            st.plotly_chart(px.pie(counts, names="Category", values="Count", hole=0.4), use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


elif page == "download":

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Download Results")

        csv = st.session_state["df"].to_csv(index=False)
        st.download_button("Download Classified CSV", csv, "classified_complaints.csv", "text/csv")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

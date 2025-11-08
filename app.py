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
# Load Custom CSS
# --------------------------------------------------------
def load_css():
    css = """
    <style>

    /* Background */
    body {
        background-color: #eef3f9 !important;
        font-family: 'Inter', sans-serif;
    }
    .block-container {
        padding-top: 1rem;
    }

    /* Banking Blue Theme */
    h1, h2, h3, h4 {
        color: #003d79 !important;
        font-weight: 800 !important;
    }

    .header-title {
        font-size: 34px !important;
        font-weight: 900 !important;
        color: #002f5e !important;
        margin-bottom: 6px;
    }
    .header-subtitle {
        font-size: 18px;
        color: #315a89;
        margin-top: -10px;
        margin-bottom: 20px;
    }

    /* Cards */
    .card {
        padding: 22px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
        margin-bottom: 25px;
    }

    /* Clean buttons */
    .stButton > button {
        background-color: #003d79 !important;
        color: white !important;
        border-radius: 6px;
        padding: 0.6rem 1.3rem;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }
    .stButton > button:hover {
        background-color: #002f5e !important;
    }

    /* Enlarged Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 20px !important;
        font-weight: 700 !important;
        padding: 15px 28px !important;
        color: #003d79 !important;
    }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

load_css()

# --------------------------------------------------------
# Load Model + Label Encoder
# --------------------------------------------------------
@st.cache_resource
def load_components():
    pipeline = joblib.load("model/clf_pipeline1.pkl")
    label_encoder = joblib.load("model/label_encoder1.pkl")
    id2label = {i: label for i, label in enumerate(label_encoder.classes_)}
    return pipeline, label_encoder, id2label

pipeline, label_encoder, id2label = load_components()


def predict_category(text):
    pred_encoded = pipeline.predict([str(text)])[0]
    return id2label[pred_encoded]

# --------------------------------------------------------
# Header
# --------------------------------------------------------
st.markdown("""
<div>
    <h1 class="header-title">Banking Complaint Intelligence Dashboard</h1>
    <p class="header-subtitle">Upload complaint data, analyze trends, and extract insights instantly.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Tabs
# --------------------------------------------------------
tabs = st.tabs(["Upload Data", "Insights & Analytics", "Download Results"])

# --------------------------------------------------------
# TAB 1 — UPLOAD
# --------------------------------------------------------
with tabs[0]:

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Upload Complaint File (CSV or Excel)")
    file = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        if file.name.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        if "complaint_text" not in df.columns:
            st.error("The uploaded file must contain a 'complaint_text' column.")
        else:
            st.success("File uploaded successfully.")
            st.dataframe(df.head(), use_container_width=True)

            df["predicted_category"] = df["complaint_text"].apply(predict_category)

            st.session_state["df"] = df


# --------------------------------------------------------
# TAB 2 — INSIGHTS
# --------------------------------------------------------
with tabs[1]:

    if "df" not in st.session_state:
        st.info("Please upload a file first.")
    else:
        df = st.session_state["df"]

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Category Distribution")

        counts = df["predicted_category"].value_counts().reset_index()
        counts.columns = ["Category", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                counts,
                x="Category",
                y="Count",
                text_auto=True,
                color="Category",
                title="Complaint Volume by Category"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.pie(
                counts,
                names="Category",
                values="Count",
                hole=0.4,
                title="Proportion of Complaints"
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------
# TAB 3 — DOWNLOAD
# --------------------------------------------------------
with tabs[2]:

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:
        df = st.session_state["df"]
        csv = df.to_csv(index=False)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Download Classified Results")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="classified_complaints.csv",
            mime="text/csv"
        )
        st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import base64

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------
st.set_page_config(
    page_title="Banking Complaint Intelligence Dashboard",
    page_icon="💼",
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

    /* Upload Card */
    .upload-card {
        padding: 25px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    }

    /* Section Card */
    .section-card {
        padding: 20px;
        background: white;
        border-radius: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 18px rgba(0,0,0,0.06);
    }

    .big-title {
        font-size: 34px !important;
        font-weight: 900 !important;
        color: #002f5e !important;
    }

    .sub-title {
        font-size: 18px; 
        color: #315a89;
        margin-bottom: 8px;
    }

    /* Buttons */
    .stButton > button {
        background-color: #003d79;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.4rem;
        font-size: 16px;
        font-weight: 600;
        border: none;
    }
    .stButton > button:hover {
        background-color: #002f5e;
        color: #ffffff;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        font-weight: 600;
        padding: 8px 20px;
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

# --------------------------------------------------------
# Prediction Function
# --------------------------------------------------------
def predict_category(text):
    pred = pipeline.predict([str(text)])[0]
    return id2label[pred]

# --------------------------------------------------------
# Header Section
# --------------------------------------------------------
st.markdown("""
<div style='padding: 20px 10px; text-align: center;'>
    <h1 class='big-title'>🏦 Banking Complaint Intelligence Dashboard</h1>
    <p class='sub-title'>Upload customer complaints, classify automatically, and view AI-powered analytics.</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# Tabs: Upload | Insights | Word Cloud | Download
# --------------------------------------------------------
tabs = st.tabs(["📁 Upload Data", "📊 Insights", "☁️ Word Cloud", "⬇️ Export"])

with tabs[0]:

    st.markdown("<div class='upload-card'>", unsafe_allow_html=True)

    st.subheader("📥 Upload Complaint File (CSV or Excel)")

    uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx"], label_visibility="collapsed")

    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded_file:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        if "complaint_text" not in df.columns:
            st.error("❌ Missing column: 'complaint_text'")
        else:
            st.success("✅ File uploaded successfully!")
            st.write("### 📄 Preview")
            st.dataframe(df.head(), use_container_width=True)

            # Classify
            st.write("### 🔍 Running Classification...")
            df["predicted_category"] = df["complaint_text"].apply(predict_category)
            st.success("✅ Classification completed!")

            st.session_state["df"] = df  # Save session data


# --------------------------------------------------------
# Insights TAB
# --------------------------------------------------------
with tabs[1]:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("📊 Complaint Category Distribution")

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:
        df = st.session_state["df"]

        counts = df["predicted_category"].value_counts().reset_index()
        counts.columns = ["Category", "Count"]

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                counts, x="Category", y="Count",
                title="Category-wise Complaint Volume",
                text_auto=True, color="Category"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig2 = px.pie(
                counts,
                names="Category",
                values="Count",
                hole=0.45,
                title="Proportion of Complaints"
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------
# Word Cloud TAB
# --------------------------------------------------------
with tabs[2]:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("☁️ Category-wise Keyword Cloud")

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:
        df = st.session_state["df"]
        categories = df["predicted_category"].unique().tolist()

        selected = st.selectbox("Choose category", categories)

        cat_text = " ".join(df[df["predicted_category"] == selected]["complaint_text"].astype(str))

        wc = WordCloud(width=1000, height=400, background_color="white").generate(cat_text)

        fig_wc, ax = plt.subplots(figsize=(12, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig_wc)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------------
# Export TAB
# --------------------------------------------------------
with tabs[3]:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("⬇️ Download Results")

    if "df" not in st.session_state:
        st.info("Upload a file first.")
    else:
        df = st.session_state["df"]
        csv = df.to_csv(index=False)

        st.download_button(
            label="⬇️ Download Classified CSV",
            data=csv,
            file_name="classified_complaints.csv",
            mime="text/csv",
        )

    st.markdown("</div>", unsafe_allow_html=True)

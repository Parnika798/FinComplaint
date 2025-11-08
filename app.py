import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# --------------------------------------------------------
# Load CSS
# --------------------------------------------------------
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------
st.set_page_config(
    page_title="Financial Complaint Analytics Dashboard",
    layout="wide"
)

# --------------------------------------------------------
# Load Pipeline + Label Encoder
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
    pred_class = pipeline.predict([str(text)])[0]
    return id2label[pred_class]

# --------------------------------------------------------
# UI Layout
# --------------------------------------------------------
st.title("📊 Financial Complaint Intelligence Dashboard")
st.write("A smart, interactive analytics tool for banks to analyze complaint patterns, detect issues, and generate insights.")

st.markdown("---")

uploaded = st.file_uploader("📁 Upload Complaint CSV/Excel File", type=["csv", "xlsx"])

if uploaded:

    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    if "complaint_text" not in df.columns:
        st.error("❌ Please ensure your file contains a column named `complaint_text`.")
        st.stop()

    st.success("✅ File uploaded successfully!")

    st.subheader("📄 Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # ----------------------------------------------------
    # Classification
    # ----------------------------------------------------
    st.subheader("🔍 Running Classification")

    df["predicted_category"] = df["complaint_text"].apply(predict_category)

    st.success("✅ Classification completed!")

    st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------
    # Analytics Section
    # ----------------------------------------------------
    st.header("📈 Complaint Distribution Analytics")

    counts = df["predicted_category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]

    col1, col2 = st.columns(2)

    # Bar Chart
    with col1:
        fig1 = px.bar(
            counts, x="Category", y="Count",
            title="Category-wise Complaint Count",
            text_auto=True, color="Category"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Pie Chart
    with col2:
        fig2 = px.pie(
            counts,
            names="Category",
            values="Count",
            title="Category Proportion"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ----------------------------------------------------
    # Keyword Cloud Section
    # ----------------------------------------------------
    st.header("☁️ Keyword Cloud")

    selected_category = st.selectbox(
        "Select a category to view its word cloud:",
        options=counts["Category"].tolist()
    )

    cat_text = " ".join(
        df[df["predicted_category"] == selected_category]["complaint_text"].astype(str)
    )

    if len(cat_text.strip()) > 0:
        wc = WordCloud(width=800, height=400, background_color="white").generate(cat_text)

        fig_wc, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")

        st.pyplot(fig_wc)

    st.markdown("---")

    # ----------------------------------------------------
    # Download Button
    # ----------------------------------------------------
    st.header("📥 Download Classified Results")

    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name="classified_complaints.csv",
        mime="text/csv"
    )

    st.success("✅ Report is ready!")

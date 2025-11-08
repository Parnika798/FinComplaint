import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib

# --------------------------------------------------------
# Page Config
# --------------------------------------------------------
st.set_page_config(
    page_title="Banking Complaint Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------------
# Enhanced Custom CSS
# --------------------------------------------------------
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Global Reset */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a365d 0%, #2d5a8f 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .sidebar-content {
        padding: 2rem 1rem;
    }

    /* Sidebar Logo/Title */
    .sidebar-logo {
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
        margin-bottom: 2rem;
        padding: 0 1rem;
        letter-spacing: -0.5px;
        text-align: center;
    }

    .sidebar-logo-sub {
        font-size: 12px;
        font-weight: 500;
        color: #94a9c9;
        text-align: center;
        margin-top: -1rem;
        margin-bottom: 2rem;
    }

    /* Sidebar Radio Buttons */
    [data-testid="stSidebar"] .stRadio > label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 1rem;
    }

    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem;
    }

    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
        background: rgba(255, 255, 255, 0.08) !important;
        padding: 0.75rem 1.25rem !important;
        border-radius: 10px !important;
        margin: 0.25rem 0 !important;
        transition: all 0.2s ease !important;
        border: 1px solid transparent !important;
    }

    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    [data-testid="stSidebar"] .stRadio label[data-baseweb="radio"][data-checked="true"] {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] .stRadio label span {
        color: #ffffff !important;
    }

    /* Main Content Container */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px !important;
    }

    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(30, 58, 138, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .header-title {
        font-size: 36px;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        letter-spacing: -1px;
    }

    .header-subtitle {
        font-size: 16px;
        color: #bfdbfe;
        margin-top: 0.5rem;
        font-weight: 500;
    }

    /* Card Styling */
    .metric-card {
        background: white;
        padding: 1.75rem;
        border-radius: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        height: 100%;
    }

    .metric-card:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
    }

    .metric-value {
        font-size: 42px;
        font-weight: 900;
        color: #1e3a8a;
        line-height: 1;
        margin-bottom: 0.5rem;
    }

    .metric-label {
        font-size: 14px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Content Cards */
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid #e5e7eb;
        margin-bottom: 1.5rem;
    }

    /* Upload Box */
    .upload-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 2px dashed #3b82f6;
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-container:hover {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        border-color: #2563eb;
    }

    .upload-icon {
        font-size: 48px;
        color: #3b82f6;
        margin-bottom: 1rem;
    }

    .upload-text {
        font-size: 18px;
        font-weight: 600;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }

    .upload-subtext {
        font-size: 14px;
        color: #6b7280;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
    }

    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
        color: white !important;
        padding: 0.75rem 2rem !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border-radius: 10px !important;
        border: none !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3) !important;
    }

    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #047857 0%, #065f46 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4) !important;
    }

    /* Dataframe Styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    /* Section Headers */
    h2, h3 {
        color: #1e3a8a !important;
        font-weight: 800 !important;
        margin-bottom: 1.5rem !important;
    }

    /* Success/Error Messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 10px !important;
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: transparent !important;
    }

    [data-testid="stFileUploader"] section {
        border: none !important;
        background: transparent !important;
    }

    /* Plotly Charts */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Divider */
    hr {
        margin: 2rem 0 !important;
        border-color: #e5e7eb !important;
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
    try:
        pipeline = joblib.load("model/clf_pipeline1.pkl")
        label_encoder = joblib.load("model/label_encoder1.pkl")
        id2label = {i: label for i, label in enumerate(label_encoder.classes_)}
        return pipeline, label_encoder, id2label
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None, None

pipeline, label_encoder, id2label = load_components()

def predict_category(text):
    if pipeline and id2label:
        pred = pipeline.predict([str(text)])[0]
        return id2label[pred]
    return "Unknown"

# --------------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🏦 Complaint AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-logo-sub">Intelligent Analysis Platform</div>', unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        ["📤 Upload Data", "📊 Insights", "💾 Download"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Enterprise-grade AI-powered complaint classification and analytics dashboard.")

# --------------------------------------------------------
# Header Banner
# --------------------------------------------------------
st.markdown("""
<div class="header-banner">
    <div class="header-title">Banking Complaint Intelligence Dashboard</div>
    <div class="header-subtitle">AI-Powered Customer Grievance Analysis & Classification System</div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------------
# PAGE LOGIC
# --------------------------------------------------------

if page == "📤 Upload Data":
    
    st.markdown('<div class="content-card">', unsafe_allow_html=True)
    st.markdown("### 📁 Upload Complaint Data")
    st.markdown("Upload your CSV or Excel file containing customer complaints for automated classification.")
    
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    st.markdown('<div class="upload-icon">📄</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-text">Drag and drop or click to browse</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-subtext">Supported formats: CSV, XLSX</div>', unsafe_allow_html=True)
    
    file = st.file_uploader("", type=["csv", "xlsx"], label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if file:
        with st.spinner("Processing your file..."):
            try:
                # Read file
                df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
                
                # Validate column
                if "complaint_text" not in df.columns:
                    st.error("❌ Missing required column: 'complaint_text'")
                else:
                    # Predict categories
                    df["predicted_category"] = df["complaint_text"].apply(predict_category)
                    st.session_state["df"] = df
                    
                    st.success(f"✅ Successfully processed {len(df)} complaints!")
                    
                    # Preview
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    st.markdown("### 👁️ Data Preview")
                    st.dataframe(df.head(10), use_container_width=True, height=400)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")


elif page == "📊 Insights":
    
    if "df" not in st.session_state:
        st.info("⚠️ Please upload a complaint file first from the 'Upload Data' page.")
    else:
        df = st.session_state["df"]
        
        # KPI Metrics
        st.markdown("### 📈 Key Performance Indicators")
        
        total_complaints = len(df)
        category_counts = df["predicted_category"].value_counts()
        top_category = category_counts.idxmax()
        top_category_count = category_counts.iloc[0]
        unique_categories = df["predicted_category"].nunique()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_complaints:,}</div>
                <div class="metric-label">Total Complaints</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{top_category_count}</div>
                <div class="metric-label">{top_category}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{unique_categories}</div>
                <div class="metric-label">Unique Categories</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Visualizations
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📊 Category Distribution Analysis")
        
        counts = df["predicted_category"].value_counts().reset_index()
        counts.columns = ["Category", "Count"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar Chart
            fig_bar = px.bar(
                counts, 
                x="Category", 
                y="Count", 
                color="Category",
                title="Complaints by Category",
                text_auto=True,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_bar.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                font=dict(family="Inter, sans-serif"),
                title_font_size=18,
                title_font_weight=700
            )
            fig_bar.update_traces(textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Pie Chart
            fig_pie = px.pie(
                counts, 
                names="Category", 
                values="Count",
                title="Category Proportion",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig_pie.update_layout(
                font=dict(family="Inter, sans-serif"),
                title_font_size=18,
                title_font_weight=700
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Table
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Detailed Breakdown")
        
        summary_df = counts.copy()
        summary_df['Percentage'] = (summary_df['Count'] / summary_df['Count'].sum() * 100).round(2)
        summary_df['Percentage'] = summary_df['Percentage'].astype(str) + '%'
        
        st.dataframe(summary_df, use_container_width=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)


elif page == "💾 Download":
    
    if "df" not in st.session_state:
        st.info("⚠️ Please upload and process a complaint file first.")
    else:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 💾 Export Classified Data")
        st.markdown("Download your processed complaint data with AI-generated classifications.")
        
        df = st.session_state["df"]
        
        # Summary before download
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **Ready to download:**
            - Total records: **{len(df):,}**
            - Categories identified: **{df['predicted_category'].nunique()}**
            - File format: **CSV**
            """)
        
        with col2:
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="classified_complaints.csv",
                mime="text/csv"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Preview
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 👁️ Final Data Preview")
        st.dataframe(df, use_container_width=True, height=400)
        st.markdown('</div>', unsafe_allow_html=True)

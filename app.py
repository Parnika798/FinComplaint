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
    st.markdown(c


import streamlit as st
from streamlit_option_menu import option_menu
import requests
import time

# --- PAGE CONFIG ---
st.set_page_config(page_title="Veritas AI | News Verification", layout="wide")

# --- CUSTOM MODERN CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(180deg, #020617 0%, #0f172a 100%) !important;
    }

    /* Sidebar Transparency (High) */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.05) !important; 
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }

    /* CHANGE: SIDEBAR BUTTON TEXT TO BLACK */
    section[data-testid="stSidebar"] .nav-link span {
        color: black !important;
        font-weight: bold !important;
    }
    
    /* Ensure the sidebar title remains white for contrast */
    section[data-testid="stSidebar"] h2 {
        color: white !important;
    }

    /* GLOBAL TEXT COLOR (Database & Settings Pages) */
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp span {
        color: white !important;
    }

    /* BUTTON TEXT TO BLACK (Main Page) */
    div.stButton > button p {
        color: black !important;
        font-weight: bold !important;
    }
    
    div.stButton > button {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: none !important;
    }

    /* SELECTBOX (MODEL CHOOSER) TEXT TO BLACK */
    div[data-baseweb="select"] * {
        color: black !important;
    }
    
    div[data-baseweb="select"] {
        background-color: white !important;
        border-radius: 10px !important;
    }

    .stTextArea textarea {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 15px !important;
    }

    /* Glass Box Container for Results */
    .glass-box {
        background: rgba(255, 255, 255, 0.05);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-top: 25px;
        color: white;
    }

    .fake-label { color: #ff4b4b; font-weight: bold; font-size: 28px; }
    .real-label { color: #00ff88; font-weight: bold; font-size: 28px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🛡️ VERITAS AI</h2>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Analyzer", "Database", "Settings"],
        icons=["shield-check", "database", "gear"],
        menu_icon="broadcast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "rgba(255, 255, 255, 0.8)"}, # Lightened container for black text
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin":"5px", 
            },
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white !important"},
        }
    )

# --- NAVIGATION LOGIC ---
if selected == "Analyzer":
    st.title("News Verification Engine")
    st.markdown("Analyze news articles with high-precision Deep Learning.")
    
    news_text = st.text_area("Paste the news article text here:", height=250, placeholder="In a shocking turn of events...")
    
    if st.button("🚀 RUN DEEP SCAN", use_container_width=True):
        if news_text:
            with st.spinner("Neural networks analyzing patterns..."):
                try:
                    response = requests.post("http://127.0.0.1:8000/analyze", json={"text": news_text})
                    data = response.json()
                    
                    label = data.get("label", "FAKE").upper()
                    score = data.get("confidence", 0.0)

                    st.markdown(f"""
                    <div class="glass-box">
                        <h3 style='color: white; margin-top: 0;'>Scan Results</h3>
                        <hr style='border: 0.5px solid rgba(255,255,255,0.1);'>
                        <div style='display: flex; justify-content: space-around; align-items: center;'>
                            <div style='text-align: center;'>
                                <p style='margin-bottom: 0; color: white;'>AUTHENTICITY VERDICT</p>
                                <p class="{'real-label' if label == 'REAL' else 'fake-label'}">{label}</p>
                            </div>
                            <div style='text-align: center; width: 40%;'>
                                <p style='margin-bottom: 5px; color: white;'>CONFIDENCE SCORE</p>
                                <h2 style='color: white; margin: 0;'>{score*100:.1f}%</h2>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.progress(score)
                    
                except Exception as e:
                    st.error(f"Connection Failed: Ensure main.py is running. Error: {e}")
        else:
            st.warning("Please enter text for analysis.")

elif selected == "Database":
    st.title("🗄️ Cloud Database")
    st.markdown("### Pinecone Index Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Vectors", "1,248")
    with col2:
        st.metric("Uptime", "99.9%")
    st.info("The Database page is now correctly isolated from the Analyzer.")

elif selected == "Settings":
    st.title("⚙️ System Settings")
    st.checkbox("Enable Real-time Web Scraping")
    st.checkbox("High-Precision Mode (Longformer)")
    st.selectbox("Inference Engine", ["BERT-Tiny", "RoBERTa", "Longformer"])
    st.success("Settings saved locally.")
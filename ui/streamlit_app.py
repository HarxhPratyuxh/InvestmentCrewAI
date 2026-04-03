import sys
import os
import threading

# Reconfigure stdout to utf-8 for Windows emoji support
if sys.stdout and getattr(sys.stdout, 'encoding', '').lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import streamlit as st
from streamlit.runtime.scriptrunner import get_script_run_ctx, add_script_run_ctx
import asyncio
from dotenv import load_dotenv

# Add the project root to python path so we can import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables before importing CrewAI to configure telemetry
load_dotenv()

from services.analysis_service import AnalysisService
from models.analysis import InvestmentRecommendation

st.set_page_config(
    page_title="AI Investment Advisor",
    page_icon="📈",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4221/4221419.png", width=80)
    st.title("Configuration")
    
    risk_profile = st.selectbox(
        "Risk Profile",
        ["Conservative", "Moderate", "Aggressive"],
        index=1,
        help="Determines the risk tolerance for the investment advice."
    )
    
    st.info(
        "**Conservative**: Focus on stability and dividends.\n"
        "**Moderate**: Balanced growth and safety.\n"
        "**Aggressive**: High growth potential, higher volatility."
    )

# --- Main Content ---
st.title("📈 AI Investment Advisor")
st.markdown("Enter a stock symbol to generate a comprehensive, multi-agent investment report.")

col1, col2 = st.columns([3, 1])
with col1:
    stock_symbol = st.text_input("Stock Symbol", value="RELIANCE.NS", placeholder="e.g., AAPL, TSLA, RELIANCE.NS")
with col2:
    st.write("") # Spacer
    st.write("") # Spacer
    analyze_btn = st.button("Analyze Stock")

# --- Agent Logs Container ---
with st.expander("🕵️ Agent Activity Logs", expanded=True):
    log_container = st.empty()
    logs = []

# Save the context to a local variable so the closure can capture it and provide it to bg threads
current_ctx = get_script_run_ctx()

def stream_callback(step_output):
    """Callback function to update the UI with agent thoughts."""
    try:
        # Check if context exists; if not, add the main thread's context captured from the outer scope
        ctx = get_script_run_ctx()
        if not ctx and current_ctx:
            add_script_run_ctx(threading.current_thread(), current_ctx)
            
        thought = getattr(step_output, 'thought', str(step_output))
        if thought:
            logs.append(f"**🤖 Agent**: {thought}")
            log_container.markdown("\n\n".join(logs[-3:])) # Show last 3 logs
    except Exception as e:
        print(f"Error in stream_callback: {e}")

# --- Execution Logic ---
if analyze_btn:
    if not stock_symbol:
        st.warning("Please enter a stock symbol.")
    else:
        service = AnalysisService(step_callback=stream_callback)
        
        with st.spinner(f"🤖 Agents are researching {stock_symbol}... this may take 2-3 minutes."):
            try:
                # Run the analysis
                # We use a synchronous call here because Streamlit handles threading for us
                result = service.run_analysis(stock_symbol, risk_profile)
                
                if isinstance(result, InvestmentRecommendation):
                    st.success("Analysis Complete!")
                    
                    # Render the Report
                    st.markdown("---")
                    
                    # 1. High Level Metrics
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("Recommendation", result.recommendation)
                    m2.metric("Target Price", f"${result.target_price:.2f}")
                    m3.metric("Current Price", f"${result.current_price:.2f}")
                    m4.metric("Confidence", f"{result.confidence_score}%")
                    
                    # 2. Detailed Markdown Report
                    st.markdown(result.to_markdown())
                    
                else:
                    st.error("Failed to generate structured report. Raw output:")
                    st.write(result)
                    
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
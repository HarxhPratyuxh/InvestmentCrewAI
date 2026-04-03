# 📈 AI Multi-Agent Investment Advisor

<p align="center">
  <img src="InvestmentCrewAIDemo.gif" alt="Investment Crew AI Demo" width="800">
</p>


<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/CrewAI-Orchestration-orange.svg" alt="CrewAI">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-UI-red.svg" alt="Streamlit">
</p>

An intelligent, multi-agent financial analysis architecture that leverages **CrewAI** to orchestrate a team of LLM-powered personas. These agents autonomously gather live market fundamentals, calculate technical indicators, scrape the latest news sentiment, and collaboratively synthesize a deeply researched investment recommendation.

## ✨ High-Level Architecture
- **Asynchronous Data Gathering**: Utilizes multi-threading to deploy the "News Researcher" and "Data Explorer" agents simultaneously, cutting execution time in half.
- **Dynamic Provider Routing**: Circumvents API rate limits by intelligently distributing workloads across different LLM providers on a *per-agent basis* (e.g., Groq for rapid data retrieval, Google Gemini for deep summarization).
- **Streamlit Callbacks**: Injects thread-safe `ScriptRunContext` across parallel workers to stream terminal outputs fluidly back into the Streamlit UI in real-time.
- **Strict Pydantic Enforcement**: Guarantees perfectly structured output logic using CrewAI's structured parsing mechanisms, falling back to custom JSON marshalling when needed.

## 🚀 Key Features

*   **Multi-Agent Research**: 4 Autonomous agents specialized in Fundamental Data, Technical Analysis, and Macro News.
*   **Dual Interface**: Fully functional REST API backend alongside an interactive Web UI dashboard.
*   **API-Independent Smart Stock Lookup**: Automatically resolves vague inputs (e.g. "Apple" or "Microsoft") into explicit Ticker symbols via native Yahoo Finance backend queries.
*   **Model Agnostic**: Run on OpenAI, Gemini, Groq, or OpenRouter via a unified `.env` configuration.

## 🛠️ Installation & Setup

1.  **Clone & Initialize Virtual Environment**:
    ```bash
    python -m venv venv
    venv\Scripts\activate   # Windows
    source venv/bin/activate # Mac/Linux
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    *   Duplicate `.env.example` to `.env`.
    *   Populate your API keys.

## 🏃‍♂️ Usage

### Option 1: Web Dashboard (Recommended)
Run the interactive Streamlit application to visualize agent thought processes in real-time.
```bash
streamlit run ui/streamlit_app.py
```

### Option 2: Command Line Interface
Execute a quick query passing args directly into the CLI orchestrator.
```bash
python main.py --stock AAPL --risk Aggressive
```

### Option 3: API Server
Start the headless FastAPI server to accept POST requests and integrate with other apps.
```bash
uvicorn api_server:app --reload
```

## 📂 Project Structure

*   `agents/`: Custom persona definitions (Backstories, Goals, Roles).
*   `tasks/`: Structured sub-tasks mapping tools to Agents.
*   `tools/`: Custom wrappers relying on `yFinance` and `Exa Search`.
*   `ui/`: Frontend reactive Streamlit codebase.
*   `models/`: Pydantic schemas validating AI outputs.
*   `services/`: Core logic and ThreadPool orchestrators.
*   `config/`: Advanced, generic LLM routing logic mapping env vars dynamically.

---
*Built as a showcase for multi-agent LLM orchestration, concurrent execution, and robust error handling.*
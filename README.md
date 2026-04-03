# 📈 AI Investment Advisor | Multi-Agent Financial Analysis System

<p align="center">
  <img src="InvestmentCrewAIDemo.gif" alt="Investment Crew AI Demo" width="800">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/CrewAI-Orchestration-orange.svg" alt="CrewAI">
  <img src="https://img.shields.io/badge/FastAPI-Backend-green.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/Streamlit-UI-red.svg" alt="Streamlit">
  <img src="https://img.shields.io/badge/LLM-Gemini_|_Groq-blueviolet.svg" alt="LLMs">
</p>

A production-grade multi-agent investment analysis system leveraging **CrewAI** to automate deep stock research and generate structured investment reports. This architecture orchestrates a team of specialized AI personas that autonomously gather live market fundamentals, calculate technical indicators, scrape the latest news sentiment, and collaboratively synthesize actionable financial strategies.

Built to showcase modern **Agentic AI workflows**, reliable output generation, and robust LLM orchestration. 

## ✨ Key Achievements & Features

* **Multi-Agent Orchestration**: Designed specialized agents (**Researchers**, **Analyst**, and **Strategist**) that seamlessly collaborate to perform fundamental, technical, and macroeconomic sentiment analysis using real-time financial data APIs (`Exa AI`, `yFinance`).
* **Parallel Execution Pipelines**: Implemented multi-threaded execution pipelines (`ThreadPoolExecutor`) for concurrent data collection and news scraping tasks, significantly reducing report generation latency and speeding up overall AI analysis.
* **Real-time Reasoning Dashboard**: Developed an interactive **Streamlit dashboard** equipped with complex callback managers that stream agent thought-processes and reasoning to the UI in real-time.
* **Structured Data Generation**: Guaranteed consistent, production-ready outputs by enforcing strict **Pydantic schemas** and falling back to automated JSON parsing loops, ensuring that final investment recommendations are fully structural and actionable.
* **Dual Interface Support**: Complete flexibility with an interactive web UI alongside a headless **FastAPI backend** capable of real-time streaming to downstream applications.
* **Dynamic LLM Provider Routing**: API-agnostic architecture allowing workloads to be intelligently distributed across different LLM providers (e.g., Groq for rapid data retrieval, Google Gemini for deep summarization) on a *per-agent basis*.

## 🛠️ Tech Stack

* **Language:** Python
* **AI & Orchestration:** CrewAI, LangChain, Pydantic
* **Models & Search:** Google Gemini, Groq, Exa AI Search API
* **Data Connectors:** yFinance
* **Frontend:** Streamlit
* **Backend Server:** FastAPI, Uvicorn

## 🚀 Installation & Setup

1. **Clone & Initialize Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate # Mac/Linux
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   * Duplicate `.env.example` to `.env`.
   * Populate your required API keys (e.g., `GEMINI_API_KEY`, `GROQ_API_KEY`, `EXA_API_KEY`).

## 🏃‍♂️ Usage

### Option 1: Web Dashboard (Recommended)
Run the interactive Streamlit application to visualize agent thought processes in real-time.
```bash
streamlit run ui/streamlit_app.py
```

### Option 2: Command Line Interface
Execute a quick automated task directly via the CLI orchestrator.
```bash
python main.py --stock AAPL --risk Aggressive
```

### Option 3: REST API Server
Start the headless FastAPI server to accept HTTP requests for backend integration.
```bash
uvicorn api_server:app --reload
```

## 📂 Architecture Structure

* `agents/`: Intelligent persona definitions (Data/News Researchers, Data Analyst, Financial Expert).
* `tasks/`: Structured CrewAI sub-tasks mapping specific tools to the appropriate Agents.
* `tools/`: Custom external interfaces wrapping `yFinance` API and `Exa Search`.
* `ui/`: Frontend reactive Streamlit codebase containing thread-safe UI stream callbacks.
* `services/`: Core logic and `ThreadPool` orchestrators governing the concurrent Crew execution.
* `models/`: Strict Pydantic schemas validating AI outputs (e.g., `InvestmentRecommendation`).
* `config/`: Dynamic LLM routing logic mapping environmental variables across different agents.

---
*Built as a showcase for production-grade multi-agent LLM orchestration, concurrent execution, and robust error handling.*
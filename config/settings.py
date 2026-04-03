import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "investment_history.db"

# Create directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Risk Profile Allocations (Percentage of portfolio)
MAX_ALLOCATION = {
    "Conservative": 0.05,  # 5%
    "Moderate": 0.10,      # 10%
    "Aggressive": 0.20     # 20%
}

# Rate Limiting (Requests per minute)
RATE_LIMITS = {
    "yfinance": 10,
    "exa": 15
}
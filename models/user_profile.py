from enum import Enum
from pydantic import BaseModel

class RiskLevel(str, Enum):
    CONSERVATIVE = "Conservative"
    MODERATE = "Moderate"
    AGGRESSIVE = "Aggressive"

class UserProfile(BaseModel):
    risk_level: RiskLevel
    investment_horizon: str = "Long Term"  # Short, Medium, Long
    capital: float = 10000.0
    currency: str = "USD"
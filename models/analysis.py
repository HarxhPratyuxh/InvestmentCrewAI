from typing import List, Optional
from pydantic import BaseModel, Field

class FinancialMetric(BaseModel):
    metric: str
    value: str
    sentiment: str = Field(description="Positive, Negative, or Neutral")

class NewsSummary(BaseModel):
    headline: str
    source: str
    sentiment_score: float = Field(description="Score between -1 (Negative) and 1 (Positive)")
    url: Optional[str] = None

class TechnicalSignal(BaseModel):
    indicator: str
    signal: str = Field(description="Buy, Sell, or Neutral")
    value: str

class InvestmentRecommendation(BaseModel):
    stock_symbol: str
    current_price: float
    target_price: float
    recommendation: str = Field(description="Strong Buy, Buy, Hold, Sell, Strong Sell")
    risk_level: str = Field(description="Low, Medium, High, Very High")
    confidence_score: float = Field(description="0 to 100")
    
    one_liner: str = Field(description="A punchy, one-sentence summary of the verdict")
    key_reasons: List[str]
    
    fundamental_analysis: List[FinancialMetric]
    technical_analysis: List[TechnicalSignal]
    recent_news: List[NewsSummary]
    
    def to_markdown(self) -> str:
        """Renders the recommendation as a beautiful Markdown report."""
        
        # Color coding for recommendation
        rec_emoji = {
            "Strong Buy": "🚀", "Buy": "✅", "Hold": "✋", 
            "Sell": "🔻", "Strong Sell": "🚨"
        }.get(self.recommendation, "ℹ️")

        md = f"""
# {rec_emoji} Investment Recommendation: {self.stock_symbol}

**Verdict**: {self.recommendation.upper()}  
**Confidence**: {self.confidence_score}/100  
**Target Price**: ${self.target_price:.2f} (Current: ${self.current_price:.2f})  
**Risk Level**: {self.risk_level}

> **"{self.one_liner}"**

## 🔑 Key Reasons
"""
        for reason in self.key_reasons:
            md += f"- {reason}\n"

        md += "\n## 📊 Fundamental Analysis\n| Metric | Value | Sentiment |\n|---|---|---|\n"
        for item in self.fundamental_analysis:
            icon = "🟢" if item.sentiment == "Positive" else "🔴" if item.sentiment == "Negative" else "⚪"
            md += f"| {item.metric} | {item.value} | {icon} {item.sentiment} |\n"

        md += "\n## 📈 Technical Signals\n| Indicator | Value | Signal |\n|---|---|---|\n"
        for item in self.technical_analysis:
            icon = "🟢" if item.signal == "Buy" else "🔴" if item.signal == "Sell" else "⚪"
            md += f"| {item.indicator} | {item.value} | {icon} {item.signal} |\n"

        md += "\n## 📰 Recent News & Sentiment\n"
        for news in self.recent_news:
            md += f"- **[{news.headline}]({news.url or '#'})** ({news.source}) - Sentiment: {news.sentiment_score}\n"
            
        return md
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional, Dict, Any

from crewai import Crew, Process
from agents import analyst, data_explorer, fin_expert, news_info_explorer
from tasks import advise, analyse, get_company_financials, get_company_news
import json
from models.analysis import InvestmentRecommendation

class AnalysisService:
    def __init__(self, step_callback: Optional[Callable] = None):
        self.step_callback = step_callback

    def _create_crew(self, agents, tasks, process=Process.sequential):
        return Crew(
            agents=agents,
            tasks=tasks,
            verbose=True,
            process=process,
            step_callback=self.step_callback,
        )

    def run_analysis(self, stock_symbol: str, risk_profile: str = "Moderate") -> InvestmentRecommendation:
        """
        Orchestrates the multi-agent analysis pipeline.
        Uses parallel execution for data gathering and sequential for analysis.
        """
        inputs = {"stock": stock_symbol, "risk_profile": risk_profile}
        
        # 1. Define Crews
        # Data Gathering Crew (Financials)
        financial_crew = self._create_crew(
            agents=[data_explorer],
            tasks=[get_company_financials]
        )
        
        # News Gathering Crew
        news_crew = self._create_crew(
            agents=[news_info_explorer],
            tasks=[get_company_news]
        )
        
        # Analysis & Recommendation Crew
        analysis_crew = self._create_crew(
            agents=[analyst, fin_expert],
            tasks=[analyse, advise]
        )

        # 2. Execute Phase 1 (Parallel Data Gathering)
        print(f"[*] Starting analysis for {stock_symbol}...")
        
        # We use a ThreadPool to run the two gathering crews simultaneously
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_fin = executor.submit(financial_crew.kickoff, inputs=inputs)
            future_news = executor.submit(news_crew.kickoff, inputs=inputs)
            
            # Wait for results (blocking)
            fin_result = future_fin.result()
            news_result = future_news.result()

        print("[OK] Phase 1 (Data Gathering) Complete.")

        # 3. Execute Phase 2 (Analysis & Recommendation)
        # The context is automatically handled by CrewAI via the Task context mechanism,
        # but we pass the inputs again to ensure consistency.
        result = analysis_crew.kickoff(inputs=inputs)
        
        print("[OK] Phase 2 (Analysis) Complete.")

        # 4. Return Structured Output
        # Since we used output_pydantic in the final task, 'result' should be the Pydantic model.
        # However, CrewAI sometimes returns a CrewOutput object wrapping the Pydantic model.
        
        if hasattr(result, 'pydantic') and result.pydantic:
            return result.pydantic
        elif isinstance(result, InvestmentRecommendation):
            return result
        
        # Fallback if something went wrong with Pydantic parsing
        # This usually happens if the LLM failed to adhere to the schema strictly
        raw_output = getattr(result, "raw", str(result))
        try:
            # Try parsing the raw output as json
            import re
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group())
                parsed = InvestmentRecommendation(**json_data)
                print("[*] Successfully parsed raw LLM JSON output to Pydantic model as fallback.")
                return parsed
        except Exception as e:
            print(f"[-] Fallback JSON parsing failed: {e}")
            
        print("[!] Warning: Output was not strictly Pydantic. Returning raw.")
        return result

    async def run_analysis_async(self, stock_symbol: str, risk_profile: str):
        """Async wrapper for the analysis."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None, 
            self.run_analysis, 
            stock_symbol, 
            risk_profile
        )
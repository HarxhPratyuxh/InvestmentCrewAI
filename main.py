import argparse
import os
import time
from services.analysis_service import AnalysisService
from models.analysis import InvestmentRecommendation

os.environ["CREWAI_STORAGE_DIR"] = os.path.join(os.getcwd(), "crewai_memory")

def main():
    """Main function to run the financial analysis with configurable execution mode."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Financial Analysis with Configurable Execution Mode"
    )
    parser.add_argument(
        "--stock",
        default="RELIANCE",
        help="Stock symbol to analyze (default: RELIANCE)",
    )

    args = parser.parse_args()

    # Record start time
    start_time = time.time()

    # Scenario: Analyze specified stock
    print(f"\n📋 Stock Analysis: {args.stock}")
    
    # Initialize Service
    service = AnalysisService()
    
    # Run Analysis
    result = service.run_analysis(args.stock, risk_profile="Moderate")

    end_time = time.time()
    execution_time = end_time - start_time

    print("\n🎉 Financial analysis completed!")
    print(f"⏱️  Total execution time: {execution_time:.2f} seconds")
    
    if isinstance(result, InvestmentRecommendation):
        print("\n" + result.to_markdown())
    else:
        print("\n" + str(result))


if __name__ == "__main__":
    main()

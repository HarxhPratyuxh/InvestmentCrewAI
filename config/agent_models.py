import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

def get_llm_for_agent(agent_role: str = None) -> LLM:
    """
    Returns the appropriate LLM configuration based on environment variables.
    Supports a DISTRIBUTED strategy to load balance across free tiers.
    """
    # Format the role for env var lookup (e.g., "Data Analyst" -> "DATA_ANALYST")
    role_prefix = ""
    if agent_role:
        role_prefix = agent_role.upper().replace(" ", "_") + "_"
        
    provider = os.getenv(f"{role_prefix}PROVIDER")
    if not provider:
        provider = os.getenv("DEFAULT_LLM_PROVIDER", "openrouter").lower()
    else:
        provider = provider.lower()
    
    # Common configuration
    config = {
        "temperature": 0.7,
        "timeout": 120,
    }

    if provider == "openrouter":
        model_name = os.getenv(f"{role_prefix}MODEL", os.getenv("OPENROUTER_MODEL", "openrouter/meta-llama/llama-3.3-70b-instruct"))
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        return LLM(
            model=model_name,
            api_key=api_key,
            **config
        )
        
    elif provider == "google":
        model_name = os.getenv(f"{role_prefix}MODEL", "gemini/gemini-3.1-flash-lite-preview")
        return LLM(
            model=model_name,
            api_key=os.getenv("GOOGLE_API_KEY"),
            **config
        )
        
    elif provider == "groq":
        model_name = os.getenv(f"{role_prefix}MODEL", "groq/groq/compound-mini")
        return LLM(
            model=model_name,
            api_key=os.getenv("GROQ_API_KEY"),
            **config
        )
        
    else:
        # Default to OpenAI
        model_name = os.getenv(f"{role_prefix}MODEL", "gpt-4o")
        return LLM(
            model=model_name,
            api_key=os.getenv("OPENAI_API_KEY"),
            **config
        )
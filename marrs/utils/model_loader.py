from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from marrs.logger.cloud_logger import CustomLogger
from marrs.exception.custom_exception import CustomException
from marrs.utils.config_loader import load_config
from dotenv import load_dotenv
import sys
import os

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY1")

log = CustomLogger().get_logger(__name__)

config = load_config()

def _validate_env():
    """
    Validate necessary environment variables.
    Ensure API keys exist.
    """
    required_vars=["GOOGLE_API_KEY1","GROQ_API_KEY1"]
    api_keys={key:os.getenv(key) for key in required_vars}
    missing = [k for k, v in api_keys.items() if not v]
    if missing:
        log.error("Missing environment variables", missing_vars=missing)
        raise CustomException("Missing environment variables", sys)
    return api_keys
    
def model_loader():
    """
    Load LLM dynamically based on provider in config.
    """
    api_keys = _validate_env()
    
    llm_block = config["llm"]

    # log.info("Loading LLM...")

    provider_key = os.getenv("LLM_PROVIDER", "google")  # Default google
    if provider_key not in llm_block:
        log.error("LLM provider not found in config", provider_key=provider_key)
        raise ValueError(f"Provider '{provider_key}' not found in config")

    llm_config = llm_block[provider_key]
    provider = llm_config.get("provider")
    model_name = llm_config.get("model_name")
    temperature = llm_config.get("temperature", 0.2)
    max_tokens = llm_config.get("max_output_tokens", 2048)
    
    # log.info("Loading LLM", provider=provider, model=model_name, temperature=temperature, max_tokens=max_tokens)

    if provider == "google":
        llm=ChatGoogleGenerativeAI(
            model=model_name,
            temperature=temperature,
            api_key=api_keys["GOOGLE_API_KEY1"],
            max_output_tokens=max_tokens
        )
        return llm

    elif provider == "groq":
        llm=ChatGroq(
            model=model_name,
            api_key=api_keys["GROQ_API_KEY1"], #type: ignore
            temperature=temperature,
        )
        return llm
        
    else:
        log.error("Unsupported LLM provider", provider=provider)
        raise CustomException(f"Unsupported LLM provider: {provider}", sys)

if __name__ == "__main__":
    # llm = load_llm()
    # llm.invoke("hi")
    api_keys = _validate_env()
    print(api_keys["GOOGLE_API_KEY1"])

import logging

from langchain_openai import AzureChatOpenAI

from Settings.config import Config

logging.basicConfig(level=logging.INFO)


# Validamos configuracion
if (
    not Config.API_BASE
    or not Config.OPENAI_API_DEPLOPYMENT_NAME
    or not Config.OPENAI_API_KEY
):
    raise ValueError(
        "API_BASE, OPENAI_API_DEPLOPYMENT_NAME, OPENAI_API_KEY must be set in Config"
    )

try:
    llm = AzureChatOpenAI(
        azure_endpoint=Config.API_BASE,
        azure_deployment=Config.OPENAI_API_DEPLOPYMENT_NAME,
        api_key=Config.OPENAI_API_KEY,
        api_version=Config.OPENAI_API_VERSION,
    )
    logging.info("Llm started succesfull...")

    # Test validation
    response = llm.invoke([{"role": "user", "content": "Hi Mir!"}])
    logging.info(f"Test llm response: {response.content}")
except Exception as e:
    raise RuntimeError(f"Error initialicing AzureChatOpenAI: {e}")

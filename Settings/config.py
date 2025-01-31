import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
    OPENAI_API_DEPLOPYMENT_NAME = os.getenv("OPENAI_API_DEPLOPYMENT_NAME")
    API_BASE = os.getenv("API_BASE")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL = os.getenv("MODEL")
    LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
    LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
    LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
    LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION")

    @classmethod
    def print_config(cls):
        """Print configuration variables:"""
        print("----- CURRENT CONFIGURATION -----")
        print(f"API_BASE: {cls.API_BASE}")
        print(f"MODEL: {cls.MODEL}")
        print(f"LANGSMITH_TRACING: {cls.LANGSMITH_TRACING}")
        print(f"LANGSMITH_PROJECT: {cls.LANGSMITH_PROJECT}")
        print(f"OPENAI_API_DEPLOPYMENT_NAME: {cls.OPENAI_API_DEPLOPYMENT_NAME}")
        print(f"OPENAI_API_VERSION: {cls.OPENAI_API_VERSION}")


# test
if __name__ == "__main__":
    Config.print_config()

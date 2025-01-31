import logging
from enum import Enum
from typing import List

from langchain.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults

from Settings.config import Config

logging.basicConfig(level=logging.INFO)


def tool_tavily(max_results: int = 2) -> BaseTool:
    try:
        tavily = Config.TAVILY_API_KEY
        tool = TavilySearchResults(max_results=max_results)
        return tool
    except Exception as e:
        logging.error(f"Error al generar la tool tavily: {e}")
        raise


class ToolInventory(Enum):
    TAVILY_SEARCH = "tool_tavily"

import logging
from enum import Enum
from typing import List, Annotated

from langchain.tools import BaseTool
from langchain_community.tools.tavily_search import TavilySearchResults

from Settings.config import Config

logging.basicConfig(level=logging.INFO)

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import interrupt, Command
from langchain_core.messages import ToolMessage


def tool_tavily(max_results: int = 2) -> BaseTool:
    try:
        tavily = Config.TAVILY_API_KEY
        tool = TavilySearchResults(max_results=max_results)
        return tool
    except Exception as e:
        logging.error(f"Error al generar la tool tavily: {e}")
        raise


def get_human_assistance() -> BaseTool:
    @tool
    def human_assistance(query: str) -> str:
        """Request assisntace for human"""
        human_response = interrupt({"query": query})
        return human_response["data"]

    return human_assistance


def get_human_assistance_custom() -> BaseTool:
    @tool
    def human_assistance_custom(
        name: str, birthday: str, tool_call_id: Annotated[str, InjectedToolCallId]
    ) -> str:
        """Request assisntace for human"""
        human_response = interrupt(
            {
                "question": "Is this correct?",
                "name": name,
                "birthday": birthday,
            }
        )
        # If the information is correct, update the state as-is
        if human_response.get("correct", "").lower().startswith("y"):
            verified_name = name
            verified_birthday = birthday
            response = "Correct"

        # Otherwise, receive information from the human reviewer.
        else:
            verified_name = human_response.get("name", name)
            verified_birthday = human_response.get("birthday", birthday)
            response = f"Made a correction: {human_response}"

        # Actualizamos explicitamente el estado con un ToolMessage dentro del tool
        state_update = {
            "name": verified_name,
            "birthday": verified_birthday,
            "messages": [ToolMessage(response, tool_call_id=tool_call_id)],
        }

        # We return a Command object in the tool to update our state
        return Command(update=state_update)

    return human_assistance_custom


class ToolInventory(Enum):
    TAVILY_SEARCH = "tool_tavily"
    HUMAN_ASSISTANCE = "humman_assistance"
    HUMAN_ASSISTANCE_CUSTOM = "human_assistance_custom"

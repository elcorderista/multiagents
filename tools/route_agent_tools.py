from langgraph.graph import END, START, StateGraph

from tools.node_state import State


def route_tools(state: State):
    """Usar en conditional_edge para enrutar al Nodo Tool si en  el ultimo mensaje
    tiene llamas a tools. De otra forma retornar al final

    Args:
        state (State): Estado del Grafo
    """
    if isinstance(state, list):
        ai_messages = state[-1]
    elif messages := state.get("messages", []):
        ai_messages = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_messages, "tool_calls") and len(ai_messages.tool_calls) > 0:
        return "tools"
    return END

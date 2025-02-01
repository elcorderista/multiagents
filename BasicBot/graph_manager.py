from typing import Annotated
import logging

# Manejo de Estado en Memoria
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph.state import CompiledStateGraph

# We use the prebuilt functions insted of ours functions
from langgraph.prebuilt import ToolNode, tools_condition

from models.llmOpenAi import llm
from tools.agent_tools import (
    tool_tavily,
    get_human_assistance,
    get_human_assistance_custom,
)
from tools.basic_tool import BasicToolNode
from tools.node_state import State, StateCustom
from tools.route_agent_tools import route_tools

logging.basicConfig(level=logging.INFO)


def graph_creation_tool():
    graph_builder = StateGraph(State)

    # Definicion del nodo
    def chatbot(state: State):
        return {"messages": llm.invoke(state["messages"])}

    CHATBOT = "chatbot"

    # Para agregar un nodo mandamos el nombre y la funcion que representa ese nodo
    graph_builder.add_node(CHATBOT, chatbot)

    # Agregamos un punto de entrada para nuestro nodo
    graph_builder.add_edge(START, "chatbot")
    # AGragamos un punto de salida para nuestro nodo
    graph_builder.add_edge(CHATBOT, END)

    graph = graph_builder.compile()

    return graph


def creation_graph_search():
    tools = [tool_tavily(max_results=2)]
    graph_builder = StateGraph(State)
    llm_with_tools = llm.bind_tools(tools=tools)

    def chatbot(state: State):
        """Nodo Chatbor"""
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    CHATBOT = "chatbot"
    TOOLS = "tools"

    # Agregamos el nodo al builder:
    graph_builder.add_node(CHATBOT, chatbot)

    # El nodo tool, valida el ultimo mensaje y
    # llama a  las tools si el mensaje contiene
    # llamadas a la herraemita.
    tool_node = BasicToolNode(tools=tools)

    graph_builder.add_node(TOOLS, tool_node)

    # Adicionamos tool_condigion, la cual retorna tools si el chatbot indica usar tools
    # o END si responde directamente. Esta condicional define el routing del loop principal
    # del nodo.
    graph_builder.add_conditional_edges(
        CHATBOT,
        route_tools,
        # El siguietne diccionario le indica al grafo que interprete las salidas de la
        # condicion como un nodo especifico.
        # Por defecto es la funcion de identidad, pero si queremos usar un nodo con
        # otro nombre aparte de 'tools', se puede actualizar el valor del dict con otro
        # valor, por ejemplo, "tools": "my_tools"
        {"tools": "tools", END: END},
    )

    # Una vez que se activa una tool, regresa y luego el bot decide el siguiente paso
    # Cada vez que entra al nodo condicional,  vaya a TOOLS, para ver si hay llamado a
    # una herramienta, o finalice el ciclo si respondio el nodo directamente.
    # El router que se realizo finilza el flujo si no hay llamadas a la herramienta.
    graph_builder.add_edge(TOOLS, CHATBOT)
    graph_builder.add_edge(START, CHATBOT)
    graph = graph_builder.compile()

    return graph


def stream_graph_upgrade(user_input: str, graph: StateGraph):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant: ", value["messages"][-1].content)


def graph_with_memory() -> CompiledStateGraph:
    # in memory checkPointer
    memory = MemorySaver()
    # Search tool
    tools = [tool_tavily(max_results=2)]

    # Create Builder
    grap_builder = StateGraph(State)

    # Model with tools
    llm_with_tools = llm.bind_tools(tools=tools)

    CHATBOT = "chatbot"
    TOOLS = "tools"

    def chatbot(state: State):
        """Firsnode in the graph"""
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    # Tool Node
    tool_node = ToolNode(tools=tools)

    # Add Nodes
    grap_builder.add_node(CHATBOT, chatbot)
    grap_builder.add_node(TOOLS, tool_node)

    # Add Conditional Edge
    grap_builder.add_conditional_edges(
        CHATBOT,
        tools_condition,
    )

    # Add Edges, any time a tool is called, we return to the chatbot
    # to decide the next step.
    grap_builder.add_edge(TOOLS, CHATBOT)
    grap_builder.add_edge(START, CHATBOT)

    # Compile de graph with checkpointer
    graph = grap_builder.compile(checkpointer=memory)

    return graph


def create_image_graph(path: str, graph: CompiledStateGraph) -> None:
    try:
        png_path = graph.get_graph().draw_mermaid_png()
        with open(path, "wb") as f:
            f.write(png_path)
        logging.info(f"Saved graph to {path}")
    except Exception as e:
        logging.exception(f"Error al generar la imagen del grafo: {e}")
        raise


def graph_with_human() -> CompiledStateGraph:
    # Add memory checkpointer
    memory = MemorySaver()

    # Add Tools Search
    tool_search = tool_tavily(max_results=2)
    tool_human = get_human_assistance()
    tools = [tool_search, tool_human]
    # Create builder
    graph_builder = StateGraph(State)

    # Model With Tools
    llm_with_tools = llm.bind_tools(tools=tools)

    # Constants nodes
    CHATBOT = "chatbot"
    TOOLS = "tools"

    # -- Definimos nodos -- #
    def chatbot(state: State):
        message = llm_with_tools.invoke(state["messages"])
        """
        Debido a que interrumpiremos el workflow
        deshabilitamos las llamadas de paraleas tools para evitar 
        repetir cualquier invocacion a un tool cuando reanudemos 
        """
        assert len(message.tool_calls) <= 1
        return {"messages": [message]}

    tool_node = ToolNode(tools=tools)

    graph_builder.add_node(CHATBOT, chatbot)
    graph_builder.add_node(TOOLS, tool_node)

    # -- Definimos conexiones -- #
    graph_builder.add_conditional_edges(
        CHATBOT,
        tools_condition,
    )
    graph_builder.add_edge(TOOLS, CHATBOT)
    graph_builder.add_edge(START, CHATBOT)

    grafo = graph_builder.compile(checkpointer=memory)

    return grafo


def graph_with_human_state() -> CompiledStateGraph:
    # Add memory checkpointer
    memory = MemorySaver()

    # Add Tools Search
    tool_search = tool_tavily(max_results=2)
    tool_human_state = get_human_assistance_custom()
    tools = [tool_search, tool_human_state]
    # Create builder
    graph_builder = StateGraph(State)

    # Model With Tools
    llm_with_tools = llm.bind_tools(tools=tools)

    # Constants nodes
    CHATBOT = "chatbot"
    TOOLS = "tools"

    # -- Definimos nodos -- #
    def chatbot(state: StateCustom):
        message = llm_with_tools.invoke(state["messages"])
        """
        Debido a que interrumpiremos el workflow
        deshabilitamos las llamadas de paraleas tools para evitar 
        repetir cualquier invocacion a un tool cuando reanudemos 
        """
        assert len(message.tool_calls) <= 1
        return {"messages": [message]}

    tool_node = ToolNode(tools=tools)

    graph_builder.add_node(CHATBOT, chatbot)
    graph_builder.add_node(TOOLS, tool_node)

    # -- Definimos conexiones -- #
    graph_builder.add_conditional_edges(
        CHATBOT,
        tools_condition,
    )
    graph_builder.add_edge(TOOLS, CHATBOT)
    graph_builder.add_edge(START, CHATBOT)

    grafo = graph_builder.compile(checkpointer=memory)

    return grafo

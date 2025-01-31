from typing import Annotated

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from models.llmOpenAi import llm
from tools.agent_tools import tool_tavily
from tools.basic_tool import BasicToolNode
from tools.node_state import State
from tools.route_agent_tools import route_tools


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
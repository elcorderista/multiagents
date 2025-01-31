import os

from IPython.display import Image, display

from BasicBot.graph_manager import graph_creation_tool

graph = graph_creation_tool()


def print_grapho():
    output_path = "graph_one.png"

    try:
        png_path = graph.get_graph().draw_mermaid_png()
        display(Image(data=png_path))
        # Guarda la imagen:
        with open(output_path, "wb") as f:
            f.write(png_path)
    except Exception as e:
        print(f"Error al generar el grafo: {e}")


def stream_graph_upgrade(user_input: str):

    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant: ", value["messages"].content)


while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Adios!")
            break
        stream_graph_upgrade(user_input)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_upgrade(user_input)
        break

import logging
import os

from IPython.display import Image

from BasicBot.graph_manager import creation_graph_search, stream_graph_upgrade

logging.basicConfig(level=logging.INFO)
graph = creation_graph_search()


def create_image_graph():
    try:
        output_path = "search_graph_two.png"
        png_path = graph.get_graph().draw_mermaid_png()
        # Guarda la imagen:
        with open(output_path, "wb") as f:
            f.write(png_path)
    except Exception as e:
        logging.error(f"Error al generar la imagen del grafo: {e}")
        raise


# Testeamos el grafo
while True:
    try:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Adios!!")
            break

        stream_graph_upgrade(user_input, graph)
    except:
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_upgrade(user_input=user_input, graph=graph)
        break

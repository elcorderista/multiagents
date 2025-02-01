import logging

from BasicBot.graph_manager import graph_with_human, create_image_graph

from langgraph.types import Command

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    graph = graph_with_human()
    ##create_image_graph("humman_graph.png", graph)

    user_input = "Necesito orientacion de un experto para crear un agente IA. Podrias solicitarme ayuda?"
    config = {"configurable": {"thread_id": 1}}

    # Create Stream
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )

    needs_human_intervetion = False

    for event in events:
        if "messages" in event:
            last_message = event["messages"][-1]
            last_message.pretty_print()

            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                for tool_call in last_message.tool_calls:
                    if tool_call["name"] == "human_assistance":
                        needs_human_intervetion = True

    if needs_human_intervetion:
        # Hacemos snapshot
        snapshot = graph.get_state(config)
        snapshot.next
        logging.info(f"Save memory graph...")

        # Get human intervention
        human_response = input("Ingresa la respuesta del experto:")
        humand_command = Command(resume={"data": human_response})

        events = graph.stream(humand_command, config, stream_mode="values")
        for event in events:
            if "messages" in event:
                event["messages"][-1].pretty_print()

    logging.info(f"Proceso finalizado")

import logging

from BasicBot.graph_manager import (
    graph_with_human
)

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    graph = graph_with_human()

    config = {"configurable": {"thread_id": "1"}}
    input_user = {
        "messages": [
            {
            "role":"user",
            "content": (
                "Estoy aprendiendo LangGrap. "
                "Puedes hacer alguna investigacion sobre eso para mi?"
            ),
            },
        ],
    }
    events = graph.stream(input_user, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            last_message = event["messages"][-1]
            last_message.pretty_print()

    user_input = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Si, eso es util, quiza pueda construir un agente autonomo con el!"
                ),
            },
        ]
    }
    events = graph.stream(user_input, config, stream_mode="values")
    for event in events:
        if "messages" in event:
            last_message = event["messages"][-1]
            last_message.pretty_print()

    # Buscamos un id aleatorio de checkpoint en el historial
    to_replay = None
    for state in graph.get_state_history(config):
        print("Num Messages: ", len(state.values["messages"]), "Next: ", state.next)
        print("-" * 80)
        if len(state.values["messages"]) == 6:
            # Seleccionamos de forma arbitraria un estado especifico
            # en funcion de la cantidad de mensajes de chat en el estado
            to_replay = state
            print(to_replay.next)
            print(to_replay.config)

    # Ejecutamos el stream desde ese checkpoint
    for event in graph.stream(None, to_replay.config, stream_mode="values"):
        if "messages" in event:
            last_message = event["messages"][-1]
            last_message.pretty_print()
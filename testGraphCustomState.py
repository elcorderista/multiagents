import logging

from BasicBot.graph_manager import graph_with_human_state, create_image_graph

from langgraph.types import Command

if __name__ == "__main__":
    user_input = (
        "Puedes buscar cuando fue el release de LangGraph?"
        "Cuando tengas la respuesta, usa la herramienta human_assistance_custom para revisarla"
    )

    config = {"configurable": {"thread_id": "1"}}
    graph = graph_with_human_state()
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )

    needs_human_intervention = False

    for event in events:
        if "messages" in event:
            last_message = event["messages"][-1]
            last_message.pretty_print()

            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                for tool_call in last_message.tool_calls:
                    if tool_call["name"] == "human_assistance_custom":
                        needs_human_intervention = True

    # Hacemos snapshot del State
    if needs_human_intervention:
        state = graph.get_state(config)
        state.next

        human_response = {"name": "LangGraph", "birthday": "Jan 14, 2024"}

        # Reanudacion del flujo
        human_command = Command(resume=human_response)
        events = graph.stream(human_command, config, stream_mode="values")
        for event in events:
            if "messages" in event:
                last_message = event["messages"][-1]
                last_message.pretty_print()
    # Intervencion Manual
    graph.update_state(config, {"name":"LangGraph (library)"})
    snapshot = graph.get_state(config)
    dict_2 = {k: v for k, v in snapshot.values.items() if k in ("name", "birthday")}



    logging.info(f"Proceso finalizado")

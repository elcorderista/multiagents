import logging

from BasicBot.graph_manager import graph_with_memory, create_image_graph

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    graph = graph_with_memory()
    # create_image_graph('memory_graph.png', graph)

    # Create a key for conversation
    config = {"configurable": {"thread_id": "1"}}

    # Call Chatbot
    user_input = "Hi there! My name is Jaco."

    # The config is the second positional argument to stream() or invoke()
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )
    for event in events:
        event["messages"][-1].pretty_print()

    snapshot = graph.get_state(config)
    print(type(snapshot))

    snapshot.next
    # Second Call
    user_input = "Remember my name?"
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        config,
        stream_mode="values",
    )

    for event in events:
        event["messages"][-1].pretty_print()

    # Third Call
    user_input = "Remember my name?"
    events = graph.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        {"configurable": {"thread_id": "2"}},
        stream_mode="values",
    )

    for event in events:
        event["messages"][-1].pretty_print()

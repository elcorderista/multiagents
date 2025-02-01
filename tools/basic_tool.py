import json

from langchain_core.messages import ToolMessage


class BasicToolNode:
    """A node that runs the tools requested in the las AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        # if messages := inputs.get("messages", []):
        # Get the last message
        #    message = messages[-1]
        # else:
        #    raise ValueError("No message found in input")

        messages = inputs.get("messages", [])
        if not messages:
            raise ValueError("No hay mensajes para procesar en tool")

        last_message = messages[-1] if isinstance(messages, list) else messages
        # if not hasattr(last_message, "tool_calls"):
        #    return{"messages": messages}

        outputs = []
        for tool_call in last_message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}

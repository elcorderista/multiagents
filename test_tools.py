from tools.agent_tools import ToolInventory, tool_tavily

query = "Que van las perdidas con Nvidia"
tavily = tool_tavily(max_results=2)
result = tavily.invoke(query)
print(result)

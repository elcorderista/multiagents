from typing import Sequence, List
from Settings.config import Config
from models.llmOpenAi import llm
from ReflectionAgent.chains import (
    generate_chain,
    reflect_chain
)


from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

#Constantes key de los nodos. 
REFLECT = "reflect"
GENERATE = "generate"


def generation_node(state: Sequence[BaseMessage]):
    """Nodo generador del post en x"""
    return generate_chain.invoke({"messages":state})

def reflection_nodo(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    """Nodo que reflexiona y critica el posto"""
    res = reflect_chain.invoke({"messages": messages})
    #Tomtamos la salida del llm y lo enmascaramos como una entrada del usuario
    return [HumanMessage(content=res.content)]


#Inicializacion del grafo
builder = MessageGraph()
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_nodo)
builder.set_entry_point(GENERATE)

#Conditional Edge 
def should_continue(state: List[BaseMessage]):
    if len(state) > 6:
        return END
    return REFLECT

builder.add_conditional_edges(GENERATE, should_continue)

#Compilamos el grafo
graph = builder.compile()

#Para visualizar el grafo
print(graph.get_graph().draw_mermaid()) #---> mermaid.live

#Impresion en asscii
graph.get_graph().print_ascii()




if __name__ == "__main__":
    print("hello Mir")
    inputs = HumanMessage(content="""Make this post better: 
                          @LangChainAI
                          - newly Tool Calling feature is seriously underrated.
                          After a long wait, it's here - making the implementation af agents across different models with function calling.
                          Made a video covering their newest blog post
                          """)
    response = graph.invoke(inputs)
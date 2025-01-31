from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
# Definicion del State
class State(TypedDict):
    # Los mensajes tienen el tipo "list". La funcion `add_messages`
    # En la annotation define como se debe actualizar esta clave de estado
    # (en este caso, agrega mensajes a la lista, en lugar de sobreescribirlos)
    messages: Annotated[list, add_messages]

#Contendra los prompts que vamos a utilizar en el langgraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from models.llmOpenAi import llm

#Define reflection prompt
reflection_promt = ChatPromptTemplate([
    (
        "system",
        "You are a virtual x influencer grading a post. Generate critique and recommendations for the user's c"
        "Always provide detailes recommendations, including requests for length, virality, style, etc."
    ),
    MessagesPlaceholder("messages"),
] )

#Define Generation prompt
generation_prompt = ChatPromptTemplate([
    (
        "system",
        "You are a x techie influencer assistant tasked with writing excellent x posts."
        "Generate the best x post posible for the user's request."
        "If the user provides critique, respond with a revised version of your previos attempts."
        
    ),
    MessagesPlaceholder("messages"),
])


#Creamos los chains
generate_chain = generation_prompt | llm
reflect_chain = reflection_promt | llm
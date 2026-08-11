from langchain_ollama import ChatOllama

model = ChatOllama(
    model="gemma4:e2b",
    temperature=0
)
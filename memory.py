from langchain.memory import ConversationBufferMemory

def get_pm_memory():
    # Use separate memory for each agent type for clearer state management
    return {
        "prioritization": ConversationBufferMemory(memory_key="prioritization"),
        "grooming": ConversationBufferMemory(memory_key="grooming"),
        "suggestion": ConversationBufferMemory(memory_key="suggestion"),
        "insights": ConversationBufferMemory(memory_key="insights"),
    }
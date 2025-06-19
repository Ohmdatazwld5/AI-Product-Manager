import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from app.memory import get_pm_memory
from app.rag import retrieve_context

# --- Environment variable check ---
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

llm = ChatGroq(
    model_name="llama3-8b-8192",
    api_key=api_key,
    temperature=0.2,
    max_tokens=2048,
)

memory = get_pm_memory()

def add_chain_of_thought(instr: str) -> str:
    """Wraps prompt with a chain-of-thought instruction for better reasoning."""
    return (
        "Let's think step by step. First, reason about the problem in detail, then provide the final structured answer as requested.\n\n"
        + instr
    )

# --- AGENT 1: Feature Prioritization ---
feature_prioritization_prompt = PromptTemplate(
    input_variables=["features", "context"],
    template=add_chain_of_thought("""
You are an expert Product Manager. Given the following features:
{features}

And context:
{context}

Prioritize the features (1 being highest), and provide a reason per feature. Output JSON: 
{{"prioritized_features": [{{"feature": "...", "reason": "..."}}, ...]}}
"""),
)
feature_prioritization_chain = feature_prioritization_prompt | llm

def prioritize_features(features: list[str]):
    """Prioritizes features and provides reasoning using LLM."""
    context = retrieve_context(features)
    input_str = "\n".join(f"- {f}" for f in features)
    response = feature_prioritization_chain.invoke({
        "features": input_str,
        "context": context
    })
    return response

# --- AGENT 2: Backlog Grooming ---
backlog_grooming_prompt = PromptTemplate(
    input_variables=["backlog", "context"],
    template=add_chain_of_thought("""
You are an agile PM. Review the backlog:
{backlog}

Context:
{context}

Group related tickets, suggest improvements, and summarize. Output JSON:
{{"groups": [{{"group": "...", "tickets": [...], "suggestions": "..."}}, ...]}}
"""),
)
backlog_grooming_chain = backlog_grooming_prompt | llm

def groom_backlog(backlog: list[dict]):
    """Groups and improves backlog items using LLM."""
    context = retrieve_context([item['title'] for item in backlog])
    input_str = "\n".join([f"{item['id']}: {item['title']} - {item['desc']}" for item in backlog])
    response = backlog_grooming_chain.invoke({
        "backlog": input_str,
        "context": context
    })
    return response

# --- AGENT 3: Intelligent Task Suggester ---
task_suggestion_prompt = PromptTemplate(
    input_variables=["backlog", "context"],
    template=add_chain_of_thought("""
Given backlog items:
{backlog}

And context:
{context}

Suggest 3 new actionable tasks or improvements the team should consider (JSON array).
"""),
)
task_suggestion_chain = task_suggestion_prompt | llm

def suggest_tasks(backlog: list[dict]):
    """Suggests new tasks or improvements using LLM."""
    context = retrieve_context([item['title'] for item in backlog])
    input_str = "; ".join([f"{item['title']}" for item in backlog])
    response = task_suggestion_chain.invoke({
        "backlog": input_str,
        "context": context
    })
    return response

# --- AGENT 4: Team Insights ---
team_insights_prompt = PromptTemplate(
    input_variables=["activity"],
    template=add_chain_of_thought("""
You are an AI scrum master. Given this team activity log:
{activity}

Summarize team progress, risks, and blockers. Output JSON with "summary", "risks", "blockers".
"""),
)
team_insights_chain = team_insights_prompt | llm

def team_insights(activity_log: str):
    """Summarizes team activity, risks, and blockers using LLM."""
    response = team_insights_chain.invoke({"activity": activity_log})
    return response
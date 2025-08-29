from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from app.config.settings import settings
import os

def get_response_from_ai_agents(llm_id, query, allow_search, system_prompt):
    """
    Get response from AI agents using LangGraph

    Args:
        llm_id (str): Model identifier
        query (List[str]): List of user message strings
        allow_search (bool): Whether to allow web search
        system_prompt (str): System prompt for the agent

    Returns:
        str: AI response content
    """
    # Ensure API keys are set
    os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
    if allow_search:
        os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY

    # Initialize LLM and tools
    llm = ChatGroq(model=llm_id)
    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    # Create agent (without state_modifier)
    agent = create_react_agent(model=llm, tools=tools)

    # Build message history: start with the system prompt
    messages = [SystemMessage(content=system_prompt)]
    # Append each user message
    for msg in query:
        messages.append(HumanMessage(content=msg))

    # Invoke the agent
    state = {"messages": messages}
    response = agent.invoke(state)

    # Extract AI messages
    response_messages = response.get("messages", [])
    ai_contents = [
        msg.content
        for msg in response_messages
        if isinstance(msg, AIMessage)
    ]

    return ai_contents[-1] if ai_contents else "No response generated."

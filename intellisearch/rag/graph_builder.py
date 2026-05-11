"""
Graph builder module for the adaptive RAG system.
"""
from langchain_community.tools import TavilySearchResults
from langchain_core.messages import AIMessage
from langchain_core.prompts import PromptTemplate
from langgraph.constants import START, END
from langgraph.graph.state import StateGraph

from intellisearch.rag.reAct_agent import agent_executor
from intellisearch.rag.retriever_setup import get_retriever
from intellisearch.config.settings import Config
from intellisearch.llms.groq_llm import llm
from intellisearch.models.grade import Grade
from intellisearch.models.route_identifier import RouteIdentifier
from intellisearch.models.state import State
from intellisearch.tools.graph_tools import routing_tool, doc_tool

config = Config()


def query_classifier(state: State):
    """Classify the query to determine routing."""
    question = state["messages"][-1].content
    retriever = get_retriever()
    context = retriever.invoke(question)

    llm_with_structured_output = llm.with_structured_output(RouteIdentifier)
    classify_prompt = PromptTemplate(
        template=config.prompt("classify_prompt"),
        input_variables=["question", "context"]
    )
    chain = classify_prompt | llm_with_structured_output
    result = chain.invoke({"question": question, "context": context})
    print(f"Route: {result.route}")

    return {
        "messages": state["messages"],
        "route": result.route,
        "latest_query": question
    }


def general_llm(state: State):
    """Fetch general knowledge result from LLM."""
    result = llm.invoke(state["messages"])
    return {"messages": result}


def retriever_node(state: State):
    """Retrieve results using the reAct agent."""
    messages = state["latest_query"]
    result = agent_executor.invoke({"input": messages})

    intermediate_steps = result.get("intermediate_steps", [])
    tool_calls = []
    if intermediate_steps:
        for action, tool_result in intermediate_steps:
            tool_calls.append({
                "tool": action.tool,
                "input": action.tool_input,
            })

    new_message = AIMessage(
        content=result["output"],
        additional_kwargs={"tool_calls": tool_calls},
    )
    return {"messages": [new_message]}


def grade(state: State):
    """Grade the results retrieved from vector stores."""
    grading_prompt = PromptTemplate(
        template=config.prompt("grading_prompt"),
        input_variables=["question", "context"]
    )
    context = state["messages"][-1].content
    question = state["latest_query"]

    llm_with_grade = llm.with_structured_output(Grade)
    chain_graded = grading_prompt | llm_with_grade
    result = chain_graded.invoke({
        "question": question,
        "context": context
    })
    return {
        "messages": state["messages"],
        "binary_score": result.binary_score
    }


def rewrite_query(state: State):
    """Rewrite the query for better retrieval."""
    query = state["latest_query"]
    rewrite_prompt = PromptTemplate(
        template=config.prompt("rewrite_prompt"),
        input_variables=["query"]
    )
    chain = rewrite_prompt | llm
    result = chain.invoke({"query": query})
    return {"latest_query": result.content}


def generate(state: State):
    """Generate the final answer."""
    context = state["messages"][-1].content
    generate_prompt = PromptTemplate(
        template=config.prompt("generate_prompt"),
        input_variables=["context"]
    )
    generate_chain = generate_prompt | llm
    result = generate_chain.invoke({"context": context})
    return {
        "messages": [{"role": "assistant", "content": result.content}]
    }


def web_search(state: State):
    """Search the web for the query."""
    search_tool = TavilySearchResults()
    result = search_tool.invoke(state["latest_query"])
    contents = [item["content"] for item in result if "content" in item]
    return {
        "messages": [{"role": "assistant", "content": "\n\n".join(contents)}]
    }


# Build the graph
graph = StateGraph(State)

graph.add_node("query_analysis", query_classifier)
graph.add_node("retriever", retriever_node)
graph.add_node("grade", grade)
graph.add_node("generate", generate)
graph.add_node("rewrite", rewrite_query)
graph.add_node("web_search", web_search)
graph.add_node("general_llm", general_llm)

graph.add_edge(START, "query_analysis")
graph.add_edge("web_search", "generate")
graph.add_edge("retriever", "grade")
graph.add_edge("rewrite", "retriever")
graph.add_conditional_edges("query_analysis", routing_tool)
graph.add_conditional_edges("grade", doc_tool)
graph.add_edge("generate", END)
graph.add_edge("general_llm", END)

builder = graph.compile()
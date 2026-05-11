"""
Common tools for document and description processing.
"""
from intellisearch.llms.groq_llm import llm


def enhance_description_with_llm(user_description: str) -> str:
    """
    Enhance user-provided document description using LLM.
    """
    prompt = f"""
    Rewrite the following user-provided document description to be used as a retriever tool instruction.
    It should clearly state that the tool is only for answering questions about the uploaded content.
    Description: "{user_description}"
    Tool Instruction:"""

    response = llm.invoke(prompt)
    return response.content.strip()
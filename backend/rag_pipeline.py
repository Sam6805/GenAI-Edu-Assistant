"""
RAG Pipeline Module
Builds and manages the RAG query pipeline.
"""

from modes import format_instruction


SYSTEM_PROMPT = """You are an Educational Content Assistant.

Your job is to answer questions ONLY using the provided study material context.
If the answer is not present in the context, say:
"I could not find this in the uploaded material."

Never invent information outside the provided context.
Always follow the selected response mode strictly.
"""


def build_query(context, question, mode):
    """
    Build a complete query for the LLM with context, question, and mode.
    
    Args:
        context (str): Retrieved context from vector store
        question (str): User's question
        mode (str): Response mode
        
    Returns:
        str: Complete formatted query
    """
    mode_instruction = format_instruction(mode)
    
    query = f"""{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Response Mode Instructions:
{mode_instruction}

Answer using only the context provided above. Follow the response mode instructions strictly.
"""
    
    return query


def format_context(documents):
    """
    Format retrieved documents into a single context string.
    
    Args:
        documents (list): List of Document objects
        
    Returns:
        str: Formatted context string
    """
    context_parts = []
    for i, doc in enumerate(documents, 1):
        context_parts.append(f"[Source {i}]\n{doc.page_content}\n")
    
    return "\n".join(context_parts)

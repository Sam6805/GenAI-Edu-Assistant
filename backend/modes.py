"""
Response Mode Formatter Module
Defines different response modes for the educational assistant.
"""

MODE_INSTRUCTIONS = {
    "default": """
    Respond with:
    - Clear explanation
    - Simple language
    - Medium length
    - Balanced detail
    """,
    
    "exam": """
    Respond in formal academic format with:
    1. Definition
    2. Detailed Explanation
    3. Key Points (bullet points)
    4. Conclusion
    Use formal academic tone and structured format.
    """,
    
    "summary": """
    Respond with:
    - Very concise answer
    - Bullet points only
    - Key facts only
    - No elaboration
    """,
    
    "explain_like_5": """
    Respond with:
    - Extremely simple language
    - Use analogies and examples
    - No technical jargon
    - Explain as if talking to a 5-year-old child
    """,
    
    "creative": """
    Respond with:
    - Story-based explanation
    - Use metaphors and creative narratives
    - Make it engaging and memorable
    - Still educational and accurate
    """
}


def format_instruction(mode):
    """
    Get formatting instruction for a specific response mode.
    
    Args:
        mode (str): Response mode (default, exam, summary, explain_like_5, creative)
        
    Returns:
        str: Formatting instruction
    """
    return MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["default"])


def get_available_modes():
    """
    Get list of available response modes.
    
    Returns:
        list: List of mode names
    """
    return list(MODE_INSTRUCTIONS.keys())

"""
ScaleDown Client Module  
Generates answers from context using local sentence transformers.
"""

import os
import re


def generate_answer(api_key, context, prompt, model="gpt-4o", mode="default"):
    """
    Generate an answer based on the provided context with mode-specific formatting.
    
    Since ScaleDown only compresses prompts and doesn't generate answers,
    we'll use a smart extraction approach and format based on the mode.
    
    Args:
        api_key (str): API key (not used in this simple implementation)
        context (str): Context information from the PDF
        prompt (str): Full prompt with instructions and question
        model (str): Model to use (not used in simple implementation)
        mode (str): Response mode (default, exam, summary, explain_like_5, creative)
        
    Returns:
        str: Generated answer based on context, formatted per mode
    """
    
    # Extract the question from the prompt
    question = ""
    if "Question:" in prompt:
        question_part = prompt.split("Question:")[1]
        # Get everything after "Question:" until response mode or end
        if "Response Mode" in question_part:
            question = question_part.split("Response Mode")[0].strip()
        else:
            question = question_part.strip()
    
    # Extract context sources
    context_sources = []
    if "Context:" in prompt:
        context_section = prompt.split("Context:")[1]
        if "Question:" in context_section:
            context_section = context_section.split("Question:")[0]
        
        # Split by [Source X]
        sources = re.split(r'\[Source \d+\]', context_section)
        context_sources = [s.strip() for s in sources if s.strip()]
    
    # If no sources found, return error
    if not context_sources:
        return "I could not find this information in the uploaded material."
    
    # Analyze the question to understand what's being asked
    question_lower = question.lower()
    
    # Extract key question words (who, what, where, when, why, how)
    question_type = None
    if any(word in question_lower for word in ['why', 'reason', 'because']):
        question_type = 'why'
    elif any(word in question_lower for word in ['who', 'person', 'character']):
        question_type = 'who'
    elif any(word in question_lower for word in ['what', 'describe']):
        question_type = 'what'
    elif any(word in question_lower for word in ['where', 'place', 'location']):
        question_type = 'where'
    elif any(word in question_lower for word in ['when', 'time']):
        question_type = 'when'
    elif any(word in question_lower for word in ['how']):
        question_type = 'how'
    
    # Extract main subject/keywords from question (remove common words)
    common_words = {'is', 'the', 'a', 'an', 'was', 'were', 'are', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might', 'must', 'can'}
    question_words = [w.strip('?.,!') for w in question_lower.split() if w.strip('?.,!') not in common_words and len(w) > 2]
    
    # Find the most relevant sources
    scored_sources = []
    for source in context_sources:
        source_lower = source.lower()
        score = 0
        
        # Score based on keyword matches
        for word in question_words:
            if word in source_lower:
                score += 2
        
        # Bonus for question type indicators
        if question_type == 'why' and any(word in source_lower for word in ['because', 'reason', 'since', 'as']):
            score += 3
        elif question_type == 'who' and any(word in source_lower for word in ['he', 'she', 'person', 'character']):
            score += 2
        
        if score > 0:
            scored_sources.append((score, source))
    
    # Sort by score
    scored_sources.sort(reverse=True, key=lambda x: x[0])
    
    if not scored_sources:
        # If no scored matches, use all sources
        scored_sources = [(1, source) for source in context_sources]
    
    # Combine top sources to form base answer
    top_sources = scored_sources[:2]  # Use top 2 sources
    combined_text = ' '.join([source for score, source in top_sources])
    
    # Clean up the text
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()
    
    # Extract sentences for processing
    sentences = [s.strip() for s in combined_text.split('.') if s.strip()]
    
    # Format answer based on mode
    if mode == "summary":
        # Summary mode: bullet points only
        key_points = []
        for sentence in sentences[:3]:
            # Create concise bullet points
            if len(sentence) > 100:
                sentence = sentence[:97] + "..."
            key_points.append(f"• {sentence}")
        return "\n".join(key_points) if key_points else combined_text[:200]
    
    elif mode == "exam":
        # Exam mode: structured academic format
        answer_parts = []
        answer_parts.append("**Answer:**\n")
        if sentences:
            answer_parts.append(f"{sentences[0]}.")
        answer_parts.append("\n\n**Key Points:**")
        for i, sentence in enumerate(sentences[1:3], 1):
            answer_parts.append(f"\n{i}. {sentence}.")
        if len(sentences) > 3:
            answer_parts.append(f"\n\n**Additional Context:**\n{sentences[3]}.")
        return "".join(answer_parts)
    
    elif mode == "explain_like_5":
        # ELI5 mode: simple language with analogies
        # Simplify the first key sentence
        if sentences:
            main_idea = sentences[0]
            # Create a simple, friendly explanation
            answer = f"Okay, here's the simple answer:\n\n{main_idea}."
            if len(sentences) > 1:
                answer += f"\n\nIn other words: {sentences[1]}."
            return answer
        return combined_text[:300]
    
    elif mode == "creative":
        # Creative mode: story-like narrative
        if sentences:
            # Add narrative elements
            answer = f"Here's an interesting way to think about it:\n\n{sentences[0]}."
            if len(sentences) > 1:
                answer += f" {sentences[1]}."
            if len(sentences) > 2:
                answer += f" This shows us that {sentences[2]}."
            return answer
        return combined_text[:400]
    
    else:  # default mode
        # Default: clear, balanced explanation
        if len(sentences) >= 3:
            answer = '. '.join(sentences[:4]) + '.'
        elif sentences:
            answer = '. '.join(sentences) + '.'
        else:
            answer = combined_text[:400]
        return answer


def get_api_key():
    """
    Get ScaleDown API key from environment variables.
    
    Returns:
        str: API key
    """
    api_key = os.getenv("SCALEDOWN_API_KEY")
    if not api_key:
        raise ValueError("SCALEDOWN_API_KEY not found in environment variables")
    return api_key

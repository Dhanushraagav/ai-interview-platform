"""
Scoring module for evaluating interview answers.
"""
from typing import List, Tuple


def evaluate_answer(question: str, answer: str, keywords: List[str]) -> Tuple[float, str]:
    """
    Evaluate an answer based on keyword matching and answer quality.
    
    Args:
        question: The interview question
        answer: The user's answer
        keywords: List of important keywords/concepts that should be mentioned
    
    Returns:
        Tuple of (score: float, feedback: str)
        Score is between 0-10
    """
    if not answer or len(answer.strip()) == 0:
        return 0.0, "Please provide an answer to the question."
    
    answer_lower = answer.lower()
    question_lower = question.lower()
    
    # Count keyword matches
    matched_keywords = [kw for kw in keywords if kw.lower() in answer_lower]
    keyword_count = len(matched_keywords)
    total_keywords = len(keywords)
    
    # Keyword matching score (70% weight)
    keyword_score = (keyword_count / total_keywords) * 7.0 if total_keywords > 0 else 0.0
    
    # Answer length and depth score (20% weight)
    word_count = len(answer.split())
    length_score = min(word_count / 50, 1.0) * 2.0  # Optimal around 50 words
    
    # Answer relevance score (10% weight)
    # Check if answer addresses the question topic
    question_words = set(question_lower.split())
    answer_words = set(answer_lower.split())
    common_words = question_words.intersection(answer_words)
    relevance_score = min(len(common_words) / 10, 1.0) * 1.0
    
    # Calculate total score
    total_score = keyword_score + length_score + relevance_score
    total_score = min(total_score, 10.0)  # Cap at 10
    total_score = round(total_score, 2)
    
    # Generate detailed feedback
    feedback = generate_feedback(
        total_score, 
        keyword_count, 
        total_keywords, 
        matched_keywords, 
        keywords,
        word_count
    )
    
    return total_score, feedback


def generate_feedback(
    score: float,
    matched_count: int,
    total_keywords: int,
    matched_keywords: List[str],
    all_keywords: List[str],
    word_count: int
) -> str:
    """Generate detailed feedback based on the evaluation."""
    
    # Score-based feedback
    if score >= 9.0:
        feedback = "🌟 Excellent answer! "
    elif score >= 7.5:
        feedback = "✅ Very good answer! "
    elif score >= 6.0:
        feedback = "👍 Good answer. "
    elif score >= 4.0:
        feedback = "⚠️ Fair answer. "
    else:
        feedback = "❌ Your answer needs improvement. "
    
    # Keyword coverage feedback
    coverage_percent = (matched_count / total_keywords) * 100
    feedback += f"You covered {matched_count}/{total_keywords} ({coverage_percent:.0f}%) key concepts. "
    
    # Missing keywords feedback
    missing_keywords = [kw for kw in all_keywords if kw not in matched_keywords]
    if missing_keywords and score < 8.0:
        feedback += f"Consider mentioning: {', '.join(missing_keywords[:3])}. "
    
    # Length feedback
    if word_count < 20:
        feedback += "Try to provide more detail in your answer. "
    elif word_count > 100:
        feedback += "Your answer is comprehensive. "
    
    # Encouragement
    if score >= 7.0:
        feedback += "Keep up the great work! "
    elif score >= 5.0:
        feedback += "You're on the right track. "
    else:
        feedback += "Review the core concepts and try to be more specific. "
    
    return feedback.strip()


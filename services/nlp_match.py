"""
NLP matching logic for comparing candidate profiles with interview answers.
"""

import logging
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def clean_text(text: str | None) -> str:
    """Sanitize and trim input text."""
    return (text or "").strip()

def get_text_similarity(left: str, right: str) -> float:
    """Calculate cosine similarity between two text blocks using TF-IDF."""
    left_text = clean_text(left)
    right_text = clean_text(right)
    
    if not left_text or not right_text:
        return 0.0
        
    try:
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
        matrix = vectorizer.fit_transform([left_text, right_text])
        similarity = float(cosine_similarity(matrix[0], matrix[1])[0, 0])
        logger.debug(f"Computed similarity: {similarity:.4f}")
        return similarity
    except Exception as e:
        logger.error(f"Error computing text similarity: {e}")
        return 0.0

def get_skill_similarities(claimed_skills: List[str], answer_text: str) -> List[Tuple[str, float]]:
    """Calculate individual similarity scores for each claimed skill against the answer."""
    similarities: List[Tuple[str, float]] = []
    for skill in claimed_skills:
        similarity = get_text_similarity(skill, answer_text)
        similarities.append((skill, similarity))
    return similarities

def get_skill_coverage(claimed_skills: List[str], answer_text: str) -> float:
    """Calculate what percentage of claimed skills are explicitly mentioned in the answer."""
    if not claimed_skills:
        return 0.0
        
    lowered_answer = answer_text.lower()
    hits = 0
    for skill in claimed_skills:
        normalized_skill = skill.lower().strip()
        if normalized_skill and normalized_skill in lowered_answer:
            hits += 1
            
    coverage = hits / len(claimed_skills)
    logger.debug(f"Skill coverage: {coverage:.4f} ({hits}/{len(claimed_skills)})")
    return coverage

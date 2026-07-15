import re
from models import CandidateProfile, InterviewResponse, RiskAssessment

def calculate_risk(profile: CandidateProfile, response: InterviewResponse) -> RiskAssessment:
    """
    Computes a deterministic RiskAssessment based on local rules and text matching.
    """
    # 1. Input validation & Fail-Closed check
    reasons = []
    
    # Check max length (5000 chars)
    resume_text = profile.resume_text or ""
    answer_text = response.answer_text or ""
    
    if len(resume_text) > 5000 or len(answer_text) > 5000:
        return RiskAssessment(
            candidate_id=profile.candidate_id,
            score=100,
            risk_label="High",
            reasons=["Input exceeded maximum safe length (5000 characters). Failed closed for security."]
        )
        
    if not profile.candidate_id or not profile.name:
        return RiskAssessment(
            candidate_id="UNKNOWN",
            score=100,
            risk_label="High",
            reasons=["Missing mandatory candidate identifier or name. Failed closed."]
        )

    # 2. Simple Pure-Python TF-IDF / Term overlap matching
    # Tokenize words (lowercase and clean)
    def tokenize(text):
        return set(re.findall(r'\b\w+\b', text.lower()))
    
    resume_words = tokenize(resume_text)
    answer_words = tokenize(answer_text)
    
    # Calculate skill match
    skills_found = 0
    for skill in profile.claimed_skills:
        if skill.lower() in answer_text.lower():
            skills_found += 1
            
    skill_match_ratio = (skills_found / len(profile.claimed_skills)) if profile.claimed_skills else 1.0
    
    # Simple word overlap similarity between answer and resume
    intersection = resume_words.intersection(answer_words)
    union = resume_words.union(answer_words)
    similarity = len(intersection) / len(union) if union else 0.0
    
    # 3. Apply Scoring Rules
    score = 0
    
    # Rule 1: NLP Similarity Penalty
    # If the answer has extremely low similarity to the resume context
    if similarity < 0.05 and len(answer_text) > 0:
        score += 30
        reasons.append(f"Extremely low resume similarity match ({similarity:.1%})")
    elif similarity < 0.15 and len(answer_text) > 0:
        score += 15
        reasons.append(f"Low resume similarity match ({similarity:.1%})")
        
    # Rule 2: Claimed Skills Match
    if skill_match_ratio < 0.34:
        score += 20
        reasons.append("Failed to reference most of the claimed resume skills in response")
        
    # Rule 3: Canned Phrase Detection (Robotic response pattern)
    canned_patterns = [
        r"\bas\s+an\s+ai\b",
        r"\blanguage\s+model\b",
        r"\bopenai\b",
        r"\bchatgpt\b",
        r"\bmy\s+knowledge\s+cutoff\b",
        r"\bgenerated\s+by\s+ai\b"
    ]
    canned_detected = False
    for pat in canned_patterns:
        if re.search(pat, answer_text.lower()):
            canned_detected = True
            break
            
    if canned_detected:
        score += 45
        reasons.append("Robotic/Canned AI helper phrase detected in response")
        
    # Rule 4: Observation Flags Penalty
    flags = response.observation_flags or []
    flag_score = 0
    critical_flags = {"multiple_voices", "lip_sync_error", "audio_unsynced"}
    warning_flags = {"unnatural_blink", "background_swapped", "head_movement_unnatural"}
    
    for flag in flags:
        flag_cleaned = flag.lower().strip()
        if flag_cleaned in critical_flags:
            flag_score += 40
            reasons.append(f"Critical observation flag: '{flag}'")
        elif flag_cleaned in warning_flags:
            flag_score += 20
            reasons.append(f"Warning observation flag: '{flag}'")
            
    score += flag_score
    
    # Rule 5: Answer Length Depth Check
    if len(answer_text.strip()) < 30 and len(answer_text.strip()) > 0:
        score += 15
        reasons.append("Answer response is excessively short")
    elif len(answer_text.strip()) == 0:
        score += 25
        reasons.append("Interview answer text is empty")
        
    # 4. Aggregation and Capping
    score = min(max(score, 0), 100)
    
    if score >= 70:
        risk_label = "High"
    elif score >= 30:
        risk_label = "Medium"
    else:
        risk_label = "Low"
        
    if not reasons:
        reasons.append("No suspicious indicators or deepfake signatures detected.")
        
    return RiskAssessment(
        candidate_id=profile.candidate_id,
        score=score,
        risk_label=risk_label,
        reasons=reasons
    )

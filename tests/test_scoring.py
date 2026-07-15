import unittest
from models import CandidateProfile, InterviewResponse
from services.scoring import score_candidate

class TestScoring(unittest.TestCase):
    def setUp(self):
        self.profile = CandidateProfile(
            candidate_id="TEST-001",
            name="Test Candidate",
            claimed_skills=["Python"],
            resume_text="I am a Python developer."
        )

    def test_score_range(self):
        response = InterviewResponse(
            candidate_id="TEST-001",
            question="What is Python?",
            expected_skill="Python",
            answer_text="Python is a programming language I use daily.",
            observation_flags=[]
        )
        assessment = score_candidate(self.profile, response)
        self.assertGreaterEqual(assessment.score, 0)
        self.assertLessEqual(assessment.score, 100)

    def test_mismatch_case(self):
        # High risk case: mismatch skills + short answer
        response = InterviewResponse(
            candidate_id="TEST-001",
            question="What is Python?",
            expected_skill="Python",
            answer_text="I like to go outside and play sports.",
            observation_flags=["multiple_voices"]
        )
        assessment = score_candidate(self.profile, response)
        self.assertGreater(assessment.score, 50)
        self.assertEqual(assessment.risk_label, "High") if assessment.score >= 70 else self.assertEqual(assessment.risk_label, "Medium")

if __name__ == "__main__":
    unittest.main()

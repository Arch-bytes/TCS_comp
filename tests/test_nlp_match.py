import unittest
from services.nlp_match import get_text_similarity, get_skill_coverage

class TestNLPMatch(unittest.TestCase):
    def test_similarity_identical(self):
        text = "Python and Machine Learning expert"
        score = get_text_similarity(text, text)
        self.assertAlmostEqual(score, 1.0, places=4)

    def test_similarity_different(self):
        text1 = "Python"
        text2 = "Cooking recipes"
        score = get_text_similarity(text1, text2)
        self.assertLess(score, 0.1)

    def test_skill_coverage_full(self):
        skills = ["Python", "Java"]
        answer = "I love Python and Java"
        coverage = get_skill_coverage(skills, answer)
        self.assertEqual(coverage, 1.0)

    def test_skill_coverage_partial(self):
        skills = ["Python", "Java", "C++"]
        answer = "I only know Python"
        coverage = get_skill_coverage(skills, answer)
        self.assertAlmostEqual(coverage, 0.333, places=2)

if __name__ == "__main__":
    unittest.main()

import pytest
from services.scoring_engine import ScoringEngine

class MockQuestion:
    def __init__(self, id, dimension, weight, experience_min=0.0, experience_max=10.0, stack_name=None, certificate_name=None):
        self.id = id
        self.dimension = dimension
        self.weight = weight
        self.experience_min = experience_min
        self.experience_max = experience_max
        self.stack_name = stack_name
        self.certificate_name = certificate_name

def test_calculate_scores_all_max():
    questions = [
        MockQuestion(1, "JavaScript Fundamentals", 1.0),
        MockQuestion(2, "Backend Fundamentals", 1.0),
        MockQuestion(3, "Infrastructure as Code", 1.0),
        MockQuestion(4, "CI/CD", 1.0),
        MockQuestion(5, "Programming Fundamentals", 1.0)
    ]
    answers = {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    
    assert result["overall_score"] == 100.0
    for dim, score in result["dimension_scores"].items():
        assert score == 100.0

def test_calculate_scores_all_min():
    questions = [
        MockQuestion(1, "JavaScript Fundamentals", 1.0),
        MockQuestion(2, "Backend Fundamentals", 1.0)
    ]
    answers = {"1": 1, "2": 1}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    
    assert result["overall_score"] == 0.0
    for score in result["dimension_scores"].values():
        assert score == 0.0

def test_calculate_scores_seniority_boost():
    # User has 6 YOE, question range 5-10
    questions = [
        MockQuestion(1, "JavaScript Fundamentals", 1.0, experience_min=5.0, experience_max=10.0),
        MockQuestion(2, "JavaScript Fundamentals", 1.0, experience_min=0.0, experience_max=2.0)
    ]
    # Ans 1 (Boosted 1.5x) = 100, Ans 2 (Normal 1.0x) = 0
    # Weighted Avg = (100 * 1.5 + 0 * 1.0) / (1.5 + 1.0) = 150 / 2.5 = 60
    answers = {"1": 4, "2": 1}
    
    result = ScoringEngine.calculate_scores(answers, questions, years_of_experience=6.0)
    
    assert result["dimension_scores"]["JavaScript Fundamentals"] == 60.0

def test_identify_weak_dimensions():
    scores = {
        "JavaScript Fundamentals": 80.0,
        "Backend Fundamentals": 50.0,
        "CI/CD": 60.0
    }
    
    weak = ScoringEngine.identify_weak_dimensions(scores, threshold=70.0)
    assert "Backend Fundamentals" in weak
    assert "CI/CD" in weak
    assert len(weak) == 2

def test_empty_answers():
    questions = [MockQuestion(1, "JavaScript Fundamentals", 1.0)]
    answers = {}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    assert result["overall_score"] == 0.0
    assert result["dimension_scores"] == {}

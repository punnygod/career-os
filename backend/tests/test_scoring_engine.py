import pytest
from services.scoring_engine import ScoringEngine
from models.question import Question

class MockQuestion:
    def __init__(self, id, dimension, weight):
        self.id = id
        self.dimension = dimension
        self.weight = weight

def test_calculate_scores_all_max():
    questions = [
        MockQuestion(1, "Core Technical Skills", 1.0),
        MockQuestion(2, "Architecture & Design", 1.0),
        MockQuestion(3, "Ownership & Impact", 1.0),
        MockQuestion(4, "Code Quality & Practices", 1.0),
        MockQuestion(5, "Communication & Influence", 1.0)
    ]
    answers = {"1": 4, "2": 4, "3": 4, "4": 4, "5": 4}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    
    assert result["overall_score"] == 100.0
    for dim in ScoringEngine.DIMENSIONS:
        assert result["dimension_scores"][dim] == 100.0

def test_calculate_scores_all_min():
    questions = [
        MockQuestion(1, "Core Technical Skills", 1.0),
        MockQuestion(2, "Architecture & Design", 1.0),
        MockQuestion(3, "Ownership & Impact", 1.0),
        MockQuestion(4, "Code Quality & Practices", 1.0),
        MockQuestion(5, "Communication & Influence", 1.0)
    ]
    answers = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    
    assert result["overall_score"] == 0.0
    for dim in ScoringEngine.DIMENSIONS:
        assert result["dimension_scores"][dim] == 0.0

def test_calculate_scores_mixed():
    questions = [
        MockQuestion(1, "Core Technical Skills", 1.0),
        MockQuestion(2, "Core Technical Skills", 2.0),
        MockQuestion(3, "Architecture & Design", 1.0)
    ]
    # Technical: (2*1.0 + 4*2.0) / 3.0 = 10.0 / 3.0 = 3.33...
    # (3.33 - 1) / 3 * 100 = 2.33 / 3 * 100 = 77.77...
    # Architecture: (1*1.0) / 1.0 = 1.0
    # (1.0 - 1) / 3 * 100 = 0
    answers = {"1": 2, "2": 4, "3": 1}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    
    technical_score = result["dimension_scores"]["Core Technical Skills"]
    assert pytest.approx(technical_score, 0.1) == 77.7
    assert result["dimension_scores"]["Architecture & Design"] == 0.0
    # Overall is average of ALL dimensions (5)
    # (77.7 + 0 + 0 + 0 + 0) / 5 = 15.54 -> rounded to 16
    assert result["overall_score"] == 16.0

def test_identify_weak_dimensions():
    scores = {
        "Core Technical Skills": 80.0,
        "Architecture & Design": 50.0,
        "Ownership & Impact": 90.0,
        "Code Quality & Practices": 60.0,
        "Communication & Influence": 85.0
    }
    
    weak = ScoringEngine.identify_weak_dimensions(scores, threshold=70.0)
    assert "Architecture & Design" in weak
    assert "Code Quality & Practices" in weak
    assert len(weak) == 2

def test_empty_answers():
    questions = [MockQuestion(1, "Core Technical Skills", 1.0)]
    answers = {}
    
    result = ScoringEngine.calculate_scores(answers, questions)
    assert result["overall_score"] == 0.0
    assert result["dimension_scores"]["Core Technical Skills"] == 0.0

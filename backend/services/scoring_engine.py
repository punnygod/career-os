from typing import Dict, List
from sqlalchemy.orm import Session
from models.question import Question


class ScoringEngine:
    """
    Core scoring engine that calculates weighted dimension scores
    and overall readiness score from assessment answers.
    """
    
    # The 5 core dimensions
    DIMENSIONS = [
        "Core Technical Skills",
        "Architecture & Design",
        "Ownership & Impact",
        "Code Quality & Practices",
        "Communication & Influence"
    ]
    
    @staticmethod
    def calculate_scores(
        answers: Dict[int, int],
        questions: List[Question]
    ) -> Dict[str, float]:
        """
        Calculate dimension scores and overall score from answers.
        
        Args:
            answers: Dictionary mapping question_id to answer value (1-4)
            questions: List of Question objects
            
        Returns:
            Dictionary with dimension scores and overall score
        """
        # Initialize dimension scores
        dimension_totals = {dim: 0.0 for dim in ScoringEngine.DIMENSIONS}
        dimension_weights = {dim: 0.0 for dim in ScoringEngine.DIMENSIONS}
        
        # Calculate weighted scores for each dimension
        for question in questions:
            question_id = str(question.id)
            if question_id in answers:
                answer_value = answers[question_id]
                weight = question.weight
                dimension = question.dimension
                
                # Add weighted score
                dimension_totals[dimension] += answer_value * weight
                dimension_weights[dimension] += weight
        
        # Calculate average scores for each dimension (0-100 scale)
        dimension_scores = {}
        for dimension in ScoringEngine.DIMENSIONS:
            if dimension_weights[dimension] > 0:
                # Calculate raw score (1-4)
                raw_score = dimension_totals[dimension] / dimension_weights[dimension]
                # Normalize to 0-100
                # Using (raw_score / 4) * 100 so that 1=25%, 2=50%, 3=75%, 4=100%
                dimension_scores[dimension] = (raw_score / 4) * 100
            else:
                dimension_scores[dimension] = 0.0
        
        # Calculate overall score (average of all dimensions)
        overall_score = sum(dimension_scores.values()) / len(ScoringEngine.DIMENSIONS)
        
        return {
            "dimension_scores": dimension_scores,
            "overall_score": round(overall_score, 0)
        }
    
    @staticmethod
    def identify_weak_dimensions(
        dimension_scores: Dict[str, float],
        threshold: float = 70.0
    ) -> List[str]:
        """
        Identify dimensions that are below the threshold.
        Returns the top 3 weakest dimensions, sorted by score.
        """
        # Sort by score ascending (weakest first)
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])
        
        # Filter by threshold and limit to top 3
        weak_dimensions = [
            dim for dim, score in sorted_dims 
            if score < threshold
        ]
        
        return weak_dimensions[:3]

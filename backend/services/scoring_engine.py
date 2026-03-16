from typing import Dict, List, Optional
import math
from models.question import Question


class ScoringEngine:
    """
    Core scoring engine that calculates weighted dimension scores,
    overall readiness score, and signal confidence from assessment answers.
    """
    
    @staticmethod
    def calculate_scores(
        answers: Dict[str, int],
        questions: List[Question],
        years_of_experience: float = 0.0
    ) -> Dict[str, any]:
        """
        Calculate dimension scores, overall score, and confidence signals.
        
        Features:
        - Weighted categories: 70% Core, 20% Stack, 10% Certifications.
        - Seniority-Aware Weighting: Questions aligned with user YOE get higher weight.
        - Confidence Engine: Calculates reliability of the signal.
        """
        # 1. Group questions by dimension
        dim_data = {}
        
        # Category totals for overall weighted score
        cat_scores = {"core": [], "stack": [], "cert": []}
        
        for question in questions:
            q_id_str = str(question.id)
            
            # Check if this question was answered
            answer_value = answers.get(q_id_str)
            if answer_value is not None:
                # Normalize raw answer (1-4) to 0-100
                score_100 = ((answer_value - 1) / 3.0) * 100
                
                # Seniority-Aware Weighting
                # If candidate YOE is within question range, boost impact by 1.5x
                seniority_multiplier = 1.0
                if question.experience_min <= years_of_experience <= question.experience_max:
                    seniority_multiplier = 1.5
                
                weight = (question.weight or 1.0) * seniority_multiplier
                dimension = question.dimension
                
                if dimension not in dim_data:
                    dim_data[dimension] = {"scores": [], "weights": []}
                
                dim_data[dimension]["scores"].append(score_100)
                dim_data[dimension]["weights"].append(weight)
                
                # Add to category scores
                if question.certificate_name:
                    cat_scores["cert"].append(score_100)
                elif question.stack_name:
                    cat_scores["stack"].append(score_100)
                else:
                    cat_scores["core"].append(score_100)
        
        # 2. Finalize dimension scores & confidence
        dimension_scores = {}
        dimension_confidences = {}
        
        for dimension, data in dim_data.items():
            scores = data["scores"]
            weights = data["weights"]
            
            # Weighted average
            weighted_sum = sum(s * w for s, w in zip(scores, weights))
            total_weight = sum(weights)
            dimension_scores[dimension] = weighted_sum / total_weight if total_weight > 0 else 0.0
            
            # Confidence Engine Logic
            # Sample Size (S): Max 40 points for 5+ questions
            sample_size_score = min(len(scores) * 8, 40)
            
            # Variance (V): Max 40 points for low variance
            # High variance across similar questions lowers confidence
            if len(scores) > 1:
                mean = sum(scores) / len(scores)
                variance = sum((x - mean) ** 2 for x in scores) / len(scores)
                std_dev = math.sqrt(variance)
                # 0 dev = 40 pts, 25 dev = 0 pts (threshold for inconsistent signals)
                variance_score = max(40 - (std_dev * 1.6), 0)
            else:
                variance_score = 10 # Low signal with 1 question
            
            # Categorical Mix (M): Max 20 points
            # (Future: boost if mixture of behavioral and technical present)
            mix_score = 20 if len(scores) > 2 else 10
            
            total_confidence = sample_size_score + variance_score + mix_score
            dimension_confidences[dimension] = "High" if total_confidence > 80 else "Medium" if total_confidence > 50 else "Low"

        # 3. Calculate Weighted Overall Score
        avg_core = sum(cat_scores["core"]) / len(cat_scores["core"]) if cat_scores["core"] else 0.0
        avg_stack = sum(cat_scores["stack"]) / len(cat_scores["stack"]) if cat_scores["stack"] else avg_core
        avg_cert = sum(cat_scores["cert"]) / len(cat_scores["cert"]) if cat_scores["cert"] else avg_core
        
        overall_score = (avg_core * 0.7) + (avg_stack * 0.2) + (avg_cert * 0.1)
        
        # Overall Confidence is average of dimensions
        # This is a simplification for the prototype
        return {
            "dimension_scores": dimension_scores,
            "dimension_confidences": dimension_confidences,
            "overall_score": round(overall_score, 0),
            "overall_confidence": "High" if len(cat_scores["core"]) >= 10 else "Medium" if len(cat_scores["core"]) >= 5 else "Low"
        }
    
    @staticmethod
    def identify_weak_dimensions(
        dimension_scores: Dict[str, float],
        threshold: float = 70.0
    ) -> List[str]:
        """Identify dimensions that are below the threshold."""
        if not dimension_scores:
            return []
        sorted_dims = sorted(dimension_scores.items(), key=lambda x: x[1])
        weak_dimensions = [dim for dim, score in sorted_dims if score < threshold]
        return weak_dimensions[:3]

    DIMENSION_GROUPS = {
        "Frontend": [
            "JavaScript Fundamentals", "Frontend Fundamentals", "State Management", 
            "Component Architecture", "Frontend System Design"
        ],
        "Backend": [
            "Backend Fundamentals", "Backend System Design", "API Design", "Databases",
            "Authentication & Authorization"
        ],
        "Cloud & Platform": [
            "Infrastructure as Code", "Cloud Platforms", "Containerization", 
            "Orchestration", "Monitoring & Logging", "Performance & Scalability",
            "Performance Optimization"
        ],
        "DevOps & Quality": [
            "CI/CD", "Automation & Scripting", "Security & Compliance", "Testing",
            "Code Quality & Engineering Practices"
        ],
        "Core Engineering": [
            "Programming Fundamentals", "Technical Decision Making", 
            "Problem Solving & Ambiguity Handling", "Architecture & Design Thinking"
        ],
        "Maturity & Soft Skills": [
            "Collaboration & Cross-Functional Communication", "Execution & Delivery Discipline", 
            "Learning & Skill Growth", "Mentorship & Knowledge Sharing", 
            "Ownership & Accountability", "Product & User Awareness"
        ]
    }

    @staticmethod
    def aggregate_scores_by_category(dimension_scores: Dict[str, float]) -> Dict[str, float]:
        """Aggregate specific dimensions into high-level categories."""
        category_scores = {}
        for category, dims in ScoringEngine.DIMENSION_GROUPS.items():
            scores = [dimension_scores.get(dim) for dim in dims if dim in dimension_scores]
            if scores:
                category_scores[category] = sum(scores) / len(scores)
        return category_scores

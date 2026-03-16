from typing import Optional, Dict, List
from datetime import datetime
from sqlalchemy.orm import Session
from models.benchmark import Benchmark


class BenchmarkEngine:
    """
    Benchmark comparison engine that matches user profile to benchmark data,
    determines readiness, and calculates data reliability.
    """
    
    @staticmethod
    def find_matching_benchmark(
        db: Session,
        role_id: int,
        years_of_experience: float,
        company_type: str,
        target_level: Optional[str] = None,
        location: Optional[str] = None,
        tech_stack: Optional[List[str]] = None
    ) -> Optional[Benchmark]:
        """
        Find the best matching benchmark for the given profile with dual-matching logic.
        """
        # Base query using experience_min/max
        base_query = db.query(Benchmark).filter(
            Benchmark.role_id == role_id,
            Benchmark.company_type == company_type.lower(),
            Benchmark.experience_min <= years_of_experience,
            Benchmark.experience_max >= years_of_experience
        )
        
        # Dual-Matching Logic: Prioritize target_level if provided
        if target_level:
            # Try exact match
            result = base_query.filter(Benchmark.target_level == target_level).first()
            if result:
                return result
            
            # Try partial match
            levels = ["Junior", "Mid-level", "Senior", "Lead", "Staff", "Principal"]
            for level in levels:
                if level.lower() in target_level.lower():
                    result = base_query.filter(Benchmark.target_level == level).first()
                    if result:
                        return result
            
        # 1. Exact Match (Location + Tech)
        if location and tech_stack:
            for tech in tech_stack:
                match = base_query.filter(
                    Benchmark.location == location,
                    Benchmark.tech_stack == tech
                ).first()
                if match: return match
                    
        # 2. Location Match
        if location:
            match = base_query.filter(Benchmark.location == location).first()
            if match: return match
                
        # 3. Tech Match
        if tech_stack:
            for tech in tech_stack:
                match = base_query.filter(Benchmark.tech_stack == tech).first()
                if match: return match
                    
        # 4. Fallback to general benchmark
        return base_query.first()
    
    @staticmethod
    def calculate_reliability_index(benchmark: Benchmark) -> Dict[str, any]:
        """
        Calculate Benchmark Reliability Index based on freshness and source diversity.
        """
        if not benchmark:
            return {"score": 0.0, "level": "Unknown", "source_count": 0}
            
        # Freshness Weight (max 0.5)
        current_year = datetime.now().year
        year_diff = current_year - (benchmark.year or 2024)
        if year_diff <= 0: freshness = 0.5
        elif year_diff == 1: freshness = 0.4
        elif year_diff == 2: freshness = 0.2
        else: freshness = 0.1
        
        # Source Diversity (max 0.5)
        sources = benchmark.source.split(";") if benchmark.source else []
        source_count = len(sources)
        diversity = min(source_count * 0.17, 0.5) # 3+ sources = 0.5 pts
        
        score = freshness + diversity
        level = "High" if score > 0.8 else "Medium" if score > 0.5 else "Low"
        
        return {
            "score": round(score, 2),
            "level": level,
            "source_count": source_count,
            "is_fresh": year_diff <= 1,
            "sources": sources
        }

    @staticmethod
    def determine_readiness(overall_score: float, benchmark: Benchmark) -> str:
        """Determine readiness level based on score and benchmark thresholds."""
        if not benchmark: return "Unknown"
        if overall_score >= benchmark.ready_threshold:
            return "Ready"
        elif overall_score >= benchmark.near_ready_threshold:
            return "Near Ready"
        else:
            return "Not Ready"
    
    @staticmethod
    def get_expected_salary_range(benchmark: Benchmark) -> Dict[str, any]:
        """Get enhanced salary range including median and reliability."""
        if not benchmark: return {}
        reliability = BenchmarkEngine.calculate_reliability_index(benchmark)
        return {
            "min": benchmark.salary_min,
            "max": benchmark.salary_max,
            "median": (benchmark.salary_min + benchmark.salary_max) / 2,
            "reliability": reliability,
            "currency": "INR"
        }

    @staticmethod
    def get_next_level_benchmark(db: Session, current_benchmark: Benchmark) -> Optional[Benchmark]:
        """Fetch benchmark for the level immediately above."""
        levels = ["Junior", "Mid-level", "Senior", "Lead", "Staff", "Principal"]
        try:
            current_idx = levels.index(current_benchmark.target_level)
            if current_idx + 1 < len(levels):
                next_level = levels[current_idx + 1]
                return db.query(Benchmark).filter(
                    Benchmark.role_id == current_benchmark.role_id,
                    Benchmark.company_type == current_benchmark.company_type,
                    Benchmark.target_level == next_level
                ).first()
        except (ValueError, AttributeError):
            pass
        return None

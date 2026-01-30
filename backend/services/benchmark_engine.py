from typing import Optional, Dict, List
from sqlalchemy.orm import Session
from models.benchmark import Benchmark


class BenchmarkEngine:
    """
    Benchmark comparison engine that matches user profile to benchmark data
    and determines readiness level.
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
        Find the best matching benchmark for the given profile.
        
        Args:
            db: Database session
            role_id: Role ID
            years_of_experience: Years of experience
            company_type: Company type (service, startup, product)
            target_level: Target level (e.g., "Senior", "Lead")
            location: Optional location filter
            tech_stack: Optional list of technologies
            
        Returns:
            Matching Benchmark object or None
        """
        # Base query
        base_query = db.query(Benchmark).filter(
            Benchmark.role_id == role_id,
            Benchmark.company_type == company_type.lower(),
            Benchmark.yoe_min <= years_of_experience,
            Benchmark.yoe_max >= years_of_experience
        )
        
        # Try with target_level filter first if provided
        if target_level:
            # Try exact match first
            exact_level_query = base_query.filter(Benchmark.target_level == target_level)
            result = exact_level_query.first()
            if result:
                return result
            
            # Try partial match (e.g., "Senior Software" contains "Senior")
            for level in ["Junior", "Mid-level", "Senior", "Lead", "Staff", "Principal"]:
                if level.lower() in target_level.lower():
                    partial_match_query = base_query.filter(Benchmark.target_level == level)
                    result = partial_match_query.first()
                    if result:
                        return result
            
        # 1. Try to find an exact match (Location + Tech)
        if location and tech_stack:
            for tech in tech_stack:
                exact_match = base_query.filter(
                    Benchmark.location == location,
                    Benchmark.tech_stack == tech
                ).first()
                if exact_match:
                    return exact_match
                    
        # 2. Try to find location match only
        if location:
            location_match = base_query.filter(Benchmark.location == location).first()
            if location_match:
                return location_match
                
        # 3. Try to find tech match only
        if tech_stack:
            for tech in tech_stack:
                tech_match = base_query.filter(Benchmark.tech_stack == tech).first()
                if tech_match:
                    return tech_match
                    
        # 4. Fallback to general benchmark (without target_level filter)
        return base_query.first()
    
    @staticmethod
    def determine_readiness(
        overall_score: float,
        benchmark: Benchmark
    ) -> str:
        """
        Determine readiness level based on score and benchmark thresholds.
        
        Args:
            overall_score: Overall assessment score (1-4 scale)
            benchmark: Benchmark object with thresholds
            
        Returns:
            Readiness level: "Ready", "Near Ready", or "Not Ready"
        """
        if overall_score >= benchmark.ready_threshold:
            return "Ready"
        elif overall_score >= benchmark.near_ready_threshold:
            return "Near Ready"
        else:
            return "Not Ready"
    
    @staticmethod
    def get_expected_salary_range(benchmark: Benchmark) -> Dict[str, float]:
        """
        Get expected salary range from benchmark.
        
        Args:
            benchmark: Benchmark object
            
        Returns:
            Dictionary with min and max salary
        """
        return {
            "min": benchmark.salary_min,
            "max": benchmark.salary_max,
            "median": (benchmark.salary_min + benchmark.salary_max) / 2
        }

    @staticmethod
    def get_next_level_benchmark(db: Session, current_benchmark: Benchmark) -> Optional[Benchmark]:
        """
        Fetch the benchmark for the level immediately above the current one.
        """
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
        except ValueError:
            pass
        return None

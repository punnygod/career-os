from typing import Optional, Dict


class SalaryAnalyzer:
    """
    Enhanced Salary Alignment engine that considers technical stack, 
    professional maturity, and data reliability.
    """
    
    @staticmethod
    def get_maturity_multiplier(behavioral_score: float) -> float:
        """
        Calculate salary premium based on professional maturity (soft skills).
        """
        if behavioral_score >= 90: return 1.20
        if behavioral_score >= 80: return 1.15
        if behavioral_score >= 70: return 1.07
        if behavioral_score >= 60: return 1.03
        return 1.0
    
    @staticmethod
    def analyze_salary(
        current_salary: Optional[float],
        expected_min: float,
        expected_max: float,
        stack_multiplier: float = 1.0,
        cert_multiplier: float = 1.0,
        behavioral_score: float = 0.0,
        reliability_weight: float = 1.0
    ) -> Dict[str, any]:
        """
        Determine salary alignment with professional maturity and reliability weighting.
        """
        if current_salary is None:
            return {"status": "Unknown", "adjusted_range": None}
            
        maturity_multiplier = SalaryAnalyzer.get_maturity_multiplier(behavioral_score)
        
        # Combined Market Multiplier
        # Note: Reliability weight affects the 'confidence' of the range rather than the value itself
        # but we use it to show directional bias.
        total_multiplier = stack_multiplier * cert_multiplier * maturity_multiplier
        
        adj_min = expected_min * total_multiplier
        adj_max = expected_max * total_multiplier
        adj_median = (adj_min + adj_max) / 2
        
        status = "Aligned"
        if current_salary < adj_min:
            status = "Underpaid"
        elif current_salary < adj_median * 0.95:
            status = "Under-indexed"
        elif current_salary > adj_max:
            status = "Market Leader"
        elif current_salary > adj_median * 1.05:
            status = "Optimized"
            
        return {
            "status": status,
            "current": current_salary,
            "market_median": round(adj_median, 0),
            "market_range": {"min": round(adj_min, 0), "max": round(adj_max, 0)},
            "multipliers": {
                "stack": stack_multiplier,
                "certification": cert_multiplier,
                "maturity": maturity_multiplier
            },
            "data_reliability": reliability_weight
        }
    
    @staticmethod
    def get_salary_gap(
        current_salary: Optional[float],
        expected_median: float,
        stack_multiplier: float = 1.0,
        cert_multiplier: float = 1.0,
        behavioral_score: float = 0.0
    ) -> Optional[float]:
        """
        Calculate potential annual gap relative to adjusted market median.
        """
        if current_salary is None:
            return None
            
        maturity_multiplier = SalaryAnalyzer.get_maturity_multiplier(behavioral_score)
        adj_median = expected_median * stack_multiplier * cert_multiplier * maturity_multiplier
        
        if current_salary < adj_median:
            return round(adj_median - current_salary, 0)
        return 0.0

    @staticmethod
    def get_market_percentile(current_salary: Optional[float], salary_min: float, salary_max: float) -> Optional[int]:
        """
        Estimate market percentile based on salary range.
        Uses linear interpolation between 10th and 90th percentile.
        """
        if current_salary is None or salary_max <= salary_min:
            return None
        
        if current_salary <= salary_min: return 10
        if current_salary >= salary_max: return 90
            
        range_percent = (current_salary - salary_min) / (salary_max - salary_min)
        percentile = 10 + round(range_percent * 80)
        return min(max(percentile, 1), 99)

    @staticmethod
    def calculate_roi(current_salary: Optional[float], target_salary: float) -> Optional[float]:
        """
        Calculate % upside from current salary to target salary.
        """
        if current_salary is None or current_salary <= 0:
            return None
        return round(((target_salary - current_salary) / current_salary) * 100, 1)

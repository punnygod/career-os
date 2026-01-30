from typing import Optional


class SalaryAnalyzer:
    """
    Salary alignment calculator that compares user's current salary
    with benchmark range.
    """
    
    @staticmethod
    def analyze_salary(
        current_salary: Optional[float],
        expected_min: float,
        expected_max: float
    ) -> str:
        """
        Determine salary alignment status.
        
        Args:
            current_salary: User's current salary (can be None)
            expected_min: Expected minimum salary from benchmark
            expected_max: Expected maximum salary from benchmark
            
        Returns:
            Alignment status: "Underpaid", "Fair", "Overpaid", or "Unknown"
        """
        if current_salary is None:
            return "Unknown"
        
        # Calculate median and tolerance ranges
        median = (expected_min + expected_max) / 2
        
        # Underpaid: below minimum
        if current_salary < expected_min:
            return "Underpaid"
        
        # Overpaid: above maximum
        elif current_salary > expected_max:
            return "Overpaid"
        
        # Fair: within range
        else:
            return "Fair"
    
    @staticmethod
    def get_salary_gap(
        current_salary: Optional[float],
        expected_min: float,
        expected_max: float
    ) -> Optional[float]:
        """
        Calculate salary gap (positive if underpaid, negative if overpaid).
        
        Args:
            current_salary: User's current salary
            expected_min: Expected minimum salary
            expected_max: Expected maximum salary
            
        Returns:
            Salary gap amount or None if current salary is unknown
        """
        if current_salary is None:
            return None
        
        median = (expected_min + expected_max) / 2
        
        if current_salary < expected_min:
            # Underpaid: gap to minimum
            return expected_min - current_salary
        elif current_salary > expected_max:
            # Overpaid: gap from maximum (negative)
            return expected_max - current_salary
        else:
            # Fair: no significant gap
            return 0.0

    @staticmethod
    def calculate_roi(current_salary: Optional[float], expected_median: float) -> Optional[float]:
        """
        Calculate potential ROI (annual salary increase) if user reaches benchmark.
        """
        if current_salary is None:
            return None
        
        if current_salary < expected_median:
            return expected_median - current_salary
        return 0.0

    @staticmethod
    def get_market_percentile(current_salary: Optional[float], salary_min: float, salary_max: float) -> Optional[int]:
        """
        Estimate market percentile based on salary range.
        SImulated using a simple linear interpolation.
        """
        if current_salary is None:
            return None
        
        if current_salary <= salary_min:
            return 10
        if current_salary >= salary_max:
            return 90
            
        # Linear interpolation between 10th and 90th percentile
        range_percent = (current_salary - salary_min) / (salary_max - salary_min)
        percentile = 10 + round(range_percent * 80)
        return min(max(percentile, 1), 99)

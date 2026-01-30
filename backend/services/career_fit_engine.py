from typing import Dict


class CareerFitEngine:
    """
    Company fit recommendation engine that analyzes dimension scores
    to suggest best company type fit.
    """
    
    @staticmethod
    def determine_company_fit(dimension_scores: Dict[str, float]) -> str:
        """
        Determine best company type fit based on dimension scores.
        
        Logic:
        - Service companies: Strong in code quality, technical skills
        - Startups: Strong in ownership, impact, adaptability
        - Product companies: Strong in architecture, design, communication
        
        Args:
            dimension_scores: Dictionary of dimension scores
            
        Returns:
            Best fit company type: "service", "startup", or "product"
        """
        # Extract relevant scores
        technical = dimension_scores.get("Core Technical Skills", 0)
        architecture = dimension_scores.get("Architecture & Design", 0)
        ownership = dimension_scores.get("Ownership & Impact", 0)
        code_quality = dimension_scores.get("Code Quality & Practices", 0)
        communication = dimension_scores.get("Communication & Influence", 0)
        
        # Calculate fit scores for each company type
        service_score = (technical * 1.5 + code_quality * 1.5 + architecture) / 4
        startup_score = (ownership * 2 + technical + communication) / 4
        product_score = (architecture * 1.5 + communication * 1.5 + ownership) / 4
        
        # Determine best fit
        fit_scores = {
            "service": service_score,
            "startup": startup_score,
            "product": product_score
        }
        
        best_fit = max(fit_scores, key=fit_scores.get)
        
        return best_fit
    
    @staticmethod
    def get_fit_explanation(company_type: str) -> str:
        """
        Get explanation for why a company type is recommended.
        
        Args:
            company_type: Company type (service, startup, product)
            
        Returns:
            Explanation text
        """
        explanations = {
            "service": (
                "Your strong technical skills and code quality practices make you "
                "well-suited for service companies where delivering high-quality "
                "solutions for clients is paramount."
            ),
            "startup": (
                "Your ownership mindset and impact-driven approach align well with "
                "startup environments where you can take initiative and drive "
                "significant results with limited resources."
            ),
            "product": (
                "Your architectural thinking and communication skills make you a "
                "great fit for product companies where designing scalable systems "
                "and collaborating across teams is essential."
            )
        }
        
        return explanations.get(company_type, "")

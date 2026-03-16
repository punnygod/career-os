from typing import Dict, List, Tuple
from services.scoring_engine import ScoringEngine


class CareerFitEngine:
    """
    Enhanced Company Fit engine that analyzes cross-dimension signals
    to suggest company fit and detect potential career friction.
    """
    
    @staticmethod
    def determine_company_fit(dimension_scores: Dict[str, float]) -> Dict[str, any]:
        """
        Determine best company type fit and detect career friction risks.
        """
        # 1. Aggregate scores by high-level category
        categories = ScoringEngine.aggregate_scores_by_category(dimension_scores)
        
        frontend = categories.get("Frontend", 0)
        backend = categories.get("Backend", 0)
        cloud = categories.get("Cloud & Platform", 0)
        devops = categories.get("DevOps & Quality", 0)
        core = categories.get("Core Engineering", 0)
        maturity = categories.get("Maturity & Soft Skills", 0)
        
        # 2. Calculate fit scores
        # Service: Quality + Fundamentals
        service_score = (devops * 1.5 + core * 1.5 + (frontend + backend) / 2) / 4
        
        # Startup: Ownership + Execution + Core
        startup_score = (maturity * 2.2 + core + (frontend + backend) / 2) / 4.2
        
        # Product: Architecture + Maturity + Backend/Frontend
        product_score = (core * 1.5 + maturity * 1.5 + (frontend + backend) / 2) / 4
        
        # Big Tech / Enterprise: Architecture + Cloud + Communication + DevOps
        enterprise_score = (core * 1.5 + cloud * 1.2 + devops * 1.2 + maturity) / 4.9
        
        fit_scores = {
            "service": service_score,
            "startup": startup_score,
            "product": product_score,
            "enterprise": enterprise_score
        }
        
        best_fit = max(fit_scores, key=fit_scores.get)
        
        # 3. Detect Career Friction Signals (Mismatch Detector)
        risk_flags = CareerFitEngine._detect_friction(categories)
        
        return {
            "best_fit": best_fit,
            "fit_scores": fit_scores,
            "risk_flags": risk_flags,
            "explanation": CareerFitEngine.get_fit_explanation(best_fit)
        }
    
    @staticmethod
    def _detect_friction(categories: Dict[str, float]) -> List[str]:
        """
        Identify anti-patterns and career blockers using cross-dimension analysis.
        """
        flags = []
        
        core = categories.get("Core Engineering", 0)
        maturity = categories.get("Maturity & Soft Skills", 0)
        tech_avg = (categories.get("Frontend", 0) + categories.get("Backend", 0)) / 2
        
        # Flag 1: Growth Bottleneck (High tech, Low communication/maturity)
        if tech_avg > 80 and maturity < 60:
            flags.append("Growth Bottleneck: High technical skill but lower professional maturity may block senior/lead role progression.")
            
        # Flag 2: Execution Gap (High maturity, Low core skills)
        if maturity > 80 and core < 60:
            flags.append("Execution Gap: Strong leadership and ownership mindset, but foundational engineering depth needs strengthening.")
            
        # Flag 3: Staff Ceiling Risk (High Architecture/Core, Low Product Awareness)
        # Note: In our mapping, Core includes Architecture & Design Thinking
        if core > 85 and maturity < 65:
            flags.append("Staff Ceiling Risk: Strong architectural thinking but needs better cross-functional communication and user awareness.")
            
        # Flag 4: Specialist vs Generalist tension
        frontend = categories.get("Frontend", 0)
        backend = categories.get("Backend", 0)
        if abs(frontend - backend) > 40:
            role = "Frontend" if frontend > backend else "Backend"
            flags.append(f"Highly Specialized: Strong {role} focus. Transitioning to full-stack or platform roles will require significant cross-training.")

        return flags

    @staticmethod
    def get_fit_explanation(company_type: str) -> str:
        """Get explanation for why a company type is recommended."""
        explanations = {
            "service": (
                "Your focus on engineering practices and quality makes you a great fit for "
                "service-based organizations where delivering robust, client-specific solutions is key."
            ),
            "startup": (
                "Your high level of ownership and bias for action align perfectly with "
                "fast-paced startup environments where individual impact is maximized."
            ),
            "product": (
                "Your balance of technical depth and product awareness makes you ideal for "
                "product companies focusing on long-term scalability and user value."
            ),
            "enterprise": (
                "Your strength in architecture, cloud infrastructure, and organizational maturity "
                "is well-suited for large-scale engineering organizations and Big Tech."
            )
        }
        return explanations.get(company_type, "Recommended based on your balanced dimension profile.")

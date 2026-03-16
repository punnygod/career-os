from typing import List, Optional, Dict, Any
import math


class RoadmapGenerator:
    """
    Enhanced Roadmap Generator that creates phase-based progression paths,
    calculates financial milestones, and signals career switch readiness.
    """
    
    # Enhanced Phase-Based Templates
    PHASE_TEMPLATES = {
        "Foundation Fixes": [
            "Audit your current codebase for technical debt in {dimension}",
            "Fix 3 high-priority bugs or performance issues related to {dimension}",
            "Complete a tutorial or read documentation on {dimension} fundamentals"
        ],
        "Technical Mastery": [
            "Implement a complex feature using advanced {dimension} patterns",
            "Perform a deep-dive performance optimization on a core module",
            "Contribute a significant improvement to your team's common library"
        ],
        "Strategic Influence": [
            "Lead a design review for a new system component",
            "Mentor a junior engineer on {dimension} best practices",
            "Draft an RFC or technical vision for long-term {dimension} improvements"
        ]
    }

    @staticmethod
    def generate_enhanced_roadmap(
        assessment_data: Dict[str, Any],
        benchmark_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive career roadmap with financial and switch signals.
        """
        dim_scores = assessment_data.get("dimension_scores", {})
        overall_score = assessment_data.get("overall_score", 0)
        yoe = assessment_data.get("years_of_experience", 0)
        current_salary = assessment_data.get("current_salary")
        
        # 1. Identify Target Level and Readiness
        readiness = assessment_data.get("readiness_level", "Unknown")
        switch_readiness = "Yellow"
        if readiness == "Ready":
            switch_readiness = "Green"
        elif readiness == "Not Ready":
            switch_readiness = "Red"
            
        # 2. Financial Projections
        financials = {"potential_growth_pct": 0.0, "target_range": None}
        if current_salary and benchmark_data:
            p75 = benchmark_data.get("max", 0) # Using max as p75 proxy for now
            if p75 > current_salary:
                growth = ((p75 - current_salary) / current_salary) * 100
                financials["potential_growth_pct"] = round(growth, 1)
                financials["target_range"] = benchmark_data
        
        # 3. Phase-Based Milestones
        weak_dims = [d for d, s in dim_scores.items() if s < 70][:3]
        milestones = []
        
        # Foundation Phase
        if weak_dims:
            milestones.append({
                "phase": "Foundation Fixes",
                "duration": "1 Month",
                "items": [{"topic": d, "action": RoadmapGenerator.PHASE_TEMPLATES["Foundation Fixes"][0].format(dimension=d)} for d in weak_dims]
            })
            
        # Mastery Phase
        strong_dims = [d for d, s in dim_scores.items() if 70 <= s < 90][:2]
        if strong_dims:
            milestones.append({
                "phase": "Technical Mastery",
                "duration": "2-3 Months",
                "items": [{"topic": d, "action": RoadmapGenerator.PHASE_TEMPLATES["Technical Mastery"][0].format(dimension=d)} for d in strong_dims]
            })

        # Influence Phase (Maturity Focus)
        maturity_score = assessment_data.get("maturity_score", 0)
        if maturity_score < 90:
            milestones.append({
                "phase": "Strategic Influence",
                "duration": "Ongoing",
                "items": [{"topic": "Engineering Maturity", "action": RoadmapGenerator.PHASE_TEMPLATES["Strategic Influence"][0].format(dimension="Core")}]
            })

        return {
            "career_path": {
                "current_role": assessment_data.get("role_name", "Developer"),
                "target_level": assessment_data.get("target_level", "Next Level"),
                "estimated_timeline": "4-6 Months" if readiness != "Ready" else "1-2 Months",
                "switch_readiness": switch_readiness,
                "overall_confidence": assessment_data.get("overall_confidence", "Medium"),
                "dimension_confidences": assessment_data.get("dimension_confidences", {}),
                "risk_flags": assessment_data.get("risk_flags", [])
            },
            "financial_projection": financials,
            "milestones": milestones,
            "study_plan": RoadmapGenerator._get_study_plan(weak_dims)
        }

    @staticmethod
    def _get_study_plan(dims: List[str]) -> List[Dict[str, str]]:
        resources = []
        for d in dims:
            resources.append({"topic": d, "resource": f"Advanced Guide to {d}", "priority": "P0"})
        return resources[:3]
        
    # Keep old methods for backward compatibility if needed, 
    # but the API should switch to the enhanced one.
    @staticmethod
    def generate_roadmap(
        weak_dimensions: List[str],
        tech_stack: Optional[List[str]] = None
    ) -> Dict[str, List[Dict]]:
        # Placeholder for old logic
        return {}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from pydantic import BaseModel

from database import get_db
from models.assessment import Assessment
from models.benchmark import Benchmark
from models.question import Question
from services.scoring_engine import ScoringEngine
from services.benchmark_engine import BenchmarkEngine
from services.roadmap_generator import RoadmapGenerator


router = APIRouter(prefix="/api/report", tags=["report"])


class DimensionScore(BaseModel):
    dimension: str
    category: str
    score: float
    benchmark_score: float
    status: str  # "strong", "adequate", "weak"


class SalaryInfo(BaseModel):
    current: Optional[float]
    expected_min: float
    expected_max: float
    expected_median: float
    alignment: str
    gap: Optional[float]
    potential_roi: Optional[float]
    market_percentile: Optional[int]


class RadarChartItem(BaseModel):
    dimension: str
    user_score: float
    benchmark_score: float

class LearningResource(BaseModel):
    title: str
    type: str
    url: str

class NextLevelPreview(BaseModel):
    target_role: str
    target_level: str
    salary_min: float
    salary_max: float

class CareerReportResponse(BaseModel):
    assessment_id: int
    overall_score: float
    readiness_level: str
    dimension_scores: List[DimensionScore]
    salary_info: Optional[SalaryInfo]
    company_fit: str
    company_fit_explanation: str
    weak_dimensions: List[str]
    quick_wins: List[str]
    radar_chart_data: List[RadarChartItem]
    interview_questions: List[str]
    learning_resources: List[LearningResource]
    next_level_preview: Optional[NextLevelPreview] = None
    # Contextual info
    location: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    current_level: Optional[str] = None


class WeeklyTasks(BaseModel):
    week: int
    tasks: List[str]


class RoadmapResponse(BaseModel):
    assessment_id: int
    roadmap: Dict[str, List[WeeklyTasks]]


@router.get("/{assessment_id}", response_model=CareerReportResponse)
def get_report(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get complete career report for an assessment.
    """
    from services.salary_analyzer import SalaryAnalyzer
    from services.career_fit_engine import CareerFitEngine
    
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if not assessment.is_complete:
        raise HTTPException(status_code=400, detail="Assessment not completed")
    
    # Get salary info if benchmark exists
    salary_info = None
    radar_chart_data = []
    next_level_preview = None
    readiness_level = assessment.readiness_level
    
    benchmark = BenchmarkEngine.find_matching_benchmark(
        db,
        assessment.role_id,
        assessment.years_of_experience,
        assessment.company_type,
        assessment.target_role,
        location=assessment.location,
        tech_stack=assessment.tech_stack
    )
    
    # Re-calculate scores live using latest engine logic (including role 0)
    from sqlalchemy import or_
    questions = db.query(Question).filter(
        or_(
            Question.role_id == assessment.role_id,
            Question.role_id == 0
        )
    ).all()
    scores = ScoringEngine.calculate_scores(assessment.answers, questions)
    dimension_scores = scores["dimension_scores"]
    overall_score = scores["overall_score"]

    # Identify weak dimensions for growth insights
    weak_dimensions = ScoringEngine.identify_weak_dimensions(
        dimension_scores, # Changed from assessment.dimension_scores
        threshold=70.0  # Normalized 0-100 threshold
    )
    
    # Format detailed dimension scores list
    dimension_scores_list = []
    benchmark_val = benchmark.ready_threshold if benchmark else 80.0
    
    for dimension, score in dimension_scores.items():
        # Find category for this dimension
        category = "Other"
        for cat, dims in ScoringEngine.DIMENSION_GROUPS.items():
            if dimension in dims:
                category = cat
                break
                
        status = "strong" if score >= 85 else "adequate" if score >= 70 else "weak"
        dimension_scores_list.append(DimensionScore(
            dimension=dimension,
            category=category,
            score=score,
            benchmark_score=benchmark_val,
            status=status
        ))
    
    # Generate aggregated category scores for Radar Chart
    category_scores = ScoringEngine.aggregate_scores_by_category(dimension_scores)
    for category, score in category_scores.items():
        radar_chart_data.append(RadarChartItem(
            dimension=category,
            user_score=score,
            benchmark_score=benchmark_val
        ))
    
    if benchmark:
        # Extension: Fetch multipliers (Handle multiple stacks/certs)
        from services.stack_module import StackExtensionModule
        from services.certification_module import CertificationExtensionModule
        
        stack_multiplier = 1.0
        # Defensive check: ensure tech_stack is a list if it comes as a JSON string
        ts = assessment.tech_stack
        if isinstance(ts, str):
            import json
            try: ts = json.loads(ts)
            except: ts = []
            
        if ts and isinstance(ts, list):
            multipliers = [StackExtensionModule.get_stack_multiplier(db, s) for s in ts]
            stack_multiplier = max(multipliers) if multipliers else 1.0
        elif assessment.primary_stack:
            stack_multiplier = StackExtensionModule.get_stack_multiplier(db, assessment.primary_stack)

        cert_multiplier = CertificationExtensionModule.get_certificate_multiplier(db, assessment.certifications)
        
        salary_range = BenchmarkEngine.get_expected_salary_range(benchmark)
        
        # Apply multipliers to the range for display
        adj_min = salary_range["min"] * stack_multiplier * cert_multiplier
        adj_max = salary_range["max"] * stack_multiplier * cert_multiplier
        adj_median = salary_range["median"] * stack_multiplier * cert_multiplier

        # Detailed alignment analysis (internal), but expose only status string in API
        alignment_details = SalaryAnalyzer.analyze_salary(
            assessment.current_salary,
            salary_range["min"],
            salary_range["max"],
            stack_multiplier=stack_multiplier,
            cert_multiplier=cert_multiplier,
            behavioral_score=category_scores.get("Maturity & Soft Skills", 0),
            reliability_weight=reliability["score"],
        )

        salary_gap = SalaryAnalyzer.get_salary_gap(
            assessment.current_salary,
            salary_range["median"],
            stack_multiplier=stack_multiplier,
            cert_multiplier=cert_multiplier,
            behavioral_score=category_scores.get("Maturity & Soft Skills", 0),
        )
        potential_roi = SalaryAnalyzer.calculate_roi(assessment.current_salary, adj_median)
        market_percentile = SalaryAnalyzer.get_market_percentile(
            assessment.current_salary,
            adj_min,
            adj_max
        )
        
        salary_info = SalaryInfo(
            current=assessment.current_salary,
            expected_min=adj_min,
            expected_max=adj_max,
            expected_median=adj_median,
            alignment=alignment_details["status"],
            gap=salary_gap,
            potential_roi=potential_roi,
            market_percentile=market_percentile
        )
        
        # Readiness level re-calculation (in case benchmarks changed or scores were adjusted)
        readiness_level = BenchmarkEngine.determine_readiness(
            overall_score, # Changed from assessment.overall_score
            benchmark
        )
        
        # Next level preview
        next_benchmark = BenchmarkEngine.get_next_level_benchmark(db, benchmark)
        if next_benchmark:
            next_level_preview = NextLevelPreview(
                target_role=assessment.target_role or "Engineer",
                target_level=next_benchmark.target_level,
                salary_min=next_benchmark.salary_min,
                salary_max=next_benchmark.salary_max
            )
    
    quick_wins = RoadmapGenerator.get_quick_wins(
        weak_dimensions,
        tech_stack=assessment.tech_stack
    )
    
    interview_questions = RoadmapGenerator.get_interview_questions(weak_dimensions)
    learning_resources = RoadmapGenerator.get_learning_resources(weak_dimensions)
    
    # Get company fit explanation
    company_fit_explanation = CareerFitEngine.get_fit_explanation(
        assessment.company_fit
    )
    
    return CareerReportResponse(
        assessment_id=assessment.id,
        overall_score=overall_score,
        readiness_level=readiness_level,
        dimension_scores=dimension_scores_list,
        salary_info=salary_info,
        company_fit=assessment.company_fit,
        company_fit_explanation=company_fit_explanation,
        weak_dimensions=weak_dimensions,
        quick_wins=quick_wins,
        radar_chart_data=radar_chart_data,
        interview_questions=interview_questions,
        learning_resources=learning_resources,
        next_level_preview=next_level_preview,
        location=assessment.location,
        tech_stack=assessment.tech_stack,
        current_level=assessment.current_level
    )


@router.get("/{assessment_id}/roadmap", response_model=RoadmapResponse)
def get_roadmap(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get personalized roadmap for an assessment.
    """
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if not assessment.is_complete:
        raise HTTPException(status_code=400, detail="Assessment not completed")
    
    # Identify weak dimensions (using 0-100 threshold)
    weak_dimensions = ScoringEngine.identify_weak_dimensions(
        assessment.dimension_scores,
        threshold=70.0
    )
    
    # Generate roadmap
    roadmap_data = RoadmapGenerator.generate_roadmap(
        weak_dimensions,
        tech_stack=assessment.tech_stack
    )
    
    # Format response
    formatted_roadmap = {}
    for dimension, weeks in roadmap_data.items():
        formatted_roadmap[dimension] = [
            WeeklyTasks(week=week_data["week"], tasks=week_data["tasks"])
            for week_data in weeks
        ]
    
    return RoadmapResponse(
        assessment_id=assessment.id,
        roadmap=formatted_roadmap
    )

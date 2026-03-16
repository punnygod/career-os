from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, List, Any
from datetime import datetime
import uuid
from pydantic import BaseModel

from database import get_db
from models.assessment import Assessment
from models.question import Question
from models.role import Role
from models.user import User
from routes.auth import get_current_user


router = APIRouter(prefix="/api/assessment", tags=["assessment"])


class StartAssessmentRequest(BaseModel):
    role_id: int
    years_of_experience: float
    company_type: str
    current_salary: Optional[float] = None
    target_role: Optional[str] = None
    # user_id is now derived from the authenticated user and is kept only for backward compatibility
    user_id: Optional[int] = None
    location: Optional[str] = None
    primary_stack: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    certifications: Optional[List[str]] = None
    current_level: Optional[str] = None


class StartAssessmentResponse(BaseModel):
    assessment_id: int
    session_id: Optional[str]
    message: str


class QuestionResponse(BaseModel):
    id: int
    dimension: str
    question_text: str
    question_order: int
    answer_options: Dict[int, str]
    is_behavioral: int
    
    class Config:
        from_attributes = True


class SubmitAnswersRequest(BaseModel):
    answers: Dict[str, int]  # question_id: answer_value (keys as strings for JSON)


class RoadmapResponse(BaseModel):
    career_path: Dict[str, Any]
    financial_projection: Dict[str, Any]
    milestones: List[Dict[str, Any]]
    study_plan: List[Dict[str, Any]]


class CompleteAssessmentResponse(BaseModel):
    assessment_id: int
    message: str
    overall_score: float
    readiness_level: str
    salary_analysis: Dict[str, Any]
    company_fit: Dict[str, Any]
    roadmap: RoadmapResponse


@router.post("/start", response_model=StartAssessmentResponse)
def start_assessment(
    request: StartAssessmentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new assessment for the authenticated user.
    """
    role = db.query(Role).filter(Role.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Assessments are now always tied to the authenticated user
    user_id = current_user.id
    session_id = None
    years_exp = request.years_of_experience
    primary_stack = request.primary_stack
    tech_stack = request.tech_stack
    certifications = request.certifications

    # If a user profile exists, use it to enrich or backfill missing context
    from models.user_profile import UserProfile

    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if profile:
        if primary_stack is None:
            primary_stack = profile.primary_stack
        if tech_stack is None:
            tech_stack = [profile.secondary_stack] if profile.secondary_stack else []
        if certifications is None:
            certifications = profile.certifications
        if years_exp == 0:
            years_exp = profile.experience_years

    assessment = Assessment(
        user_id=user_id,
        session_id=session_id,
        role_id=request.role_id,
        years_of_experience=years_exp,
        company_type=request.company_type,
        current_salary=request.current_salary,
        target_role=request.target_role,
        location=request.location,
        primary_stack=primary_stack,
        tech_stack=tech_stack,
        certifications=certifications,
        current_level=request.current_level,
        is_complete=0
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return StartAssessmentResponse(
        assessment_id=assessment.id,
        session_id=session_id,
        message="Assessment started successfully"
    )


@router.get("/{assessment_id}/questions", response_model=List[QuestionResponse])
def get_questions(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Get filtered questions based on role, stack, and experience.
    """
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    from sqlalchemy import or_
    query = db.query(Question).filter(
        or_(Question.role_id == assessment.role_id, Question.role_id == 0)
    )
    
    # Filtering based on YOE
    if assessment.years_of_experience >= 5:
        query = query.filter(Question.experience_min >= 2.0)
    else:
        query = query.filter(Question.experience_max <= 6.0)
        
    # Filtering based on Stack
    if assessment.primary_stack:
        query = query.filter(or_(Question.stack_name == None, Question.stack_name == assessment.primary_stack))
    else:
        query = query.filter(Question.stack_name == None)
        
    questions = query.order_by(Question.question_order).all()
    
    return [QuestionResponse(
        id=q.id,
        dimension=q.dimension,
        question_text=q.question_text,
        question_order=q.question_order,
        answer_options=q.get_answer_options_dict(),
        is_behavioral=q.is_behavioral
    ) for q in questions]


@router.post("/{assessment_id}/answers")
def submit_answers(
    assessment_id: int,
    request: SubmitAnswersRequest,
    db: Session = Depends(get_db)
):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    assessment.answers = request.answers
    db.commit()
    return {"message": "Answers submitted successfully"}


@router.post("/{assessment_id}/complete", response_model=CompleteAssessmentResponse)
def complete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Finalize assessment and generate comprehensive report.
    """
    from services.scoring_engine import ScoringEngine
    from services.benchmark_engine import BenchmarkEngine
    from services.salary_analyzer import SalaryAnalyzer
    from services.career_fit_engine import CareerFitEngine
    from services.roadmap_generator import RoadmapGenerator
    
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment or not assessment.answers:
        raise HTTPException(status_code=404, detail="Assessment not found or no answers")
    
    from sqlalchemy import or_
    questions = db.query(Question).filter(
        or_(Question.role_id == assessment.role_id, Question.role_id == 0)
    ).all()
    
    # 1. Scoring Logic
    scores = ScoringEngine.calculate_scores(
        assessment.answers, 
        questions, 
        years_of_experience=assessment.years_of_experience
    )
    assessment.overall_score = scores["overall_score"]
    assessment.dimension_scores = scores["dimension_scores"]
    
    # 2. Benchmark Logic
    benchmark = BenchmarkEngine.find_matching_benchmark(
        db, assessment.role_id, assessment.years_of_experience, 
        assessment.company_type, assessment.target_role
    )
    
    # 3. Enhanced Analysis
    readiness = BenchmarkEngine.determine_readiness(assessment.overall_score, benchmark)
    assessment.readiness_level = readiness
    
    # Multipliers
    from services.stack_module import StackExtensionModule
    stack_multiplier = StackExtensionModule.get_stack_multiplier(db, assessment.primary_stack or "")
    
    # Category aggregation for maturity
    categories = ScoringEngine.aggregate_scores_by_category(assessment.dimension_scores)
    maturity_score = categories.get("Maturity & Soft Skills", 0)
    
    reliability = BenchmarkEngine.calculate_reliability_index(benchmark)
    salary_range = BenchmarkEngine.get_expected_salary_range(benchmark)
    
    salary_analysis = SalaryAnalyzer.analyze_salary(
        assessment.current_salary,
        salary_range.get("min", 0),
        salary_range.get("max", 0),
        stack_multiplier=stack_multiplier,
        behavioral_score=maturity_score,
        reliability_weight=reliability["score"]
    )
    assessment.salary_alignment = salary_analysis["status"]
    
    fit_data = CareerFitEngine.determine_company_fit(assessment.dimension_scores)
    assessment.company_fit = fit_data["best_fit"]
    
    # 4. Roadmap Generation
    role = db.query(Role).filter(Role.id == assessment.role_id).first()
    assessment_context = {
        **scores,
        "years_of_experience": assessment.years_of_experience,
        "current_salary": assessment.current_salary,
        "readiness_level": readiness,
        "maturity_score": maturity_score,
        "role_name": role.display_name if role else "Developer",
        "target_level": assessment.target_role or "Next Level",
        "risk_flags": fit_data["risk_flags"]
    }
    
    roadmap = RoadmapGenerator.generate_enhanced_roadmap(assessment_context, salary_range)
    
    # Mark complete
    assessment.is_complete = 1
    assessment.completed_at = datetime.utcnow()
    db.commit()
    
    return CompleteAssessmentResponse(
        assessment_id=assessment.id,
        message="Assessment completed successfully",
        overall_score=assessment.overall_score,
        readiness_level=readiness,
        salary_analysis=salary_analysis,
        company_fit=fit_data,
        roadmap=roadmap
    )

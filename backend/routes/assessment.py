from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from datetime import datetime
import uuid
from pydantic import BaseModel

from database import get_db
from models.assessment import Assessment
from models.question import Question
from models.role import Role


router = APIRouter(prefix="/api/assessment", tags=["assessment"])


class StartAssessmentRequest(BaseModel):
    role_id: int
    years_of_experience: float
    company_type: str
    current_salary: Optional[float] = None
    target_role: Optional[str] = None
    user_id: Optional[int] = None
    location: Optional[str] = None
    tech_stack: Optional[List[str]] = None
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
    
    class Config:
        from_attributes = True


class SubmitAnswersRequest(BaseModel):
    answers: Dict[int, int]  # question_id: answer_value


class CompleteAssessmentResponse(BaseModel):
    assessment_id: int
    message: str
    overall_score: float
    readiness_level: str


@router.post("/start", response_model=StartAssessmentResponse)
def start_assessment(
    request: StartAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Create a new assessment (anonymous or authenticated).
    """
    # Verify role exists
    role = db.query(Role).filter(Role.id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Generate session ID for anonymous users
    session_id = None if request.user_id else str(uuid.uuid4())
    
    # Create assessment
    assessment = Assessment(
        user_id=request.user_id,
        session_id=session_id,
        role_id=request.role_id,
        years_of_experience=request.years_of_experience,
        company_type=request.company_type,
        current_salary=request.current_salary,
        target_role=request.target_role,
        location=request.location,
        tech_stack=request.tech_stack,
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
    Get all questions for an assessment based on role.
    """
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Get questions for the role
    questions = db.query(Question).filter(
        Question.role_id == assessment.role_id
    ).order_by(Question.question_order).all()
    
    # Format response
    response = []
    for q in questions:
        response.append(QuestionResponse(
            id=q.id,
            dimension=q.dimension,
            question_text=q.question_text,
            question_order=q.question_order,
            answer_options=q.get_answer_options_dict()
        ))
    
    return response


@router.post("/{assessment_id}/answers")
def submit_answers(
    assessment_id: int,
    request: SubmitAnswersRequest,
    db: Session = Depends(get_db)
):
    """
    Submit answers for an assessment.
    """
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Update answers
    assessment.answers = request.answers
    db.commit()
    
    return {"message": "Answers submitted successfully"}


@router.post("/{assessment_id}/complete", response_model=CompleteAssessmentResponse)
def complete_assessment(
    assessment_id: int,
    db: Session = Depends(get_db)
):
    """
    Finalize assessment and generate report.
    """
    from services.scoring_engine import ScoringEngine
    from services.benchmark_engine import BenchmarkEngine
    from services.salary_analyzer import SalaryAnalyzer
    from services.career_fit_engine import CareerFitEngine
    
    # Get assessment
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    if not assessment.answers:
        raise HTTPException(status_code=400, detail="No answers submitted")
    
    # Get questions
    questions = db.query(Question).filter(
        Question.role_id == assessment.role_id
    ).all()
    
    # Calculate scores
    scores = ScoringEngine.calculate_scores(assessment.answers, questions)
    assessment.overall_score = scores["overall_score"]
    assessment.dimension_scores = scores["dimension_scores"]
    
    # Find matching benchmark
    benchmark = BenchmarkEngine.find_matching_benchmark(
        db,
        assessment.role_id,
        assessment.years_of_experience,
        assessment.company_type,
        assessment.target_role
    )
    
    if benchmark:
        # Determine readiness
        assessment.readiness_level = BenchmarkEngine.determine_readiness(
            assessment.overall_score,
            benchmark
        )
        
        # Analyze salary
        salary_range = BenchmarkEngine.get_expected_salary_range(benchmark)
        assessment.salary_alignment = SalaryAnalyzer.analyze_salary(
            assessment.current_salary,
            salary_range["min"],
            salary_range["max"]
        )
    else:
        assessment.readiness_level = "Unknown"
        assessment.salary_alignment = "Unknown"
    
    # Determine company fit
    assessment.company_fit = CareerFitEngine.determine_company_fit(
        assessment.dimension_scores
    )
    
    # Mark as complete
    assessment.is_complete = 1
    assessment.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(assessment)
    
    return CompleteAssessmentResponse(
        assessment_id=assessment.id,
        message="Assessment completed successfully",
        overall_score=assessment.overall_score,
        readiness_level=assessment.readiness_level
    )

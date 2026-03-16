from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Assessment(Base):
    """Assessment model storing user profile and answers."""
    
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User relationship (nullable for anonymous assessments)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Session ID for anonymous users
    session_id = Column(String, index=True, nullable=True)
    
    # Profile information
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    years_of_experience = Column(Float, nullable=False)
    company_type = Column(String, nullable=False)  # service, startup, product
    current_salary = Column(Float, nullable=True)  # Optional, in INR
    target_role = Column(String, nullable=True)  # e.g., "Senior", "Lead", "Staff"
    
    # Contextual parameters
    location = Column(String, nullable=True)
    primary_stack = Column(String, nullable=True)
    tech_stack = Column(JSON, nullable=True)  # List of strings (secondary stacks)
    certifications = Column(JSON, nullable=True)  # List of strings
    current_level = Column(String, nullable=True)
    
    # Answers stored as JSON
    # Format: {"question_id": answer_value, ...}
    answers = Column(JSON, nullable=True)
    
    # Scores
    overall_score = Column(Float, nullable=True)
    dimension_scores = Column(JSON, nullable=True)  # {"dimension_name": score, ...}
    
    # Results
    readiness_level = Column(String, nullable=True)  # Ready, Near Ready, Not Ready
    salary_alignment = Column(String, nullable=True)  # Underpaid, Fair, Overpaid
    company_fit = Column(String, nullable=True)  # service, startup, product
    
    # Metadata
    is_complete = Column(Integer, default=0)  # 0 for incomplete, 1 for complete
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    
    def __repr__(self):
        return f"<Assessment(id={self.id}, role_id={self.role_id}, is_complete={self.is_complete})>"

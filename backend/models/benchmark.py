from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Benchmark(Base):
    """Benchmark data model for role/YOE/company type combinations."""

    __tablename__ = "benchmarks"

    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    # Experience range
    experience_min = Column(Float, nullable=False)
    experience_max = Column(Float, nullable=False)

    # Company type
    company_type = Column(String, nullable=False)  # service, startup, product, mnc

    # Salary range (in INR)
    salary_min = Column(Float, nullable=False)
    salary_max = Column(Float, nullable=False)

    # Readiness thresholds (0–100 score space)
    ready_threshold = Column(Float, nullable=False)
    near_ready_threshold = Column(Float, nullable=False)

    # Target level (e.g., "Junior", "Mid-level", "Senior", "Lead", "Staff")
    target_level = Column(String, nullable=False)

    # Contextual filters
    location = Column(String, nullable=True)
    tech_stack = Column(String, nullable=True)
    role = Column(String, nullable=True)  # label like "frontend", "backend"
    stack_name = Column(String, nullable=True)

    # Benchmark metadata (already present in DB)
    percentile = Column(String, nullable=True)         # e.g., "p50", "p75"
    year = Column(Integer, nullable=False)             # e.g., 2025
    source = Column(String, nullable=True)             # "Indeed;Levels.fyi;Glassdoor"
    confidence_score = Column(Float, nullable=True)    # 0.7–0.9
    meta_notes = Column(String, nullable=True)         # free-form notes

    def __repr__(self):
        return (
            f"<Benchmark(role_id={self.role_id}, exp={self.experience_min}-{self.experience_max}, "
            f"company_type={self.company_type}, level={self.target_level}, location={self.location})>"
        )

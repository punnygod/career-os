from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Benchmark(Base):
    """Benchmark data model for role/YOE/company type combinations."""
    
    __tablename__ = "benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    
    # Experience range
    yoe_min = Column(Float, nullable=False)
    yoe_max = Column(Float, nullable=False)
    
    # Company type
    company_type = Column(String, nullable=False)  # service, startup, product
    
    # Salary range (in INR)
    salary_min = Column(Float, nullable=False)
    salary_max = Column(Float, nullable=False)
    
    # Readiness thresholds
    ready_threshold = Column(Float, nullable=False)  # e.g., 3.5 out of 4
    near_ready_threshold = Column(Float, nullable=False)  # e.g., 3.0 out of 4
    
    # Target level (e.g., "Senior", "Lead", "Staff")
    target_level = Column(String, nullable=False)
    
    # Contextual filters
    location = Column(String, nullable=True)
    tech_stack = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Benchmark(role_id={self.role_id}, yoe={self.yoe_min}-{self.yoe_max}, level={self.target_level})>"

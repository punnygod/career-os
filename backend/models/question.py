from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float
from database import Base


class Question(Base):
    """Question bank model with dimension mapping."""
    
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    dimension = Column(String, nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    question_order = Column(Integer, nullable=False)
    
    # Answer options stored as JSON-like text
    # Format: "1: Basic understanding|2: Intermediate|3: Advanced|4: Expert"
    answer_options = Column(Text, nullable=False)
    
    # New extension columns
    stack_name = Column(String, nullable=True)
    certificate_name = Column(String, nullable=True)
    experience_min = Column(Float, default=0.0)
    experience_max = Column(Float, default=100.0)
    
    # Weight for this question in the dimension score (default 1.0)
    weight = Column(Float, default=1.0)
    
    # Flag to distinguish behavioral/maturity questions from technical ones
    is_behavioral = Column(Integer, default=0) # 0 for false, 1 for true
    
    def __repr__(self):
        return f"<Question(id={self.id}, dimension={self.dimension})>"
    
    def get_answer_options_dict(self):
        """Parse answer options into a dictionary."""
        options = {}
        for option in self.answer_options.split("|"):
            key, value = option.split(":", 1)
            options[int(key.strip())] = value.strip()
        return options

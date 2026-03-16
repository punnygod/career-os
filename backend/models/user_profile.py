from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from database import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    role = Column(String)
    primary_stack = Column(String)
    secondary_stack = Column(String)
    certifications = Column(JSON, default=[])
    experience_years = Column(Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "role": self.role,
            "primary_stack": self.primary_stack,
            "secondary_stack": self.secondary_stack,
            "certifications": self.certifications,
            "experience_years": self.experience_years
        }

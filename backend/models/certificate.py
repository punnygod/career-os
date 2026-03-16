from sqlalchemy import Column, Integer, String, Float
from database import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    tier = Column(String)  # e.g., Entry, Intermediate, Expert, Specialization
    multiplier = Column(Float, default=1.0)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "tier": self.tier,
            "multiplier": self.multiplier
        }

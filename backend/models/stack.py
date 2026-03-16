from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

stack_roles = Table(
    "stack_roles",
    Base.metadata,
    Column("stack_id", Integer, ForeignKey("stacks.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    extend_existing=True,
)

class Stack(Base):
    __tablename__ = "stacks"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    category = Column(String)  # e.g., Backend, Frontend, DevOps
    demand_score = Column(Float, default=1.0)
    scarcity_score = Column(Float, default=1.0)
    enterprise_score = Column(Float, default=1.0)
    multiplier = Column(Float, default=1.0)
    
    roles = relationship("Role", secondary=stack_roles, backref="stacks")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "demand_score": self.demand_score,
            "scarcity_score": self.scarcity_score,
            "enterprise_score": self.enterprise_score,
            "multiplier": self.multiplier
        }

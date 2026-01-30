from sqlalchemy import Column, Integer, String, Text
from database import Base


class Role(Base):
    """Role model defining available tech roles."""
    
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    description = Column(Text)
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
    
    def __repr__(self):
        return f"<Role(id={self.id}, name={self.name})>"

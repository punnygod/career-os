from sqlalchemy.orm import Session
from models.stack import Stack

class StackExtensionModule:
    @staticmethod
    def get_stack_multiplier(db: Session, stack_name: str) -> float:
        """Fetch the salary multiplier for a specific tech stack."""
        if not stack_name:
            return 1.0
        
        stack = db.query(Stack).filter(Stack.name == stack_name).first()
        return stack.multiplier if stack else 1.0

    @staticmethod
    def get_stack_demand_metrics(db: Session, stack_name: str) -> dict:
        """Fetch demand, scarcity, and enterprise scores for a stack."""
        if not stack_name:
            return {"demand": 1.0, "scarcity": 1.0, "enterprise": 1.0}
        
        stack = db.query(Stack).filter(Stack.name == stack_name).first()
        if stack:
            return {
                "demand": stack.demand_score,
                "scarcity": stack.scarcity_score,
                "enterprise": stack.enterprise_score
            }
        return {"demand": 1.0, "scarcity": 1.0, "enterprise": 1.0}

"""
Seed script for roles data.
Run this to populate the roles table with initial data.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from models.role import Role


def seed_roles():
    """Seed roles table with initial data."""
    db = SessionLocal()
    
    try:
        # Clear roles to apply changes
        db.query(Role).delete()
        
        roles = [
            Role(
                id=0,
                name="core",
                display_name="Engineering Maturity",
                description="Internal role for behavioral and core engineering dimensions. Role-agnostic.",
                is_active=0 # Hidden from role listings
            ),
            Role(
                id=1,
                name="frontend",
                display_name="Frontend Engineer",
                description="Build user interfaces and client-side applications using modern frameworks like React, Vue, or Angular.",
                is_active=1
            ),
            Role(
                id=2,
                name="backend",
                display_name="Backend Engineer",
                description="Design and implement server-side logic, APIs, and database systems.",
                is_active=1
            ),
            Role(
                id=3,
                name="fullstack",
                display_name="Full Stack Engineer",
                description="Versatile engineer capable of handling both frontend and backend development, including database management and system integration.",
                is_active=1
            ),
            Role(
                id=4,
                name="devops",
                display_name="DevOps / SRE",
                description="Manage infrastructure, CI/CD pipelines, and ensure system reliability.",
                is_active=1
            )
        ]
        
        # In SQLite/SQLAlchemy, to force ID 0, we can add them to the session
        # but sometimes autoincrement interferes. Explicitly adding them should work.
        db.add_all(roles)
        db.commit()
        
        print(f"Successfully seeded {len(roles)} roles (including Hidden Core ID: 0)!")
        
    except Exception as e:
        print(f"Error seeding roles: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_roles()

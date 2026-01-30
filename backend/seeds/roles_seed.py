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
        # Check if roles already exist
        existing_roles = db.query(Role).count()
        if existing_roles > 0:
            print(f"Roles already seeded ({existing_roles} roles found). Skipping...")
            return
        
        roles = [
            Role(
                name="frontend",
                display_name="Frontend Engineer",
                description="Build user interfaces and client-side applications using modern frameworks like React, Vue, or Angular.",
                is_active=1
            ),
            Role(
                name="backend",
                display_name="Backend Engineer",
                description="Design and implement server-side logic, APIs, and database systems.",
                is_active=1
            ),
            Role(
                name="data",
                display_name="Data / ML Engineer",
                description="Build data pipelines, machine learning models, and analytics systems.",
                is_active=1
            ),
            Role(
                name="devops",
                display_name="DevOps / SRE",
                description="Manage infrastructure, CI/CD pipelines, and ensure system reliability.",
                is_active=1
            )
        ]
        
        db.add_all(roles)
        db.commit()
        
        print(f"Successfully seeded {len(roles)} roles!")
        
    except Exception as e:
        print(f"Error seeding roles: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_roles()

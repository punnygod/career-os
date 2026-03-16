"""
Master seed script to run all seed files in order.
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import init_db

# Import seed functions
from seeds.roles_seed import seed_roles
from seeds.questions_seed import seed_questions
from seeds.benchmark_seed import seed_benchmarks


def seed_all():
    """Run all seed scripts in the correct order."""
    print("=" * 60)
    print("Career OS - Database Seeding")
    print("=" * 60)
    print()
    
    # Initialize database
    print("Initializing database...")
    init_db()
    print("✓ Database initialized")
    print()
    
    # Seed roles
    print("Seeding roles...")
    seed_roles()
    print()
    
    # Seed questions
    print("Seeding questions...")
    seed_questions()
    print()
    
    # Seed benchmarks
    print("Seeding benchmarks...")
    seed_benchmarks()
    print()

    # Import and seed new modules
    from seeds.stack_seed import seed_stacks
    from seeds.certificate_seed import seed_certificates
    print("Seeding stacks...")
    seed_stacks()
    print()
    print("Seeding certificates...")
    seed_certificates()
    print()
    
    print("=" * 60)
    print("✓ All seed data loaded successfully!")
    print("=" * 60)


if __name__ == "__main__":
    seed_all()

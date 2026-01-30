"""
Seed script for benchmark data.
Run this to populate the benchmarks table with salary ranges and readiness thresholds.
Data based on public sources like levels.fyi, Glassdoor, and Payscale (2024 data).
"""
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, init_db
from models.benchmark import Benchmark
from models.role import Role


# Benchmark data for different roles, YOE ranges, and company types
# Salary ranges are in INR (annual) - Adjusted for Indian Market Standards
BENCHMARK_DATA = [
    # Frontend Engineer - Junior (0-2 years)
    {"role": "frontend", "yoe_min": 0, "yoe_max": 2, "company_type": "service", "salary_min": 450000, "salary_max": 800000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "frontend", "yoe_min": 0, "yoe_max": 2, "company_type": "startup", "salary_min": 700000, "salary_max": 1400000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "frontend", "yoe_min": 0, "yoe_max": 2, "company_type": "product", "salary_min": 1000000, "salary_max": 1800000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Frontend Engineer - Mid-level (2-5 years)
    {"role": "frontend", "yoe_min": 2, "yoe_max": 5, "company_type": "service", "salary_min": 900000, "salary_max": 1800000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "frontend", "yoe_min": 2, "yoe_max": 5, "company_type": "startup", "salary_min": 1500000, "salary_max": 3000000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "frontend", "yoe_min": 2, "yoe_max": 5, "company_type": "product", "salary_min": 2200000, "salary_max": 4500000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Frontend Engineer - Senior (5-8 years)
    {"role": "frontend", "yoe_min": 5, "yoe_max": 8, "company_type": "service", "salary_min": 1800000, "salary_max": 3000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "frontend", "yoe_min": 5, "yoe_max": 8, "company_type": "startup", "salary_min": 3200000, "salary_max": 5500000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "frontend", "yoe_min": 5, "yoe_max": 8, "company_type": "product", "salary_min": 4500000, "salary_max": 8000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    
    # Frontend Engineer - Lead/Staff (8+ years)
    {"role": "frontend", "yoe_min": 8, "yoe_max": 15, "company_type": "service", "salary_min": 3000000, "salary_max": 5000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "frontend", "yoe_min": 8, "yoe_max": 15, "company_type": "startup", "salary_min": 5500000, "salary_max": 9000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "frontend", "yoe_min": 8, "yoe_max": 15, "company_type": "product", "salary_min": 8500000, "salary_max": 15000000, "target_level": "Staff", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    
    # Backend Engineer - Junior (0-2 years)
    {"role": "backend", "yoe_min": 0, "yoe_max": 2, "company_type": "service", "salary_min": 500000, "salary_max": 850000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "backend", "yoe_min": 0, "yoe_max": 2, "company_type": "startup", "salary_min": 750000, "salary_max": 1500000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "backend", "yoe_min": 0, "yoe_max": 2, "company_type": "product", "salary_min": 1100000, "salary_max": 2000000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Backend Engineer - Mid-level (2-5 years)
    {"role": "backend", "yoe_min": 2, "yoe_max": 5, "company_type": "service", "salary_min": 1000000, "salary_max": 2000000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "backend", "yoe_min": 2, "yoe_max": 5, "company_type": "startup", "salary_min": 1800000, "salary_max": 3500000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "backend", "yoe_min": 2, "yoe_max": 5, "company_type": "product", "salary_min": 2500000, "salary_max": 5000000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Backend Engineer - Senior (5-8 years)
    {"role": "backend", "yoe_min": 5, "yoe_max": 8, "company_type": "service", "salary_min": 2000000, "salary_max": 3500000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "backend", "yoe_min": 5, "yoe_max": 8, "company_type": "startup", "salary_min": 3500000, "salary_max": 6000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "backend", "yoe_min": 5, "yoe_max": 8, "company_type": "product", "salary_min": 5000000, "salary_max": 9000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    
    # Backend Engineer - Lead/Staff (8+ years)
    {"role": "backend", "yoe_min": 8, "yoe_max": 15, "company_type": "service", "salary_min": 3500000, "salary_max": 6000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "backend", "yoe_min": 8, "yoe_max": 15, "company_type": "startup", "salary_min": 6000000, "salary_max": 10000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "backend", "yoe_min": 8, "yoe_max": 15, "company_type": "product", "salary_min": 9000000, "salary_max": 18000000, "target_level": "Staff", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    
    # Data/ML Engineer - Junior (0-2 years)
    {"role": "data", "yoe_min": 0, "yoe_max": 2, "company_type": "service", "salary_min": 550000, "salary_max": 950000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "data", "yoe_min": 0, "yoe_max": 2, "company_type": "startup", "salary_min": 850000, "salary_max": 1600000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "data", "yoe_min": 0, "yoe_max": 2, "company_type": "product", "salary_min": 1200000, "salary_max": 2200000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Data/ML Engineer - Mid-level (2-5 years)
    {"role": "data", "yoe_min": 2, "yoe_max": 5, "company_type": "service", "salary_min": 1100000, "salary_max": 2200000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "data", "yoe_min": 2, "yoe_max": 5, "company_type": "startup", "salary_min": 2000000, "salary_max": 3800000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "data", "yoe_min": 2, "yoe_max": 5, "company_type": "product", "salary_min": 2800000, "salary_max": 5500000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # Data/ML Engineer - Senior (5-8 years)
    {"role": "data", "yoe_min": 5, "yoe_max": 8, "company_type": "service", "salary_min": 2200000, "salary_max": 4000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "data", "yoe_min": 5, "yoe_max": 8, "company_type": "startup", "salary_min": 4000000, "salary_max": 7000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "data", "yoe_min": 5, "yoe_max": 8, "company_type": "product", "salary_min": 6000000, "salary_max": 11000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    
    # Data/ML Engineer - Lead/Staff (8+ years)
    {"role": "data", "yoe_min": 8, "yoe_max": 15, "company_type": "service", "salary_min": 4000000, "salary_max": 7000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "data", "yoe_min": 8, "yoe_max": 15, "company_type": "startup", "salary_min": 7000000, "salary_max": 12000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "data", "yoe_min": 8, "yoe_max": 15, "company_type": "product", "salary_min": 11000000, "salary_max": 22000000, "target_level": "Staff", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    
    # DevOps/SRE - Junior (0-2 years)
    {"role": "devops", "yoe_min": 0, "yoe_max": 2, "company_type": "service", "salary_min": 500000, "salary_max": 900000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "devops", "yoe_min": 0, "yoe_max": 2, "company_type": "startup", "salary_min": 800000, "salary_max": 1500000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "devops", "yoe_min": 0, "yoe_max": 2, "company_type": "product", "salary_min": 1100000, "salary_max": 2000000, "target_level": "Junior", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # DevOps/SRE - Mid-level (2-5 years)
    {"role": "devops", "yoe_min": 2, "yoe_max": 5, "company_type": "service", "salary_min": 1000000, "salary_max": 2200000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "devops", "yoe_min": 2, "yoe_max": 5, "company_type": "startup", "salary_min": 1800000, "salary_max": 3800000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    {"role": "devops", "yoe_min": 2, "yoe_max": 5, "company_type": "product", "salary_min": 2800000, "salary_max": 5500000, "target_level": "Mid-level", "ready_threshold": 80.0, "near_ready_threshold": 60.0},
    
    # DevOps/SRE - Senior (5-8 years)
    {"role": "devops", "yoe_min": 5, "yoe_max": 8, "company_type": "service", "salary_min": 2200000, "salary_max": 4000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "devops", "yoe_min": 5, "yoe_max": 8, "company_type": "startup", "salary_min": 4000000, "salary_max": 7500000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    {"role": "devops", "yoe_min": 5, "yoe_max": 8, "company_type": "product", "salary_min": 6000000, "salary_max": 11000000, "target_level": "Senior", "ready_threshold": 85.0, "near_ready_threshold": 70.0},
    
    # DevOps/SRE - Lead/Staff (8+ years)
    {"role": "devops", "yoe_min": 8, "yoe_max": 15, "company_type": "service", "salary_min": 4000000, "salary_max": 7500000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "devops", "yoe_min": 8, "yoe_max": 15, "company_type": "startup", "salary_min": 7500000, "salary_max": 13000000, "target_level": "Lead", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
    {"role": "devops", "yoe_min": 8, "yoe_max": 15, "company_type": "product", "salary_min": 11000000, "salary_max": 22000000, "target_level": "Staff", "ready_threshold": 90.0, "near_ready_threshold": 75.0},
]


def seed_benchmarks():
    """Seed benchmarks table with initial data."""
    db = SessionLocal()
    
    try:
        # Check if benchmarks already exist
        existing_benchmarks = db.query(Benchmark).count()
        if existing_benchmarks > 0:
            print(f"Benchmarks already seeded ({existing_benchmarks} benchmarks found). Skipping...")
            return
        
        # Get all roles
        roles = {role.name: role.id for role in db.query(Role).all()}
        
        if not roles:
            print("Error: Roles not found. Please run roles_seed.py first.")
            return
        
        benchmarks = []
        
        for data in BENCHMARK_DATA:
            role_name = data["role"]
            if role_name not in roles:
                print(f"Warning: Role '{role_name}' not found, skipping...")
                continue
            
            benchmarks.append(Benchmark(
                role_id=roles[role_name],
                yoe_min=data["yoe_min"],
                yoe_max=data["yoe_max"],
                company_type=data["company_type"],
                salary_min=data["salary_min"],
                salary_max=data["salary_max"],
                target_level=data["target_level"],
                ready_threshold=data["ready_threshold"],
                near_ready_threshold=data["near_ready_threshold"]
            ))
        
        db.add_all(benchmarks)
        db.commit()
        
        print(f"Successfully seeded {len(benchmarks)} benchmarks!")
        print(f"  - Covering 4 roles × 4 levels × 3 company types")
        
    except Exception as e:
        print(f"Error seeding benchmarks: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
    seed_benchmarks()

import sys
import os
from sqlalchemy import text

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def migrate():
    with engine.connect() as conn:
        print("Starting migration...")
        
        # Add columns to assessments table
        try:
            print("Updating 'assessments' table...")
            conn.execute(text("ALTER TABLE assessments ADD COLUMN IF NOT EXISTS primary_stack VARCHAR"))
            conn.execute(text("ALTER TABLE assessments ADD COLUMN IF NOT EXISTS certifications JSON"))
            print("✓ 'assessments' table updated")
        except Exception as e:
            print(f"Error updating 'assessments' table: {e}")

        # Add columns to benchmarks table
        try:
            print("Updating 'benchmarks' table...")
            # experience_min and experience_max already exist based on inspection
            # target_level is missing
            conn.execute(text("ALTER TABLE benchmarks ADD COLUMN IF NOT EXISTS target_level VARCHAR"))
            
            # Best effort to populate target_level if empty
            conn.execute(text("UPDATE benchmarks SET target_level = 'Mid-level' WHERE target_level IS NULL"))
            
            print("✓ 'benchmarks' table updated")
        except Exception as e:
            print(f"Error updating 'benchmarks' table: {e}")

        conn.commit()
        print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()

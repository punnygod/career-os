import sys
import os
from sqlalchemy import inspect

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def inspect_tables():
    inspector = inspect(engine)
    tables = ['assessments', 'questions', 'benchmarks', 'user_profiles']
    for table_name in tables:
        try:
            columns = inspector.get_columns(table_name)
            print(f"--- {table_name} ---")
            for column in columns:
                print(f"{column['name']} ({column['type']})")
        except Exception as e:
            print(f"Error inspecting table '{table_name}': {e}")

if __name__ == "__main__":
    inspect_tables()

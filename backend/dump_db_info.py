import sys
import os
import json
from sqlalchemy import inspect, text

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine

def dump_db_info():
    inspector = inspect(engine)
    table_names = inspector.get_table_names()
    
    print(f"Total Tables: {len(table_names)}")
    
    for table_name in table_names:
        print(f"\n{'='*20} {table_name} {'='*20}")
        
        # Schema
        columns = inspector.get_columns(table_name)
        print("Columns:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']})")
            
        # Sample Data
        try:
            with engine.connect() as connection:
                result = connection.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
                rows = [dict(row._mapping) for row in result]
                print(f"\nSample Data ({len(rows)} rows):")
                for row in rows:
                    # Handle decimals/non-serializable types for pretty printing if needed
                    print(json.dumps(row, indent=2, default=str))
        except Exception as e:
            print(f"Error fetching data from {table_name}: {e}")

if __name__ == "__main__":
    dump_db_info()

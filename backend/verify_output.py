import json
from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def run_scenario(name, role_id, yoe, company_type, salary, target_role, score_val):
    print(f"\n--- Scenario: {name} ---")
    
    # 1. Start Assessment
    start_payload = {
        "role_id": role_id,
        "years_of_experience": yoe,
        "company_type": company_type,
        "current_salary": salary,
        "target_role": target_role
    }
    response = client.post("/api/assessment/start", json=start_payload)
    assessment_id = response.json()["assessment_id"]
    
    # 2. Submit Answers
    response = client.get(f"/api/assessment/{assessment_id}/questions")
    questions = response.json()
    answers = {q["id"]: score_val for q in questions}
    client.post(f"/api/assessment/{assessment_id}/answers", json={"answers": answers})
    
    # 3. Complete
    client.post(f"/api/assessment/{assessment_id}/complete")
    
    # 4. Fetch Report
    response = client.get(f"/api/report/{assessment_id}")
    report = response.json()
    
    output = {
        "input": start_payload,
        "results": {
            "overall_score": report["overall_score"],
            "readiness_level": report["readiness_level"],
            "salary_info": report["salary_info"],
            "company_fit": report["company_fit"],
            "next_level": report["next_level_preview"]
        }
    }
    print(json.dumps(output, indent=2))
    return output

def main():
    results = []
    
    # Case 1: Junior Underpaid
    results.append(run_scenario(
        "Junior Underpaid (Service)", 
        1, 1.0, "service", 50000, "Junior", 3
    ))
    
    # Case 2: Mid-level Ready (Product)
    results.append(run_scenario(
        "Mid-level Ready (Product)", 
        1, 3.5, "product", 130000, "Mid-level", 4
    ))
    
    # Case 3: Senior High Potential ROI
    results.append(run_scenario(
        "Senior High Potential (Startup)", 
        1, 6.0, "startup", 110000, "Senior", 4
    ))
    
    # Case 4: Not Ready Case
    results.append(run_scenario(
        "Not Ready (Product)", 
        1, 5.0, "product", 150000, "Senior", 1
    ))

if __name__ == "__main__":
    main()

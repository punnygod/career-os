from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_full_assessment_flow():
    # 1. Start Assessment
    start_payload = {
        "role_id": 1,
        "years_of_experience": 3.5,
        "company_type": "Product",
        "current_salary": 90000,
        "target_role": "Senior Frontend Engineer",
        "location": "New York",
        "tech_stack": ["React", "TypeScript", "Node.js"],
        "current_level": "L4"
    }
    response = client.post("/api/assessment/start", json=start_payload)
    assert response.status_code == 200
    data = response.json()
    assessment_id = data["assessment_id"]
    assert assessment_id > 0
    
    # 2. Get Questions
    response = client.get(f"/api/assessment/{assessment_id}/questions")
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) > 0
    
    # 3. Submit Answers
    answers = {q["id"]: 4 for q in questions} # Answer '4' for all questions
    submit_payload = {"answers": answers}
    response = client.post(f"/api/assessment/{assessment_id}/answers", json=submit_payload)
    assert response.status_code == 200
    
    # 4. Complete Assessment
    response = client.post(f"/api/assessment/{assessment_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert "overall_score" in data
    assert "readiness_level" in data
    
    # 5. Fetch Report
    response = client.get(f"/api/report/{assessment_id}")
    assert response.status_code == 200
    report = response.json()
    assert report["assessment_id"] == assessment_id
    assert len(report["dimension_scores"]) > 0
    assert "salary_info" in report
    assert "radar_chart_data" in report
    assert len(report["radar_chart_data"]) == len(report["dimension_scores"])
    
    # Special check for ROI and market percentile (new features)
    if report["salary_info"]:
        assert "potential_roi" in report["salary_info"]
        assert "market_percentile" in report["salary_info"]

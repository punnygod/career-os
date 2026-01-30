from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_start_assessment_success():
    payload = {
        "role_id": 1,
        "years_of_experience": 2.0,
        "company_type": "Startup"
    }
    response = client.post("/api/assessment/start", json=payload)
    assert response.status_code == 200
    assert "assessment_id" in response.json()

def test_start_assessment_invalid_role():
    payload = {
        "role_id": 9999,
        "years_of_experience": 2.0,
        "company_type": "Startup"
    }
    response = client.post("/api/assessment/start", json=payload)
    assert response.status_code == 404

def test_get_questions_success():
    # Start assessment first
    start_resp = client.post("/api/assessment/start", json={
        "role_id": 1,
        "years_of_experience": 2.0,
        "company_type": "Startup"
    })
    assessment_id = start_resp.json()["assessment_id"]
    
    response = client.get(f"/api/assessment/{assessment_id}/questions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_submit_answers_and_complete():
    # Start assessment
    start_resp = client.post("/api/assessment/start", json={
        "role_id": 1,
        "years_of_experience": 2.0,
        "company_type": "Startup"
    })
    assessment_id = start_resp.json()["assessment_id"]
    
    # Get questions
    q_resp = client.get(f"/api/assessment/{assessment_id}/questions")
    questions = q_resp.json()
    
    # Submit answers
    answers = {str(q["id"]): 4 for q in questions}
    submit_resp = client.post(f"/api/assessment/{assessment_id}/answers", json={"answers": answers})
    assert submit_resp.status_code == 200
    
    # Complete assessment
    complete_resp = client.post(f"/api/assessment/{assessment_id}/complete")
    assert complete_resp.status_code == 200
    data = complete_resp.json()
    assert "overall_score" in data
    assert data["overall_score"] == 100.0 # Since all answers were 4

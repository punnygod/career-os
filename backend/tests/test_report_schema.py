from fastapi.testclient import TestClient
import sys
import os

# Add backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_report_schema_enhancements():
    # Note: This requires a seeded database and an existing assessment.
    # For now, we'll just check if the model fields are present in the response model definition.
    from routes.report import CareerReportResponse
    
    fields = CareerReportResponse.model_fields
    assert "radar_chart_data" in fields
    assert "interview_questions" in fields
    assert "learning_resources" in fields
    assert "next_level_preview" in fields
    
    # Check SalaryInfo fields
    from routes.report import SalaryInfo
    salary_fields = SalaryInfo.model_fields
    assert "potential_roi" in salary_fields
    assert "market_percentile" in salary_fields

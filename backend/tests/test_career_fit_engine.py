from services.career_fit_engine import CareerFitEngine

def test_determine_company_fit_service():
    # Strong in Backend Fundamentals + Architecture + Code Quality (Maturity)
    scores = {
        "Backend Fundamentals": 90.0,
        "Code Quality & Engineering Practices": 90.0,
        "Programming Fundamentals": 80.0
    }
    result = CareerFitEngine.determine_company_fit(scores)
    assert result["best_fit"] == "service"

def test_determine_company_fit_startup():
    # Strong in Ownership & Accountability + Problem Solving
    scores = {
        "Ownership & Accountability": 95.0,
        "Problem Solving & Ambiguity Handling": 90.0,
        "Execution & Delivery Discipline": 90.0
    }
    result = CareerFitEngine.determine_company_fit(scores)
    assert result["best_fit"] == "startup"

def test_detect_friction_signals():
    # High technical, low maturity
    scores = {
        "Backend Fundamentals": 90.0,
        "JavaScript Fundamentals": 90.0,
        "Collaboration & Cross-Functional Communication": 30.0,
        "Ownership & Accountability": 40.0
    }
    result = CareerFitEngine.determine_company_fit(scores)
    assert any("Growth Bottleneck" in flag for flag in result["risk_flags"])

def test_get_fit_explanation():
    assert "service-based" in CareerFitEngine.get_fit_explanation("service")
    assert "startup environments" in CareerFitEngine.get_fit_explanation("startup")
    assert "product companies" in CareerFitEngine.get_fit_explanation("product")
    assert "Big Tech" in CareerFitEngine.get_fit_explanation("enterprise")

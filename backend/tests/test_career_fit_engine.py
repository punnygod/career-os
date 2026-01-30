from services.career_fit_engine import CareerFitEngine

def test_determine_company_fit_service():
    scores = {
        "Core Technical Skills": 90.0,
        "Code Quality & Practices": 90.0,
        "Architecture & Design": 70.0,
        "Ownership & Impact": 50.0,
        "Communication & Influence": 50.0
    }
    # service_score = (90 * 1.5 + 90 * 1.5 + 70) / 4 = (135 + 135 + 70) / 4 = 340 / 4 = 85
    # startup_score = (50 * 2 + 90 + 50) / 4 = (100 + 90 + 50) / 4 = 240 / 4 = 60
    # product_score = (70 * 1.5 + 50 * 1.5 + 50) / 4 = (105 + 75 + 50) / 4 = 230 / 4 = 57.5
    assert CareerFitEngine.determine_company_fit(scores) == "service"

def test_determine_company_fit_startup():
    scores = {
        "Ownership & Impact": 95.0,
        "Core Technical Skills": 70.0,
        "Communication & Influence": 80.0,
        "Architecture & Design": 50.0,
        "Code Quality & Practices": 50.0
    }
    # startup_score = (95 * 2 + 70 + 80) / 4 = (190 + 70 + 80) / 4 = 340 / 4 = 85
    assert CareerFitEngine.determine_company_fit(scores) == "startup"

def test_determine_company_fit_product():
    scores = {
        "Architecture & Design": 90.0,
        "Communication & Influence": 90.0,
        "Ownership & Impact": 70.0,
        "Core Technical Skills": 50.0,
        "Code Quality & Practices": 50.0
    }
    # product_score = (90 * 1.5 + 90 * 1.5 + 70) / 4 = (135 + 135 + 70) / 4 = 85
    assert CareerFitEngine.determine_company_fit(scores) == "product"

def test_get_fit_explanation():
    assert "service companies" in CareerFitEngine.get_fit_explanation("service")
    assert "startup environments" in CareerFitEngine.get_fit_explanation("startup")
    assert "product companies" in CareerFitEngine.get_fit_explanation("product")
    assert CareerFitEngine.get_fit_explanation("unknown") == ""

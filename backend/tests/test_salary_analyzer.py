from services.salary_analyzer import SalaryAnalyzer

def test_analyze_salary():
    # Fair
    assert SalaryAnalyzer.analyze_salary(100000, 90000, 110000) == "Fair"
    # Underpaid
    assert SalaryAnalyzer.analyze_salary(80000, 90000, 110000) == "Underpaid"
    # Overpaid
    assert SalaryAnalyzer.analyze_salary(120000, 90000, 110000) == "Overpaid"
    # Unknown
    assert SalaryAnalyzer.analyze_salary(None, 90000, 110000) == "Unknown"

def test_get_salary_gap():
    # Fair
    assert SalaryAnalyzer.get_salary_gap(100000, 90000, 110000) == 0.0
    # Underpaid
    assert SalaryAnalyzer.get_salary_gap(80000, 90000, 110000) == 10000.0
    # Overpaid
    assert SalaryAnalyzer.get_salary_gap(120000, 90000, 110000) == -10000.0
    # Unknown
    assert SalaryAnalyzer.get_salary_gap(None, 90000, 110000) is None

def test_calculate_roi():
    assert SalaryAnalyzer.calculate_roi(80000, 100000) == 20000.0
    assert SalaryAnalyzer.calculate_roi(120000, 100000) == 0.0
    assert SalaryAnalyzer.calculate_roi(None, 100000) is None

def test_market_percentile():
    assert SalaryAnalyzer.get_market_percentile(60000, 60000, 100000) == 10
    assert SalaryAnalyzer.get_market_percentile(100000, 60000, 100000) == 90
    assert SalaryAnalyzer.get_market_percentile(80000, 60000, 100000) == 50
    assert SalaryAnalyzer.get_market_percentile(None, 60000, 100000) is None

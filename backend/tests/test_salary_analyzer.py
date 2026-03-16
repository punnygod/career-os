from services.salary_analyzer import SalaryAnalyzer

def test_analyze_salary():
    # Aligned: current is median
    result = SalaryAnalyzer.analyze_salary(100000, 90000, 110000)
    assert result["status"] == "Aligned"
    
    # Underpaid
    result = SalaryAnalyzer.analyze_salary(80000, 90000, 110000)
    assert result["status"] == "Underpaid"
    
    # Market Leader
    result = SalaryAnalyzer.analyze_salary(120000, 90000, 110000)
    assert result["status"] == "Market Leader"

def test_get_salary_gap():
    # Gap to median (100k)
    gap = SalaryAnalyzer.get_salary_gap(80000, 100000)
    assert gap == 20000.0
    
    # No gap if above or equal
    gap = SalaryAnalyzer.get_salary_gap(105000, 100000)
    assert gap == 0.0

def test_maturity_multiplier():
    assert SalaryAnalyzer.get_maturity_multiplier(95) == 1.20
    assert SalaryAnalyzer.get_maturity_multiplier(85) == 1.15
    assert SalaryAnalyzer.get_maturity_multiplier(50) == 1.0

def test_market_percentile():
    assert SalaryAnalyzer.get_market_percentile(60000, 60000, 100000) == 10
    assert SalaryAnalyzer.get_market_percentile(100000, 60000, 100000) == 90
    assert SalaryAnalyzer.get_market_percentile(80000, 60000, 100000) == 50

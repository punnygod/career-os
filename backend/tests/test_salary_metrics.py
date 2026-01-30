from services.salary_analyzer import SalaryAnalyzer

def test_calculate_roi():
    # Underpaid case
    assert SalaryAnalyzer.calculate_roi(80000, 100000) == 20000
    # Overpaid/Fair case
    assert SalaryAnalyzer.calculate_roi(120000, 100000) == 0
    # None case
    assert SalaryAnalyzer.calculate_roi(None, 100000) is None

def test_market_percentile():
    # Near min
    assert SalaryAnalyzer.get_market_percentile(60000, 60000, 100000) == 10
    # Near max
    assert SalaryAnalyzer.get_market_percentile(100000, 60000, 100000) == 90
    # Median
    assert SalaryAnalyzer.get_market_percentile(80000, 60000, 100000) == 50
    # None case
    assert SalaryAnalyzer.get_market_percentile(None, 60000, 100000) is None

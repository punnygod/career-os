import pytest
from unittest.mock import MagicMock
from services.benchmark_engine import BenchmarkEngine

class MockBenchmark:
    def __init__(self, **kwargs):
        self.year = 2025
        self.source = "Levels.fyi;Indeed"
        self.salary_min = 0
        self.salary_max = 0
        self.ready_threshold = 85.0
        self.near_ready_threshold = 70.0
        for k, v in kwargs.items():
            setattr(self, k, v)

def test_determine_readiness():
    benchmark = MockBenchmark(ready_threshold=85.0, near_ready_threshold=70.0)
    assert BenchmarkEngine.determine_readiness(90.0, benchmark) == "Ready"
    assert BenchmarkEngine.determine_readiness(80.0, benchmark) == "Near Ready"
    assert BenchmarkEngine.determine_readiness(65.0, benchmark) == "Not Ready"

def test_calculate_reliability_index():
    benchmark = MockBenchmark(year=2025, source="Source1;Source2;Source3")
    result = BenchmarkEngine.calculate_reliability_index(benchmark)
    assert result["level"] == "High"
    assert result["source_count"] == 3

def test_get_expected_salary_range():
    benchmark = MockBenchmark(salary_min=100000.0, salary_max=150000.0)
    result = BenchmarkEngine.get_expected_salary_range(benchmark)
    assert result["min"] == 100000.0
    assert result["median"] == 125000.0
    assert "reliability" in result

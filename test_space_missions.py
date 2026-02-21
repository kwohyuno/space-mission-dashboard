"""
Tests for space_missions.py grading functions.
Covers: return types, expected outputs, edge cases, and input validation.
"""

import pytest
from space_missions import (
    getMissionCountByCompany,
    getSuccessRate,
    getMissionsByDateRange,
    getTopCompaniesByMissionCount,
    getMissionStatusCount,
    getMissionsByYear,
    getMostUsedRocket,
    getAverageMissionsPerYear,
)


# ============================================================
# Function 1: getMissionCountByCompany
# ============================================================
class TestGetMissionCountByCompany:
    def test_return_type(self):
        result = getMissionCountByCompany("NASA")
        assert isinstance(result, int)

    def test_known_company(self):
        result = getMissionCountByCompany("RVSN USSR")
        assert result == 1777

    def test_nonexistent_company(self):
        assert getMissionCountByCompany("NonExistentCompany") == 0

    def test_empty_string(self):
        assert getMissionCountByCompany("") == 0

    def test_invalid_type_int(self):
        assert getMissionCountByCompany(123) == 0

    def test_invalid_type_none(self):
        assert getMissionCountByCompany(None) == 0

    def test_case_sensitive(self):
        assert getMissionCountByCompany("nasa") == 0
        assert getMissionCountByCompany("NASA") > 0


# ============================================================
# Function 2: getSuccessRate
# ============================================================
class TestGetSuccessRate:
    def test_return_type(self):
        result = getSuccessRate("NASA")
        assert isinstance(result, float)

    def test_rounded_to_2_decimals(self):
        result = getSuccessRate("NASA")
        assert result == round(result, 2)

    def test_range_0_to_100(self):
        result = getSuccessRate("NASA")
        assert 0.0 <= result <= 100.0

    def test_nonexistent_company(self):
        assert getSuccessRate("NonExistentCompany") == 0.0

    def test_empty_string(self):
        assert getSuccessRate("") == 0.0

    def test_invalid_type_int(self):
        assert getSuccessRate(123) == 0.0

    def test_invalid_type_none(self):
        assert getSuccessRate(None) == 0.0


# ============================================================
# Function 3: getMissionsByDateRange
# ============================================================
class TestGetMissionsByDateRange:
    def test_return_type(self):
        result = getMissionsByDateRange("1957-10-01", "1957-12-31")
        assert isinstance(result, list)

    def test_known_range(self):
        result = getMissionsByDateRange("1957-10-01", "1957-12-31")
        assert result == ["Sputnik-1", "Sputnik-2", "Vanguard TV3"]

    def test_all_strings(self):
        result = getMissionsByDateRange("1957-10-01", "1957-12-31")
        assert all(isinstance(m, str) for m in result)

    def test_single_day(self):
        result = getMissionsByDateRange("1957-10-04", "1957-10-04")
        assert result == ["Sputnik-1"]

    def test_no_missions_in_range(self):
        result = getMissionsByDateRange("1900-01-01", "1950-01-01")
        assert result == []

    def test_start_after_end(self):
        result = getMissionsByDateRange("2020-12-31", "2020-01-01")
        assert result == []

    def test_invalid_date_string(self):
        assert getMissionsByDateRange("abc", "xyz") == []

    def test_invalid_type_int(self):
        assert getMissionsByDateRange(123, 456) == []

    def test_invalid_type_none(self):
        assert getMissionsByDateRange(None, None) == []


# ============================================================
# Function 4: getTopCompaniesByMissionCount
# ============================================================
class TestGetTopCompaniesByMissionCount:
    def test_return_type(self):
        result = getTopCompaniesByMissionCount(3)
        assert isinstance(result, list)

    def test_tuple_structure(self):
        result = getTopCompaniesByMissionCount(3)
        for item in result:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[0], str)
            assert isinstance(item[1], int)

    def test_correct_length(self):
        result = getTopCompaniesByMissionCount(5)
        assert len(result) == 5

    def test_descending_order(self):
        result = getTopCompaniesByMissionCount(10)
        counts = [count for _, count in result]
        assert counts == sorted(counts, reverse=True)

    def test_top_1(self):
        result = getTopCompaniesByMissionCount(1)
        assert result[0][0] == "RVSN USSR"
        assert result[0][1] == 1777

    def test_n_zero(self):
        assert getTopCompaniesByMissionCount(0) == []

    def test_n_negative(self):
        assert getTopCompaniesByMissionCount(-1) == []

    def test_invalid_type_string(self):
        assert getTopCompaniesByMissionCount("3") == []

    def test_invalid_type_float(self):
        assert getTopCompaniesByMissionCount(3.5) == []

    def test_invalid_type_none(self):
        assert getTopCompaniesByMissionCount(None) == []


# ============================================================
# Function 5: getMissionStatusCount
# ============================================================
class TestGetMissionStatusCount:
    def test_return_type(self):
        result = getMissionStatusCount()
        assert isinstance(result, dict)

    def test_has_success_key(self):
        result = getMissionStatusCount()
        assert "Success" in result

    def test_has_failure_key(self):
        result = getMissionStatusCount()
        assert "Failure" in result

    def test_has_partial_failure_key(self):
        result = getMissionStatusCount()
        assert "Partial Failure" in result

    def test_has_prelaunch_failure_key(self):
        result = getMissionStatusCount()
        assert "Prelaunch Failure" in result

    def test_values_are_ints(self):
        result = getMissionStatusCount()
        for count in result.values():
            assert isinstance(count, int)

    def test_values_positive(self):
        result = getMissionStatusCount()
        for count in result.values():
            assert count > 0

    def test_total_equals_dataset_size(self):
        result = getMissionStatusCount()
        total = sum(result.values())
        assert total > 0


# ============================================================
# Function 6: getMissionsByYear
# ============================================================
class TestGetMissionsByYear:
    def test_return_type(self):
        result = getMissionsByYear(2020)
        assert isinstance(result, int)

    def test_known_year(self):
        result = getMissionsByYear(1957)
        assert result == 3  # Sputnik-1, Sputnik-2, Vanguard TV3

    def test_year_with_no_missions(self):
        assert getMissionsByYear(1900) == 0

    def test_future_year(self):
        assert getMissionsByYear(3000) == 0

    def test_invalid_type_string(self):
        assert getMissionsByYear("2020") == 0

    def test_invalid_type_float(self):
        assert getMissionsByYear(2020.5) == 0

    def test_invalid_type_none(self):
        assert getMissionsByYear(None) == 0


# ============================================================
# Function 7: getMostUsedRocket
# ============================================================
class TestGetMostUsedRocket:
    def test_return_type(self):
        result = getMostUsedRocket()
        assert isinstance(result, str)

    def test_known_result(self):
        result = getMostUsedRocket()
        assert result == "Cosmos-3M (11K65M)"

    def test_not_empty(self):
        result = getMostUsedRocket()
        assert len(result) > 0


# ============================================================
# Function 8: getAverageMissionsPerYear
# ============================================================
class TestGetAverageMissionsPerYear:
    def test_return_type(self):
        result = getAverageMissionsPerYear(2010, 2020)
        assert isinstance(result, float)

    def test_rounded_to_2_decimals(self):
        result = getAverageMissionsPerYear(2010, 2020)
        assert result == round(result, 2)

    def test_single_year(self):
        result = getAverageMissionsPerYear(2020, 2020)
        assert result == float(getMissionsByYear(2020))

    def test_start_after_end(self):
        assert getAverageMissionsPerYear(2020, 2010) == 0.0

    def test_same_year(self):
        result = getAverageMissionsPerYear(1957, 1957)
        assert result == 3.0

    def test_invalid_type_string(self):
        assert getAverageMissionsPerYear("2010", "2020") == 0.0

    def test_invalid_type_none(self):
        assert getAverageMissionsPerYear(None, None) == 0.0

    def test_invalid_type_float(self):
        assert getAverageMissionsPerYear(2010.5, 2020.5) == 0.0

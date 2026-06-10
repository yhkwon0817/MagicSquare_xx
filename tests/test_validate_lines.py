import pytest

from validate_lines import validate_lines

MAGIC = 34

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# T2: R1(row:0) 합 33 — VALID_GRID에서 (0,0) 16→15
WRONG_ROW_GRID = [
    [15, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# T3: 완성 격자에 0 삽입
INCOMPLETE_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# T4: 주대각(diag:main)만 합 35 — 행·열 보정으로 대각만 ≠ 34
WRONG_DIAG_GRID = [
    [17, 2, 2, 13],
    [5, 10, 11, 8],
    [8, 6, 7, 12],
    [4, 15, 14, 1],
]

# T5: R1(row:0)·C2(col:1) 동시 합 33
MULTIPLE_WRONG_GRID = [
    [16, 2, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]


def test_grid_with_zero_returns_incomplete():
    # T3
    # Arrange
    grid = INCOMPLETE_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    # TODO: assert result["status"] == "incomplete"
    # TODO: assert result["failed_lines"] == []
    pytest.fail("RED skeleton — assert pending")


def test_complete_valid_grid_returns_pass():
    # T1
    # Arrange
    grid = VALID_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    # TODO: assert result["status"] == "pass"
    # TODO: assert result["failed_lines"] == []
    pytest.fail("RED skeleton — assert pending")


def test_wrong_row_sum_returns_fail_with_line_detail():
    # T2
    # Arrange
    grid = WRONG_ROW_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    # TODO: assert result["status"] == "fail"
    # TODO: assert result["failed_lines"] == [
    # TODO:     {"id": "row:0", "sum": 33, "expected": MAGIC},
    # TODO: ]
    pytest.fail("RED skeleton — assert pending")


def test_wrong_diagonal_sum_returns_fail_with_line_detail():
    # T4
    # Arrange
    grid = WRONG_DIAG_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    # TODO: assert result["status"] == "fail"
    # TODO: assert result["failed_lines"] == [
    # TODO:     {"id": "diag:main", "sum": 35, "expected": MAGIC},
    # TODO: ]
    pytest.fail("RED skeleton — assert pending")


def test_multiple_wrong_lines_returns_fail_with_line_detail():
    # T5
    # Arrange
    grid = MULTIPLE_WRONG_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    # TODO: assert result["status"] == "fail"
    # TODO: assert result["failed_lines"] == [
    # TODO:     {"id": "row:0", "sum": 33, "expected": MAGIC},
    # TODO:     {"id": "col:1", "sum": 33, "expected": MAGIC},
    # TODO: ]
    pytest.fail("RED skeleton — assert pending")

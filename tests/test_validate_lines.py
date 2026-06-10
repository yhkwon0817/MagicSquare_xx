from validate_lines import validate_lines

MAGIC = 34

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

# T2: R1(row:0) 합 33 — (0,3) 13→12 (col:3·diag:anti도 33으로 연동)
WRONG_ROW_GRID = [
    [16, 3, 2, 12],
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

# T4: 주대각(diag:main) 합 35 — 행·열 보정 시도, row:2·col:1도 33
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
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


def test_golden_master_valid_grid_regression():
    # T1 · Golden master — 회귀 시 이 격자·기대값 불변
    # Arrange
    grid = VALID_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []


def test_wrong_row_sum_returns_fail_with_line_detail():
    # T2
    # Arrange
    grid = WRONG_ROW_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 33, "expected": MAGIC},
        {"id": "col:3", "sum": 33, "expected": MAGIC},
        {"id": "diag:anti", "sum": 33, "expected": MAGIC},
    ]


def test_wrong_diagonal_sum_returns_fail_with_line_detail():
    # T4
    # Arrange
    grid = WRONG_DIAG_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:2", "sum": 33, "expected": MAGIC},
        {"id": "col:1", "sum": 33, "expected": MAGIC},
        {"id": "diag:main", "sum": 35, "expected": MAGIC},
    ]


def test_multiple_wrong_lines_returns_fail_with_line_detail():
    # T5
    # Arrange
    grid = MULTIPLE_WRONG_GRID

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 33, "expected": MAGIC},
        {"id": "col:1", "sum": 33, "expected": MAGIC},
    ]

MAGIC = 34


def validate_lines(grid):
    for row in grid:
        for cell in row:
            if cell == 0:
                return {"status": "incomplete", "failed_lines": []}

    failed_lines = []

    for i in range(4):
        row_sum = sum(grid[i])
        if row_sum != MAGIC:
            failed_lines.append({"id": f"row:{i}", "sum": row_sum, "expected": MAGIC})

    for j in range(4):
        col_sum = sum(grid[i][j] for i in range(4))
        if col_sum != MAGIC:
            failed_lines.append({"id": f"col:{j}", "sum": col_sum, "expected": MAGIC})

    main_sum = sum(grid[i][i] for i in range(4))
    if main_sum != MAGIC:
        failed_lines.append({"id": "diag:main", "sum": main_sum, "expected": MAGIC})

    anti_sum = sum(grid[i][3 - i] for i in range(4))
    if anti_sum != MAGIC:
        failed_lines.append({"id": "diag:anti", "sum": anti_sum, "expected": MAGIC})

    if failed_lines:
        return {"status": "fail", "failed_lines": failed_lines}

    return {"status": "pass", "failed_lines": []}

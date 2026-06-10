# TDD RED — validate_lines

`validate_lines` Command API에 대한 **RED 단계 전용** 워크플로. 실패하는 테스트만 추가·수정한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[RED]`
- GREEN·REFACTOR 작업은 하지 않는다. 구현 요청이 와도 RED 범위만 수행한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> dict` |
| 수정 허용 | `tests/` 만 (`tests/test_validate_lines.py` 등) |
| 수정 금지 | `src/` 전체 (`src/validate_lines.py` 포함) |
| 도메인 | 4×4 격자, 셀 0(빈칸) 또는 1~16, 마법상수 **34**, 10선 검증 |
| 10선 ID | `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti` |

### 기대 반환값

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...],  # fail 시만 채움; pass/incomplete 는 []
}
```

- **pass**: 0 없음, 10선 합 모두 34
- **fail**: 0 없음, 하나 이상 합 ≠ 34 → `failed_lines`에 `{ "id", "sum", "expected": 34 }`
- **incomplete**: 0 하나라도 포함 → 합 계산·34 비교 없음, `failed_lines`는 `[]`

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순서로 작성한다.

1. **Arrange** — 4×4 `grid` fixture 또는 인라인 격자 준비. 시나리오(정답 / 합 오류 / 빈칸)를 주석으로 한 줄 명시.
2. **Act** — `result = validate_lines(grid)` 한 번 호출.
3. **Assert** — `status`, `failed_lines` 구조·값을 도메인 규칙에 맞게 검증. fail 시 **어느 줄**인지 `id`·`sum`·`expected`까지 assert.

테스트 함수명: `test_<시나리오>_<기대status>` (예: `test_wrong_row_sum_returns_fail`).

## pytest 예시

```python
from validate_lines import validate_lines

MAGIC = 34

# --- pass ---
def test_complete_valid_grid_returns_pass():
    # Arrange: 표준 4×4 마방진 (0 없음, 10선 합 34)
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    # Act
    result = validate_lines(grid)
    # Assert
    assert result["status"] == "pass"
    assert result["failed_lines"] == []

# --- incomplete (R5) ---
def test_grid_with_zero_returns_incomplete():
    # Arrange: 빈칸(0) 포함 — 합 검증 하지 않음
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 0, 12],
        [4, 15, 14, 1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []

# --- fail: 틀린 줄 식별 ---
def test_wrong_row_sum_returns_fail_with_line_detail():
    # Arrange: R1(row:0) 합만 34가 아님
    grid = [
        [16, 3, 2, 12],  # sum 33
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
    result = validate_lines(grid)
    assert result["status"] == "fail"
    assert result["failed_lines"] == [
        {"id": "row:0", "sum": 33, "expected": MAGIC},
    ]
```

실행:

```bash
pytest tests/test_validate_lines.py -v
```

RED 확인: **새·수정 테스트가 실패**해야 한다 (`FAILED`). 전부 통과면 아직 RED가 아니다.

## 금지 (엄격)

| 금지 | 이유 |
|------|------|
| `src/` 수정·추가·삭제 | GREEN 단계 전용 |
| assert 완화·삭제·우회 | Red 회피 |
| `@pytest.mark.skip`, `xfail` | Red 회피 |
| 더미 구현으로 통과시키기 | GREEN에서 처리 |
| Solver, UI, 중복·범위 검증 테스트 | 세션 3 범위 밖 |

구현이 없어 `ImportError` 등으로 실패하는 것은 RED로 인정한다. assert를 약하게 바꿔 통과시키지 않는다.

## 보고 형식

작업 완료 후 아래 형식으로 보고한다.

```markdown
[RED]

## 추가·변경 테스트
- `test_...`: (한 줄 시나리오 설명)

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N failed, M passed (또는 ImportError 등 RED 사유)

## 다음 단계
- GREEN: `src/validate_lines.py` 최소 구현으로 위 실패 테스트 통과
```

## 체크리스트

- [ ] 응답 첫 줄 `[RED]`
- [ ] `tests/` 만 변경
- [ ] AAA·함수명·줄 ID 규칙 준수
- [ ] pass / fail / incomplete 시나리오 중 요청된 것만 추가
- [ ] pytest 실행 후 **실패** 확인
- [ ] 금지 항목 위반 없음

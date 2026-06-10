# MagicSquare_xx

4×4 **부분 마방진**에서 빈칸을 채운 뒤, **행·열·대각 10선**이 마법상수 **34**인지 한 번에 판정하고, 틀리면 **어느 줄**인지 반환하는 `validate_lines` Command와 TDD Test Loop.

> **세션 3 범위**: Rule(R1~R5) · Command · Test Loop — Solver, UI, BCE, 중복·범위 검증은 **포함하지 않음**.

상세 요구사항: [`docs/PRD.md`](docs/PRD.md)

---

## 문제 (Mom Test)

부분 마방진을 맞출 때 행·열·대각 검증을 빠뜨리면 (~20분 낭비, 표 재작업) 손으로 전 항목을 다시 더해야 “맞다”고 확신할 수 있다.  
본 프로젝트는 **판정·확인 비용**을 `validate_lines` 한 번의 호출로 줄인다.

---

## Quick Start

```bash
# 의존성: Python 3.x + pytest
pytest tests/test_validate_lines.py -v
```

| 설정 | 값 |
|------|-----|
| `testpaths` | `tests` |
| `pythonpath` | `src` |

---

## API

```python
from validate_lines import validate_lines

result = validate_lines(grid)  # grid: 4×4 list[list[int]], 셀 0 또는 1~16
# result: { "status": str, "failed_lines": list[dict] }
```

| `status` | 조건 | `failed_lines` |
|----------|------|----------------|
| `pass` | 0 없음, 10선 합 모두 34 | `[]` |
| `fail` | 0 없음, 하나 이상 합 ≠ 34 | 틀린 줄만 `{ "id", "sum", "expected": 34 }` |
| `incomplete` | 0 포함 (**R5**) — 합 검증 **하지 않음** | `[]` |

### 10선 · 줄 ID

| 표기 | ID |
|------|-----|
| R1~R4 (행) | `row:0`~`row:3` |
| C1~C4 (열) | `col:0`~`col:3` |
| D1 (주대각) | `diag:main` |
| D2 (반대각) | `diag:anti` |

구현: [`src/validate_lines.py`](src/validate_lines.py) · 테스트: [`tests/test_validate_lines.py`](tests/test_validate_lines.py)

---

## TDD · ARRR

사이클: **RED → GREEN → REFACTOR** (한 번에 한 Phase)

| Phase | 수정 | Cursor 커맨드 |
|-------|------|---------------|
| Arrange | 계획 / tests/ 골격 | `/red-test-plan` · `/red-skeleton` |
| Red | `tests/` | `/tdd-red` · `/golden-master` |
| Green | `src/` | `/green-minimal` |
| Refactor | `src/` (green 유지) | `/refactor-smell` · `/refactor-safe` |

필수 테스트 시나리오 **T1~T5** — 상세: [Test Plan](#test-plan) · [`docs/PRD.md` §7](docs/PRD.md)

---

## Test Plan

`tests/test_validate_lines.py`에 구현할 **필수 시나리오 T1~T5**. 각 테스트는 **AAA**(Arrange → Act → Assert)이며, **Act**는 `result = validate_lines(grid)` **한 번**만 호출한다 *(AC1)*.

### Golden Master — `VALID_GRID`

T1 · `/golden-master` 회귀 앵커. **값 변경 금지.**

```python
VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

0 없음 · 10선 합 각 34.

### 테스트 매트릭스

| TEST ID | 권장 함수명 | 시나리오 | Arrange | 기대 `status` | `failed_lines` |
|---------|-------------|----------|---------|---------------|----------------|
| **T1** | `test_complete_valid_grid_returns_pass` | 표준 4×4 마방진 | `VALID_GRID` | `pass` | `[]` |
| **T2** | `test_wrong_row_sum_returns_fail_with_line_detail` | **행** 하나 합 ≠ 34 | T1에서 R1(`row:0`) 한 셀 변경 → sum 33 | `fail` | `[{id:"row:0", sum:33, expected:34}]` |
| **T3** | `test_grid_with_zero_returns_incomplete` | 격자에 **0**(빈칸) 포함 | 완성 격자에 0 삽입 | `incomplete` | `[]` |
| **T4** | `test_wrong_diagonal_sum_returns_fail_with_line_detail` | **대각선만** ≠ 34 | T1에서 주대각 또는 반대각만 변경 | `fail` | `diag:main` 또는 `diag:anti` + `sum` + `expected:34` |
| **T5** | `test_multiple_wrong_lines_returns_fail_with_line_detail` | **여러 줄** 동시 ≠ 34 | 행·열 등 2줄 이상 동시 오류 | `fail` | **모든** 틀린 줄 `id`·`sum`·`expected:34` |

- 함수명은 `test_<시나리오>_<기대status>` 규칙. 의미가 같으면 변형 허용, **TEST ID 매핑은 유지**한다.
- T1이 `/golden-master`와 중복이면 **T1을 golden master로 승격**하고 함수 1개로 통합한다.
- fail 계열(T2·T4·T5)은 **AC6**에 따라 `failed_lines` 각 항목의 `id`·`sum`·`expected: 34`까지 assert한다.

### AC ↔ TEST ID 추적

| TEST ID | 커버 AC | 비고 |
|---------|---------|------|
| **T1** | AC1, AC2, AC3 | 10선 한 번 호출 · pass · golden master 앵커 |
| **T2** | AC1, AC5, AC6 | 행 단일 fail · 줄 ID·sum·expected assert |
| **T3** | AC4 | R5 incomplete · 합 검증 생략 |
| **T4** | AC1, AC5, AC6 | 대각 단독 fail — 대각 누락 방지 |
| **T5** | AC1, AC5, AC6 | 다중 fail — **모든** 틀린 줄 누락 없이 assert |

### RED 작성 순서

워크북 성공 기준 #2(Red→Green) 권장 순서:

1. **T3** — R5 `incomplete` (0 포함 시 합 검증 없음)
2. **T1** — `pass` · golden master
3. **T2** — 행 단일 `fail`
4. **T4** — 대각 단독 `fail`
5. **T5** — 다중 `fail`

### Assert 규칙

| `status` | assert |
|----------|--------|
| `pass` | `status == "pass"`, `failed_lines == []` |
| `incomplete` | `status == "incomplete"`, `failed_lines == []` |
| `fail` | `status == "fail"`, 각 틀린 줄 `{ "id", "sum", "expected": 34 }` |

각 테스트 함수에 `# T1` … `# T5` 주석으로 TEST ID 대응을 표기하는 것을 권장한다.

---

## 프로젝트 구조

```
MagicSquare_xx/
├── README.md
├── docs/PRD.md              # 제품 요구사항 (SSOT)
├── .cursorrules             # ECB · TDD · AI 규칙
├── .cursor/commands/        # 슬래시 커맨드 (tdd-red, green-minimal, …)
├── .cursor/skills/          # magic-square-tdd · magic-square-docs
├── pyproject.toml
├── src/validate_lines.py
├── tests/test_validate_lines.py
├── Report/                  # 세션 보고서
└── Prompting/               # Transcript Export
```

---

## 문서

| 문서 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | PRD — R-G-I-O · R1~R5 · AC · T1~T5 |
| [`.cursorrules`](.cursorrules) | 구현·테스트 SSOT (PRD와 동일 계약) |
| [`Report/01`](Report/01.MagicSquare_MomTest_Report.md) | Mom Test · 페르소나 |
| [`Report/03`](Report/03.MagicSquare_Session3_Workbook_Report.md) | 세션 3 워크북 |
| [`.cursor/skills/magic-square-tdd/SKILL.md`](.cursor/skills/magic-square-tdd/SKILL.md) | ARRR Skill |

세션 Export: Cursor에서 `/export`

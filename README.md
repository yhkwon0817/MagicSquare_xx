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

필수 테스트 시나리오 **T1~T5**: pass · 행 fail · incomplete(R5) · 대각 fail · 다중 fail — [`docs/PRD.md` §7](docs/PRD.md)

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

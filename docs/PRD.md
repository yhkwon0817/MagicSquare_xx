# MagicSquare_xx — Product Requirements Document (PRD)

**문서 ID**: `docs/PRD.md`  
**프로젝트**: MagicSquare_xx · 세션 3  
**버전**: 0.2 (초안)  
**작성일**: 2026-06-10  
**SSOT 우선순위**: 본 PRD ↔ [`.cursorrules`](../.cursorrules) — API·Rule·TDD는 **동일**. 충돌 시 `.cursorrules`가 구현·테스트 기준.

**선행 문서**

| 문서 | 역할 |
|------|------|
| [Report/01 — Mom Test](../Report/01.MagicSquare_MomTest_Report.md) | 페르소나 · 진짜 문제 |
| [Report/03 — 세션 3 워크북](../Report/03.MagicSquare_Session3_Workbook_Report.md) | R-G-I-O · 성공 기준 · 8계층 |
| [Report/06 — R-G-I-O 계약 리뷰](../Report/06.MagicSquare_Session3-RGIO-Contract-Review_Report.md) | 워크북–계약 갭 반영 |

---

## §1. 개요

### 1.1 한 줄 정의

4×4 **부분 마방진**에서 빈칸을 채운 직후, **행·열·대각 10선**이 각각 마법상수 **34**인지 **한 번에 판정**하고, 틀리면 **어느 줄**인지 반환하는 `validate_lines` Command와 Test Loop.

### 1.2 진짜 문제 (Mom Test)

> 부분 마방진을 처음 맞출 때, 행·열·대각을 빠짐없이 검증했다는 확신이 없어 시간을 쓰고 표를 다시 그린 뒤에야, 손으로 전 항목을 다시 더해 “맞다”고 끝낼 수 있다.

| # | 증거 | 근거 |
|---|------|------|
| 1 | 대각선 하나를 빼먹어 **약 20분** 손실 | F-2 |
| 2 | 혼자 다시 더해 알고 **표를 처음부터 다시** 그림 | F-4, F-5 |
| 3 | 두 번째엔 행·열·대각·중복·범위까지 확인 후 **제출·정답** | F-6, F-7 |

### 1.3 세션 3 주제

**4×4 부분 마방진에서 빈칸을 채운 직후, 10선 합 34 여부를 즉시 확정하고, 틀리면 줄 단위로 짚는다.** 미완성 격자(0 포함)는 `incomplete`로 **fail과 구분**한다.

*(솔루션 최소화 — 앱·솔버·UI가 아니라 **판정·확인 비용**만 다룸)*

---

## §2. 페르소나 · R-G-I-O

### 2.1 Role

4×4 **부분** 마방진 **학습자**. 빈칸 2개(0)를 1~16으로 채운 뒤 **맞았는지 스스로 확인**해야 함.

### 2.2 Goal

빈칸 채운 후 **10선 합 34 여부를 즉시 판정**하고, 틀리면 **어느 행·열·대각선**인지 식별 *(~20분 낭비 → 처음·한 번에)*.

### 2.3 Input

| 필드 | 타입 | 제약 |
|------|------|------|
| `grid` | `list[list[int]]` | **4×4** 고정 |
| 셀 값 | `int` | **0**(빈칸) 또는 **1~16** |

### 2.4 Output

`validate_lines(grid)` → **ValidationResult** (`dict`):

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [
        {"id": str, "sum": int, "expected": 34},
        ...
    ],
}
```

| status | failed_lines |
|--------|--------------|
| `pass` | `[]` |
| `fail` | 합 ≠ 34인 줄만 (1개 이상) |
| `incomplete` | `[]` — **R5**: 합 계산·34 비교 **수행하지 않음** |

> **명칭**: 워크북(`Report/03`)의 `lines[]`·`ok` 필드는 본 프로젝트에서 **`failed_lines` + `status`만** 사용한다 (`Report/05` · `.cursorrules`).

---

## §3. 범위

### 3.1 In Scope (세션 3)

| 계층 | 내용 |
|------|------|
| **Rule** | R1~R5 — 10선 합 34 판정 · R5 incomplete |
| **Command** | `validate_lines(grid)` |
| **(Skill)** | Cursor TDD·ARRR 커맨드 · pytest fixture (선택) |
| **Test Loop** | RED → GREEN → REFACTOR · T1~T5 |

### 3.2 Out of Scope (세션 3 이후)

| 제외 | 이유 |
|------|------|
| `Solver` / 빈칸 자동 채우기 / 힌트 | 고통은 **풀기**보다 **맞는지 확인** |
| BCE 전체 · `GridUI` · `InputHandler` | UI·입력은 표면 솔루션 |
| Entity(`MagicSquare`/`Cell`) · Boundary(`ResultDisplay`) | 세션 3는 Command 중심 |
| 1~16 **중복·범위** 검증 | 합 34 판정에 집중 *(세션 4+)* |

---

## §4. 도메인 · Rule (R1~R5)

### 4.1 Entity

| 항목 | 값 |
|------|-----|
| 격자 | 4×4 `list[list[int]]` |
| 셀 | **0**(빈칸) 또는 **1~16** |
| 부분 마방진 | 빈칸 2개(0), 나머지 1~16 각 1회 *(세션 3는 중복 assert 안 함)* |
| 마법상수 | **34** |

### 4.2 10선 (합 34 대상)

| 표기 | 줄 ID | 설명 |
|------|-------|------|
| R1~R4 | `row:0`~`row:3` | 행 4 |
| C1~C4 | `col:0`~`col:3` | 열 4 |
| D1 | `diag:main` | 주대각 (좌상→우하) |
| D2 | `diag:anti` | 반대각 (우상→좌하) |

### 4.3 Rule

| ID | 규칙 | status |
|----|------|--------|
| **R1** | 각 **행** 합 = 34 | `pass` / `fail` |
| **R2** | 각 **열** 합 = 34 | `pass` / `fail` |
| **R3** | **주대각** (`diag:main`) 합 = 34 | `pass` / `fail` |
| **R4** | **반대각** (`diag:anti`) 합 = 34 | `pass` / `fail` |
| **R5** | 격자에 **0이 하나라도** 있으면 → `status=incomplete`. **합 계산·34 비교하지 않음** (fail과 구분) | `incomplete` |

**판정 순서 (구현 권장)**

1. R5 — `0` 포함 시 즉시 `{ "status": "incomplete", "failed_lines": [] }` 반환  
2. R1~R4 — 10선 합 계산 → 모두 34이면 `pass`, 하나라도 아니면 `fail` + 틀린 줄 수집

---

## §5. Command API

### 5.1 시그니처

```python
def validate_lines(grid: list[list[int]]) -> dict:
    ...
```

- **구현**: `src/validate_lines.py`
- **테스트**: `tests/test_validate_lines.py`

### 5.2 ValidationResult 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | `str` | `"pass"` \| `"fail"` \| `"incomplete"` |
| `failed_lines` | `list[dict]` | fail 시 틀린 줄만. 각 항목: `id`, `sum`, `expected` |

**failed_lines 항목**

```python
{"id": "row:0", "sum": 33, "expected": 34}
```

- `expected`는 항상 **34**
- `id`는 §4.2 줄 ID만 사용
- **pass** · **incomplete** → `failed_lines == []`
- **fail** → 10선 **전부** 검사, 틀린 줄 **누락 없이** 반환 (다중 실패 포함)

### 5.3 status별 거동 요약

| status | 0 포함 | 10선 검사 | failed_lines |
|--------|--------|-----------|--------------|
| `pass` | ❌ | 모두 sum=34 | `[]` |
| `fail` | ❌ | 하나 이상 ≠34 | 틀린 줄만 |
| `incomplete` | ✅ (R5) | **하지 않음** | `[]` |

---

## §6. Acceptance Criteria (AC1~AC6)

| ID | 기준 | Mom Test 연결 |
|----|------|---------------|
| **AC1** | `validate_lines(grid)` **한 번**으로 10선(4+4+2) 합 34 검증 | 대각 누락 방지 |
| **AC2** | 완성 격자(0 없음) · 10선 모두 34 → `status=pass`, `failed_lines=[]` | 2차 전 항목 확인 → 1차에도 확신 |
| **AC3** | pass 시 10선 각 sum=34 *(구현 내부)*; 테스트는 status·failed_lines로 검증 | 성공 기준 #1 |
| **AC4** | `0` 포함 → `status=incomplete` (**pass 아님**), `failed_lines=[]`, 합 검증 생략 | fail vs incomplete 구분 |
| **AC5** | fail 시 `failed_lines`에 **틀린 줄 ID**·`sum`·`expected: 34` | 줄 단위 짚기 |
| **AC6** | RED 테스트: fail 시 **줄 ID·sum·expected**까지 assert | 20분 낭비 → 1번에 재현 |

---

## §7. Test Scenarios · TEST ID (T1~T5)

RED·GREEN·golden master에서 **필수**로 다루는 시나리오. 각 시나리오의 **TEST ID**는 **T1~T5**이다.

| TEST ID | 시나리오 | Arrange | 기대 status | failed_lines |
|---------|----------|---------|-------------|--------------|
| **T1** | 표준 4×4 마방진 (0 없음, 10선 합 34) | `VALID_GRID` *(§7.3)* | `pass` | `[]` |
| **T2** | **행** 하나 합 ≠ 34 (예: `row:0`, sum 33) | T1에서 R1 한 셀 변경 | `fail` | `[{id:"row:0", sum:33, expected:34}]` |
| **T3** | 격자에 **0**(빈칸) 포함 | 임의 완성 격자에 0 삽입 | `incomplete` | `[]` |
| **T4** | **대각선만** ≠ 34 | T1에서 주대각 또는 반대각만 변경 | `fail` | `diag:main` 또는 `diag:anti` + sum |
| **T5** | **여러 줄** 동시 ≠ 34 | 행·열 등 2줄 이상 동시 오류 | `fail` | **모든** 틀린 줄 ID·sum |

### 7.1 TEST ID 정의

| 구분 | ID 체계 | 용도 | 예 |
|------|---------|------|-----|
| **TEST ID** | **T1~T5** | pytest 시나리오·AC 추적·`/red-test-plan` 매트릭스 | T4 = 대각 단독 fail |
| **AC ID** | **AC1~AC6** | 수용 기준 (§6) | AC4 = incomplete 구분 |
| **줄 ID** | `row:*` · `col:*` · `diag:*` | `failed_lines[].id` — API 출력 | `diag:main` |

- TEST ID와 줄 ID는 **다른 체계**이다. T2는 TEST ID이고, 그 테스트가 assert하는 `failed_lines` 항목의 `id`가 줄 ID이다.
- T1~T5는 세션 3 **필수** 테스트다. `/red-skeleton`·`/tdd-red`·`/golden-master`·체크리스트에서 동일 ID를 사용한다.

### 7.2 AC ↔ TEST ID 추적 매트릭스

| TEST ID | 커버 AC | Mom Test · 비고 |
|---------|---------|-----------------|
| **T1** | AC1, AC2, AC3 | 10선 한 번 호출 · pass · golden master 앵커 |
| **T2** | AC1, AC5, AC6 | 행 단일 fail · 줄 ID·sum·expected assert |
| **T3** | AC4 | R5 incomplete · 합 검증 생략 |
| **T4** | AC1, AC5, AC6 | **대각 누락** 방지 — 대각 단독 fail |
| **T5** | AC1, AC5, AC6 | 다중 fail — **모든** 틀린 줄 누락 없이 assert |

- **AC1**은 모든 TEST ID에 공통: Act는 `validate_lines(grid)` **한 번**만 호출한다.
- 워크북 성공 기준 #2(Red→Green)는 **T3 → T1 → T2 → T4 → T5** RED 순서로 커버한다 *(§8.3 `/red-test-plan`)*.

### 7.3 Golden Master — VALID_GRID

```python
VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

- T1 · `/golden-master` 회귀 앵커로 고정 (**값 변경 금지**)
- 0 없음 · 10선 합 각 34

### 7.4 TEST ID ↔ pytest 함수명 (권장)

규칙: `test_<시나리오>_<기대status>`. 아래는 **권장 초안** — 의미가 같으면 변형 허용, TEST ID 매핑은 유지한다.

| TEST ID | 권장 함수명 | 기대 status |
|---------|-------------|-------------|
| **T1** | `test_complete_valid_grid_returns_pass` | `pass` |
| **T2** | `test_wrong_row_sum_returns_fail_with_line_detail` | `fail` |
| **T3** | `test_grid_with_zero_returns_incomplete` | `incomplete` |
| **T4** | `test_wrong_diagonal_sum_returns_fail_with_line_detail` | `fail` |
| **T5** | `test_multiple_wrong_lines_returns_fail_with_line_detail` | `fail` |

- T1이 `/golden-master`와 중복이면 **T1을 golden master로 승격**하고 함수 1개로 통합한다 *(`.cursor/commands/golden-master.md`)*.
- fail 계열(T2·T4·T5)은 AC6에 따라 `failed_lines` 각 항목의 `id`·`sum`·`expected: 34`까지 assert한다.

### 7.5 테스트 작성 규칙

- **AAA**: Arrange → Act → Assert
- **함수명**: §7.4 권장명 또는 `test_<시나리오>_<기대status>` — **TEST ID(T1~T5)와 1:1 대응** 주석 권장
- **Act**: `result = validate_lines(grid)` 한 번
- **Assert**: `status`, `failed_lines` — fail 시 줄 ID·`sum`·`expected`까지

---

## §8. TDD · ARRR Test Loop

### 8.1 Phase

| Phase | 수정 허용 | 금지 |
|-------|-----------|------|
| **RED** | `tests/` | `src/` |
| **GREEN** | `src/` | tests assert 완화 |
| **REFACTOR** | `src/` (동작 동일) | tests·공개 API 변경 |

- 사이클: **RED → GREEN → REFACTOR** — **한 번에 한 Phase**
- 응답 첫 줄: `[RED]` / `[GREEN]` / `[REFACTOR]`

### 8.2 금지

- assert 완화·삭제 · `@pytest.mark.skip` · `xfail` · 더미 구현으로 Red 회피
- Phase 밖 파일 수정

### 8.3 ARRR · Cursor 슬래시 커맨드

```text
Arrange  → /red-test-plan   T1~T5 매트릭스 (파일 변경 없음)
         → /red-skeleton     tests/ AAA 골격
Red      → /tdd-red          assert · pytest FAILED
         → /golden-master    VALID_GRID 회귀
Green    → /green-minimal    src/ 최소 구현
Refactor → /refactor-smell   냄새 분석
         → /refactor-safe    smell 1건 · green 유지
Repeat   → 새 시나리오
```

| pytest 단계 | 기대 |
|-------------|------|
| RED (skeleton / tdd-red) | FAILED (또는 ImportError) |
| GREEN / REFACTOR | 전부 passed |

```bash
pytest tests/test_validate_lines.py -v
```

---

## §9. 프로젝트 구조 · Harness

```
MagicSquare_xx/
├── docs/
│   └── PRD.md                 ← 본 문서
├── .cursorrules               ← ECB · TDD · AI (구현 SSOT)
├── .cursor/
│   ├── commands/              ← tdd-red, red-test-plan, green-minimal, …
│   └── skills/
│       ├── magic-square-tdd/
│       └── magic-square-docs/
├── pyproject.toml             ← pytest: testpaths, pythonpath
├── src/
│   ├── __init__.py
│   └── validate_lines.py
├── tests/
│   ├── __init__.py
│   └── test_validate_lines.py
├── Report/                    ← 세션 보고서
└── Prompting/                 ← Transcript Export
```

### 9.1 pytest 설정

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
```

---

## §10. 성공 기준 3개 (워크북 ↔ PRD 매핑)

| # | 워크북 성공 기준 | PRD |
|---|------------------|-----|
| 1 | 한 Command로 10선×34 검증 | AC1 · §4.2 · §5 · T1 |
| 2 | Red→Green: fail / incomplete / pass 재현 | T3·T1·T2·T4·T5 · §7.2 · §8 |
| 3 | fail 시 줄 ID·sum·expected | AC5·AC6 · T2·T4·T5 · §7.4 |

---

## §11. 관련 문서

| 문서 | 설명 |
|------|------|
| [`.cursorrules`](../.cursorrules) | ECB · API · TDD · AI 협업 |
| [Report/01 — Mom Test](../Report/01.MagicSquare_MomTest_Report.md) | 페르소나 · F-1~F-8 |
| [Report/03 — 워크북](../Report/03.MagicSquare_Session3_Workbook_Report.md) | R-G-I-O 원본 |
| [Report/04 — TDD RED](../Report/04.MagicSquare_TDD-RED-Command_Report.md) | `/tdd-red` |
| [Report/05 — Harness](../Report/05.MagicSquare_Session3-Harness-Cursorrules_Report.md) | 골격 · `.cursorrules` |
| [Report/06 — 계약 리뷰](../Report/06.MagicSquare_Session3-RGIO-Contract-Review_Report.md) | 갭 8건 → 본 PRD 반영 |
| [`.cursor/skills/magic-square-tdd/SKILL.md`](../.cursor/skills/magic-square-tdd/SKILL.md) | ARRR Skill |
| [`.cursor/commands/export.md`](../.cursor/commands/export.md) | Report · Transcript Export |

---

## §12. 변경 이력

| 버전 | 일자 | 변경 |
|------|------|------|
| 0.1 | 2026-06-10 | 초안 — Report/01·03·06 + `.cursorrules` + ARRR 커맨드 통합. `failed_lines` 계약 확정, R1~R4·T4·T5·pass/incomplete `failed_lines=[]` 보완 |
| 0.2 | 2026-06-10 | §7 TEST ID(T1~T5) 정의 · AC↔TEST ID 추적 매트릭스 · pytest 권장 함수명(§7.4) 추가 |

---

*본 문서는 `docs/PRD.md` — MagicSquare_xx 세션 3 Product Requirements Document (초안)입니다.*

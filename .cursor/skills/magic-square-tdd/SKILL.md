---
name: magic-square-tdd
description: >-
  MagicSquare_xx validate_lines TDD·ARRR 워크플로. RED/GREEN/REFACTOR Phase,
  /red-test-plan, /red-skeleton, /tdd-red, /green-minimal, /golden-master,
  /refactor-smell, /refactor-safe 호출 시 적용. 4×4 부분 마방진 10선 합 34 검증.
---

# MagicSquare_xx — TDD · ARRR Skill

`validate_lines` Test Loop를 **ARRR** 순서로 실행할 때 이 Skill을 따른다.

## SSOT

| 문서 | 역할 |
|------|------|
| `.cursorrules` | API · R5 · 10선 ID · Phase 규칙 (**1순위**) |
| `docs/PRD.md` | AC·T 시나리오 (없으면 `Report/03` · `Report/06`) |
| `.cursor/commands/export.md` | Report · Transcript Export (`export-session` 동일) |

## ARRR → 슬래시 커맨드

```text
Arrange ─┬─ /red-test-plan   테스트 매트릭스 (파일 변경 없음)
         └─ /red-skeleton     tests/ AAA 골격 · T1~T5 stub

Red      ─── /tdd-red          assert 본문 · pytest FAILED
         └── /golden-master    VALID_GRID 회귀 앵커 (tests/)

Green    ─── /green-minimal    src/ 최소 구현 · pytest 전부 passed

Refactor ┬─ /refactor-smell    냄새 분석 (파일 변경 없음)
         └─ /refactor-safe     smell 1건 · green 유지

Repeat   ─── 새 시나리오 → /red-test-plan 또는 /tdd-red
```

## Phase 선언 (응답 첫 줄)

| Phase | 선언 |
|-------|------|
| RED | `[RED]` 또는 `[RED] · Test Plan` / `[RED] · Skeleton` |
| GREEN | `[GREEN]` |
| REFACTOR | `[REFACTOR]` 또는 `[REFACTOR] · Smell` |

**한 번에 한 Phase만.** 다른 Phase 파일 수정 금지.

## API 계약 (`.cursorrules`)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...],  # fail 시만; pass/incomplete → []
}
```

| status | 조건 |
|--------|------|
| `pass` | 0 없음, 10선 합 34 |
| `fail` | 0 없음, 합 ≠ 34 줄 → `{ "id", "sum", "expected": 34 }` |
| `incomplete` | 0 포함 (R5) — **합 계산·34 비교 없음** |

10선 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`

## T1~T5 (RED 필수)

| ID | 기대 |
|----|------|
| T1 | pass · `failed_lines=[]` |
| T2 | fail · 단일 행 `id`·`sum` |
| T3 | incomplete · `failed_lines=[]` |
| T4 | fail · 대각 `diag:main` 또는 `diag:anti` |
| T5 | fail · **모든** 틀린 줄 |

## Phase별 수정 허용

| Phase | 허용 | 금지 |
|-------|------|------|
| RED (plan) | 없음 | src/, tests/ |
| RED | `tests/` | `src/` |
| GREEN | `src/` | tests/ assert 완화 |
| REFACTOR (smell) | 없음 | src/, tests/ |
| REFACTOR (safe) | `src/` | tests/, API 변경 |

## TDD 금지 (전 Phase)

- assert 완화·삭제 · `@pytest.mark.skip` · `xfail`
- Solver, UI, BCE, 1~16 중복·범위 검증
- **git commit / push** — 사용자 명시 요청 시만

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

| 단계 | 기대 결과 |
|------|-----------|
| skeleton / tdd-red | FAILED (또는 ImportError) |
| green-minimal / refactor-safe | 전부 passed |

## AI 협업

- **한국어**로 설명·보고
- 슬래시 커맨드만 입력해도 **질문 없이** SSOT 기준 실행
- 문서 Export는 `magic-square-docs` Skill · `/export` 사용

## 커맨드 파일 위치

| 슬래시 | 파일 |
|--------|------|
| `/red-test-plan` | `.cursor/commands/red-test-plan.md` |
| `/red-skeleton` | `.cursor/commands/red-skeleton.md` |
| `/tdd-red` | `.cursor/commands/tdd-red.md` |
| `/green-minimal` | `.cursor/commands/green-minimal.md` |
| `/golden-master` | `.cursor/commands/golden-master.md` |
| `/refactor-smell` | `.cursor/commands/refactor-smell.md` |
| `/refactor-safe` | `.cursor/commands/refactor-safe.md` |
| `/export` | `.cursor/commands/export.md` |

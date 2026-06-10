# MagicSquare_xx — <주제> Report

**작성 목적**: <한 줄 — 예: ARRR 실습 · RED Test Plan 커맨드 정의>  
**범위**: <수정·분석 범위 — 예: `.cursor/commands/` · tests/ RED만>  
**산출물 성격**: <예: Test Loop Arrange 단계 실행 가이드>

---

## 문서 메타데이터

| 항목 | 내용 |
|------|------|
| 문서 ID | `NN.MagicSquare_<주제>_Report` |
| 프로젝트 ID | MagicSquare_xx |
| 단계 | <예: 세션 3 — ARRR Arrange / RED Test Plan> |
| 작성일 | YYYY-MM-DD |
| 선행 문서 | [`NN....md`](./NN....md) |
| 대화 Export | [`Prompting/NN....md`](../Prompting/NN....md) |
| 산출 파일 | <예: `.cursor/commands/red-test-plan.md`> |

---

## 1. 요약

| 구분 | 결과 |
|------|------|
| 요청 | <한 줄> |
| 산출 | <파일·커맨드> |
| 정렬 기준 | `.cursorrules` · `docs/PRD.md` (또는 `Report/03`) |
| **판정** | <예: RED 진입 준비 / GREEN 완료 / REFACTOR 1건> |

---

## 2. ARRR · Phase (해당 시)

| 단계 | 슬래시 | Phase 선언 | 수정 허용 |
|------|--------|------------|-----------|
| Arrange | `/red-test-plan` | `[RED] · Test Plan` | 없음 |
| Arrange | `/red-skeleton` | `[RED] · Skeleton` | `tests/` |
| Red | `/tdd-red` | `[RED]` | `tests/` |
| Red | `/golden-master` | `[RED]`/`[GREEN]` | `tests/` |
| Green | `/green-minimal` | `[GREEN]` | `src/` |
| Refactor | `/refactor-smell` | `[REFACTOR] · Smell` | 없음 |
| Refactor | `/refactor-safe` | `[REFACTOR]` | `src/` |

TDD: **RED → GREEN → REFACTOR**. 한 번에 한 Phase.

---

## 3. API · 도메인 (`.cursorrules`)

```python
validate_lines(grid) -> {
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": [...],
}
```

| status | 조건 | failed_lines |
|--------|------|--------------|
| `pass` | 0 없음, 10선 합 34 | `[]` |
| `fail` | 0 없음, 합 ≠ 34 | `{ "id", "sum", "expected": 34 }` |
| `incomplete` | 0 포함 (R5) | `[]` — 합 검증 생략 |

10선 ID: `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`

---

## 4. 본문 (<세션 주제>)

<!-- TDD RED: AAA · pytest 예시 · T1~T5 -->
<!-- GREEN: R5 · 10선 · 최소 구현 -->
<!-- REFACTOR: smell 목록 · safe 변경 1건 -->
<!-- ARRR Harness: 커맨드 6종 + Skill 2종 목록 -->

---

## 5. pytest (해당 시)

```bash
pytest tests/test_validate_lines.py -v
```

| Phase | 기대 |
|-------|------|
| RED | N failed (또는 ImportError) |
| GREEN / REFACTOR | N passed, 0 failed |

---

## 6. 금지

| 금지 | 이유 |
|------|------|
| Phase 밖 파일 수정 | TDD 사이클 |
| assert 완화 · skip · xfail | Red 회피 |
| Solver, UI, 중복·범위 | 세션 3 범위 밖 |

---

## 7. 결론 및 다음 단계

### 결론

- <한 줄>

### 권장 액션

1. <다음 슬래시 또는 산출>
2. ...

---

## 8. 관련 문서

| 문서 | 설명 |
|------|------|
| [03.MagicSquare_Session3_Workbook_Report.md](./03.MagicSquare_Session3_Workbook_Report.md) | R-G-I-O · 성공 기준 |
| [`.cursorrules`](../.cursorrules) | ECB · TDD |
| [`.cursor/commands/export.md`](../.cursor/commands/export.md) | Export 커맨드 |

---

*본 문서는 `Report/NN.MagicSquare_<주제>_Report.md` — MagicSquare_xx <주제> 보고서입니다.*

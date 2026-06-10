# REFACTOR Safe — validate_lines

`/refactor-smell`에서 정한 **1순위 1건**만 리팩터한다. **pytest 전부 green**을 유지한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[REFACTOR]`
- RED·GREEN(기능 추가)은 하지 않는다.
- 한 번에 **한 가지** 구조 변경만 — 동작·공개 API 동일.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API · R5 · 10선 ID 불변 |
| `src/validate_lines.py` | 리팩터 대상 |
| `tests/test_validate_lines.py` | **변경 금지** — green 게이트 |
| `.cursor/commands/refactor-smell.md` | 선행 smell (없으면 Duplicated logic 1건만 자동 선택) |

**질문·추가 입력 없이** smell 1순위(또는 10선 합 중복 제거) 1건만 수행한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> dict` — 시그니처·키 이름 불변 |
| 수정 허용 | `src/validate_lines.py` |
| 수정 금지 | `tests/`, 공개 API 변경 |
| 도메인 | R5 · 10선 · failed_lines 계약 **동일** |

## Safe Refactor 절차

1. **Before** — `pytest tests/test_validate_lines.py -v` → 전부 passed 확인 (하나라도 fail이면 GREEN 먼저)
2. **Change** — smell 1건: 예) `_line_sum(cells) -> int` 추출, `MAGIC = 34` 상수, 10선 id·cells 튜플 루프
3. **After** — 동일 pytest → **전부 passed**
4. **Rollback rule** — failed 1개라도 → 변경 되돌리고 보고

### 허용 · 금지

| 허용 | 금지 |
|------|------|
| private helper (`_sum_row` 등) | `validate_lines` 반환 dict 구조 변경 |
| 상수 추출 · 작은 루프 통합 | 기능 추가 · R5 로직 변경 |
| 동작 동일 rename | tests/ 수정 |
| golden master 포함 전체 green | 한 PR에 smell 2건 이상 |

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

REFACTOR 완료: **0 failed**. golden master·T1~T5 포함.

## 보고 형식

```markdown
[REFACTOR]

## 변경 요약
- smell: (이름)
- 변경: (한 줄)

## pytest 결과
- Before: N passed
- After: N passed, 0 failed

## 다음 단계
- `/refactor-smell`: 잔여 smell 재점검
- smell 없음 → ARRR 사이클 종료 또는 새 RED 시나리오
```

## 금지

| 금지 | 이유 |
|------|------|
| `tests/` 수정 | 계약 고정 |
| 동작 변경 · API 변경 | REFACTOR 아님 |
| smell 2건 이상 동시 | rollback 어려움 |
| Solver, UI, 중복·범위 | 세션 3 범위 밖 |

## 체크리스트

- [ ] 응답 첫 줄 `[REFACTOR]`
- [ ] `src/` 만 변경 · smell 1건
- [ ] Before/After pytest **전부 passed**
- [ ] API·R5·failed_lines 불변

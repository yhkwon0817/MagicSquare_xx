# GREEN Minimal — validate_lines

현재 **실패 중인 RED 테스트**를 통과시키는 **최소 구현**만 `src/validate_lines.py`에 추가한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[GREEN]`
- RED(테스트 추가)·REFACTOR(구조 정리)는 하지 않는다.
- 테스트 assert 완화·삭제는 하지 않는다.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API · R5 · 10선 ID |
| `docs/PRD.md` | AC·T (없으면 `Report/03`) |
| `tests/test_validate_lines.py` | **통과 대상** — assert가 진실 |

**질문·추가 입력 없이** 실패 테스트를 읽고 최소 구현한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> { "status", "failed_lines" }` |
| 수정 허용 | `src/` (`src/validate_lines.py`) |
| 수정 금지 | `tests/` (assert 변경 금지) |
| 도메인 | 4×4, 0 또는 1~16, 마법상수 **34**, 10선 |

## 최소 구현 순서

1. **R5 선행** — `0` in any cell → `{ "status": "incomplete", "failed_lines": [] }`, **즉시 return** (합 계산 없음)
2. **10선 합** — 행 4 · 열 4 · `diag:main` · `diag:anti` 각 sum 계산
3. **fail 수집** — sum ≠ 34인 줄만 `{ "id", "sum", "expected": 34 }` append
4. **pass** — failed_lines 비어 있으면 `status=pass`
5. **fail** — 하나라도 있으면 `status=fail`

줄 ID (`.cursorrules` 준수):

- `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti`

### 허용 · 금지 (GREEN 품질)

| 허용 | 금지 |
|------|------|
| if/for로 직접 합산 | Solver, UI, 중복·범위 검증 |
| 테스트 통과에 필요한 최소 분기 | 테스트 파일 수정 |
| 매직 넘버 `34` (또는 상수 1개) | “미래 확장” 추상화·과잉 클래스 |

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

GREEN 확인: **전부 passed**. 하나라도 FAILED면 GREEN 미완.

## 보고 형식

```markdown
[GREEN]

## 구현 요약
- R5 incomplete 조기 return
- 10선 합 · failed_lines 수집

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N passed, 0 failed

## 다음 단계
- `/refactor-smell`: 코드 냄새 점검
- `/refactor-safe`: Green 유지 리팩터
```

## 금지

| 금지 | 이유 |
|------|------|
| `tests/` assert 완화·삭제 | Red 회피 |
| REFACTOR성 대규모 구조 변경 | `/refactor-safe` |
| 범위 밖 기능 | 세션 3 |

## 체크리스트

- [ ] 응답 첫 줄 `[GREEN]`
- [ ] `src/` 만 변경
- [ ] R5 · 10선 · failed_lines 계약
- [ ] pytest **전부 passed**
- [ ] 최소 구현 (불필요 추상화 없음)

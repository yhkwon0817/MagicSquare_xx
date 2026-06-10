# RED Skeleton — validate_lines

`tests/test_validate_lines.py`에 **AAA 골격·fixture·함수명**만 추가한다. assert 본문은 **TODO**로 남기고 RED 실패를 유지한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[RED] · Skeleton`
- GREEN·REFACTOR 작업은 하지 않는다. `src/`는 건드리지 않는다.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API · 10선 ID · R5 |
| `docs/PRD.md` | T1~T5 (없으면 `Report/03` · `Report/06`) |
| `.cursor/commands/red-test-plan.md` | 계획표 형식 (선행 `/red-test-plan` 없어도 T1~T5 자동 적용) |

**질문·추가 입력 없이** T1~T5 골격을 한 번에 작성한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> dict` |
| 수정 허용 | `tests/` 만 (`tests/test_validate_lines.py`) |
| 수정 금지 | `src/` 전체 |
| 도메인 | 4×4, 0 또는 1~16, 마법상수 **34**, 10선 |

## Skeleton 규칙

각 테스트 함수는 **Arrange → Act → Assert** 순서를 주석으로 명시한다.

1. **Arrange** — `grid` 상수 또는 module-level fixture 사용
2. **Act** — `result = validate_lines(grid)` 한 줄
3. **Assert** — `# TODO: assert ...` 주석 + **`pytest.fail("RED skeleton — assert pending")`**  
   (assert 본문을 아직 쓰지 않았음을 명확히 하고 RED 유지)

**함수명**: `test_<시나리오>_<기대status>` (예: `test_complete_valid_grid_returns_pass`)

### module-level 상수 (필수)

```python
import pytest
from validate_lines import validate_lines

MAGIC = 34

VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

T1~T5 각각 **함수 stub 1개** — 총 5개 테스트 함수.

### T4 · T5 격자 (Skeleton용 기본값)

- **T4**: `VALID_GRID`에서 주대각 한 셀만 변경해 `diag:main` sum ≠ 34
- **T5**: 행·열 각 1줄 이상 동시에 ≠ 34

## pytest

```bash
pytest tests/test_validate_lines.py -v
```

Skeleton 확인: **5 failed** (`pytest.fail` 메시지) 또는 `ImportError`(구현 없음). **passed 0**이면 skeleton 미완.

## 금지

| 금지 | 이유 |
|------|------|
| `src/` 수정 | GREEN 전용 |
| assert 본문 완성 | `/tdd-red`에서 처리 |
| `@pytest.mark.skip`, `xfail` | Red 회피 |
| Solver, UI, 중복·범위 검증 | 세션 3 범위 밖 |

## 보고 형식

```markdown
[RED] · Skeleton

## 추가·변경
- `tests/test_validate_lines.py`: MAGIC, VALID_GRID, T1~T5 stub 5개

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v`
- 결과: N failed (skeleton pending)

## 다음 단계
- `/tdd-red`: Assert TODO → 실제 assert, pytest FAILED(의미 있는 실패) 확인
```

## 체크리스트

- [ ] 응답 첫 줄 `[RED] · Skeleton`
- [ ] `tests/` 만 변경
- [ ] T1~T5 함수 5개 · AAA 주석 · `pytest.fail` placeholder
- [ ] VALID_GRID · MAGIC 상수
- [ ] pytest 실행 후 **전부 failed** (또는 ImportError)

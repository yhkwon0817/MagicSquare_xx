# Golden Master — validate_lines

표준 4×4 마방진 **VALID_GRID**를 golden master fixture로 고정하고, **회귀 앵커** 테스트 1건을 `tests/`에 추가한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[RED]` *(golden master 테스트 추가)* 또는 `[GREEN]` *(구현 없이 이미 pass인 경우)*  
  — 구현이 없으면 `[RED]`, pass면 `[GREEN]`으로 선언.
- REFACTOR는 하지 않는다.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | pass 계약 · 10선 |
| `docs/PRD.md` | T1 / AC3 (없으면 `Report/03` 성공 기준 #1) |
| `tests/test_validate_lines.py` | 기존 `VALID_GRID` 재사용 우선 |

**질문·추가 입력 없이** golden master 테스트 1건을 추가한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> dict` |
| 수정 허용 | `tests/` (`tests/test_validate_lines.py`) |
| 수정 금지 | `src/` (GREEN에서만 구현) |
| Golden master | 아래 **VALID_GRID** 고정 (변경 금지) |

### VALID_GRID (golden master)

```python
VALID_GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
```

- 0 없음 · 10선 합 각 34 · 1~16 각 1회 (세션 3는 중복 assert **하지 않음** — 합 34만)

## Golden Master 테스트 규칙

**함수명**: `test_golden_master_valid_grid_regression` (이미 T1과 중복이면 **T1을 golden master로 승격**하고 중복 함수는 merge)

**AAA**:

1. **Arrange** — `grid = VALID_GRID` (module constant 참조, **리터럴 복붙 금지**)
2. **Act** — `result = validate_lines(grid)`
3. **Assert** — `status == "pass"`, `failed_lines == []`

주석 한 줄: `# Golden master — 회귀 시 이 격자·기대값 불변`

## pytest

```bash
pytest tests/test_validate_lines.py -v -k golden_master
```

- 구현 전: **FAILED** (RED) — `/green-minimal` 대상
- 구현 후: **passed** — 이후 REFACTOR에서도 **항상 pass** 유지

## 금지

| 금지 | 이유 |
|------|------|
| VALID_GRID 값 변경 | golden master 훼손 |
| assert 완화 | 회귀 무력화 |
| `src/` 수정 (본 커맨드) | 테스트 추가 단계 |
| Solver, UI, 중복·범위 assert | 세션 3 범위 밖 |

## 보고 형식

```markdown
[RED] 또는 [GREEN]

## Golden Master
- fixture: `VALID_GRID` (module-level)
- test: `test_golden_master_valid_grid_regression`

## pytest 결과
- 명령: `pytest tests/test_validate_lines.py -v -k golden_master`
- 결과: ...

## 다음 단계
- RED면 `/green-minimal`
- GREEN면 `/refactor-smell` — golden master pass 유지
```

## 체크리스트

- [ ] Phase 첫 줄 선언
- [ ] `VALID_GRID` 단일 SSOT · 테스트는 참조만
- [ ] `tests/` 만 변경
- [ ] pytest 실행·결과 보고

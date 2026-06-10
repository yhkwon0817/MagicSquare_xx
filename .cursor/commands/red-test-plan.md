# RED Test Plan — validate_lines

`validate_lines` **RED 진입 전** 테스트 계획만 수립한다. **파일은 수정하지 않는다** — 채팅에 계획표만 출력한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[RED] · Test Plan`
- 구현·테스트 코드 작성·pytest 실행은 하지 않는다.
- GREEN·REFACTOR 작업은 하지 않는다.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API · 10선 ID · R5 · TDD Phase |
| `docs/PRD.md` | AC·T 시나리오 (없으면 `Report/03` §3 · `Report/06` 갭 반영) |
| `Report/03.MagicSquare_Session3_Workbook_Report.md` | R-G-I-O · 성공 기준 3개 |

**질문·추가 입력 없이** 위 SSOT만으로 계획을 완성한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| API | `validate_lines(grid) -> { "status", "failed_lines" }` |
| 수정 허용 | **없음** (계획 출력만) |
| 수정 금지 | `src/`, `tests/` 전체 |
| 도메인 | 4×4, 셀 0 또는 1~16, 마법상수 **34**, 10선 |
| 10선 ID | `row:0`~`row:3`, `col:0`~`col:3`, `diag:main`, `diag:anti` |

### status · failed_lines 계약

| status | 조건 | failed_lines |
|--------|------|--------------|
| `pass` | 0 없음, 10선 합 모두 34 | `[]` |
| `fail` | 0 없음, 하나 이상 합 ≠ 34 | 틀린 줄만 `{ "id", "sum", "expected": 34 }` |
| `incomplete` | 0 하나라도 포함 (R5) | `[]` — 합 계산·34 비교 **하지 않음** |

## 필수 시나리오 (T1~T5)

SSOT·워크북·계약 리뷰(`Report/06`)를 반영해 **아래 5건을 반드시** 계획에 포함한다.

| ID | 시나리오 | 기대 status | assert 포인트 |
|----|----------|-------------|---------------|
| **T1** | 표준 4×4 마방진 (0 없음, 10선 합 34) | `pass` | `failed_lines == []` |
| **T2** | 행 하나 합 ≠ 34 (예: `row:0`) | `fail` | `id`, `sum`, `expected: 34` |
| **T3** | 격자에 0(빈칸) 포함 | `incomplete` | `failed_lines == []`, 합 검증 없음 |
| **T4** | 대각선만 ≠ 34 (`diag:main` 또는 `diag:anti`) | `fail` | 대각 줄 ID·sum |
| **T5** | **여러 줄** 동시 ≠ 34 | `fail` | **모든** 틀린 줄 ID·sum |

## 실행 절차

1. SSOT에서 API·R5·10선 ID·금지 범위 확인
2. T1~T5 각각에 대해 **격자 개요**(어떤 셀을 바꿀지) · **함수명 초안** · **AAA 요약** 작성
3. 우선순위: T3(R5) → T1(pass) → T2(fail 단일) → T4 → T5
4. 아래 **보고 형식**으로 출력 — **파일 생성·수정 없음**

## 보고 형식

```markdown
[RED] · Test Plan

## 테스트 매트릭스

| ID | 함수명(안) | Arrange 요약 | Act | Assert 핵심 | 우선순위 |
|----|------------|--------------|-----|-------------|----------|
| T1 | test_... | ... | validate_lines(grid) | status=pass, failed_lines=[] | ... |
| ... | ... | ... | ... | ... | ... |

## fixture · 상수 (안)
- `MAGIC = 34`
- `VALID_GRID`: 표준 4×4 마방진 (T1·golden master 공용)

## RED 순서 제안
1. ...
2. ...

## 다음 단계
- `/red-skeleton`: tests/ 골격·fixture
- `/tdd-red`: assert 본문 추가 후 pytest FAILED 확인
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` · `tests/` 수정 | 계획 단계 |
| pytest 실행 | `/red-skeleton` · `/tdd-red` 이후 |
| 사용자에게 시나리오 질문 | SSOT로 자급 |
| Solver, UI, 중복·범위 검증 시나리오 | 세션 3 범위 밖 |

## 체크리스트

- [ ] 응답 첫 줄 `[RED] · Test Plan`
- [ ] T1~T5 전부 포함
- [ ] 10선 ID·R5·failed_lines 계약 준수
- [ ] 파일 변경 없음
- [ ] `/red-skeleton` 다음 단계 명시

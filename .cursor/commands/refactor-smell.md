# REFACTOR Smell — validate_lines

`src/validate_lines.py`의 **코드 냄새만** 식별한다. **파일은 수정하지 않는다** — 분석표만 출력한다.

## Phase 선언

- 응답 **첫 줄**에 반드시 선언: `[REFACTOR] · Smell`
- 코드 변경·테스트 변경·pytest 실행은 **하지 않는다** (분석만).
- RED·GREEN 작업은 하지 않는다.

## SSOT (읽기 전용)

| 문서 | 용도 |
|------|------|
| `.cursorrules` | API · R5 · 10선 |
| `src/validate_lines.py` | 분석 대상 |
| `tests/test_validate_lines.py` | 행동 계약 (변경 금지) |

**질문·추가 입력 없이** 현재 `src/validate_lines.py`를 읽고 냄새 목록을 작성한다.

## 대상 범위

| 항목 | 내용 |
|------|------|
| 분석 대상 | `src/validate_lines.py` |
| 수정 허용 | **없음** |
| 수정 금지 | `src/`, `tests/` |

## 점검 카탈로그 (MagicSquare 세션 3)

아래 항목을 **해당 시** 표에 기록한다.

| Smell | 징후 (validate_lines 맥락) |
|-------|---------------------------|
| **Duplicated 10-line logic** | 행/열/대각 합·비교 블록 반복 |
| **Magic number scatter** | `34` 리터럴 다수 (상수 1개면 OK) |
| **Deep nesting** | R5·fail 수집 if 중첩 3단계 이상 |
| **Long function** | `validate_lines` 한 함수 40줄 초과 |
| **Dead branch** | unreachable code · unused 변수 |
| **Wrong abstraction** | Solver/UI/중복검증 혼입 |
| **ID string typo risk** | 줄 ID 하드코딩 불일치 (`row:0` vs `R1`) |

**없음**이면 “냄새 없음 — `/refactor-safe` 생략 가능” 명시.

## 실행 절차

1. `src/validate_lines.py` 전체 읽기
2. 카탈로그 대조 → **위치(함수·줄)** · smell · **한 줄 개선 방향** 기록
3. **우선순위**: 동작 영향 큰 중복 → 매직 넘버 → 네이밍
4. `/refactor-safe`에 넘길 **1순위 항목 1개**만 추천

## 보고 형식

```markdown
[REFACTOR] · Smell

## 코드 냄새 목록

| # | 위치 | Smell | 개선 방향 (한 줄) | 우선순위 |
|---|------|-------|-------------------|----------|
| 1 | validate_lines L.. | ... | ... | 높음 |

## 1순위 refactor-safe 대상
- ...

## 다음 단계
- `/refactor-safe`: 1순위 1건만, pytest green 유지
```

## 금지

| 금지 | 이유 |
|------|------|
| `src/` · `tests/` 수정 | 분석 단계 |
| 범위 밖 리팩터 제안 (Solver 등) | 세션 3 |
| 테스트 assert 변경 제안 | 계약 불변 |

## 체크리스트

- [ ] 응답 첫 줄 `[REFACTOR] · Smell`
- [ ] 파일 변경 없음
- [ ] smell ≥0건 명시 (없으면 “없음”)
- [ ] `/refactor-safe` 1순위 1건 추천

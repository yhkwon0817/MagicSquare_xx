# MagicSquare_xx — <주제> Checklist

**문서 ID**: `NN.MagicSquare_<주제>_Checklist`  
**대응 Report**: [`Report/NN.MagicSquare_<주제>_Report.md`](./NN.MagicSquare_<주제>_Report.md)  
**작성일**: YYYY-MM-DD

---

## Phase · 커맨드 실행

| # | 슬래시 | Phase | 파일 변경 | pytest 기대 | 완료 |
|---|--------|-------|-----------|-------------|------|
| 1 | `/red-test-plan` | `[RED] · Test Plan` | 없음 | 미실행 | [ ] |
| 2 | `/red-skeleton` | `[RED] · Skeleton` | `tests/` | failed (skeleton) | [ ] |
| 3 | `/tdd-red` | `[RED]` | `tests/` | failed (assert) | [ ] |
| 4 | `/golden-master` | `[RED]`/`[GREEN]` | `tests/` | failed → passed | [ ] |
| 5 | `/green-minimal` | `[GREEN]` | `src/` | 전부 passed | [ ] |
| 6 | `/refactor-smell` | `[REFACTOR] · Smell` | 없음 | 미실행 | [ ] |
| 7 | `/refactor-safe` | `[REFACTOR]` | `src/` | 전부 passed | [ ] |
| 8 | `/export` | — | Report·Transcript | — | [ ] |

---

## T1~T5 시나리오

| ID | 테스트 함수 | status | failed_lines assert | 완료 |
|----|-------------|--------|---------------------|------|
| T1 | test_..._pass | pass | `[]` | [ ] |
| T2 | test_..._fail | fail | `id`, `sum`, `expected: 34` | [ ] |
| T3 | test_..._incomplete | incomplete | `[]` | [ ] |
| T4 | test_..._diag_fail | fail | `diag:main` 또는 `diag:anti` | [ ] |
| T5 | test_..._multi_fail | fail | 모든 틀린 줄 | [ ] |

---

## 계약 · 금지

- [ ] API: `status` + `failed_lines` (`.cursorrules`)
- [ ] R5: 0 포함 → incomplete, 합 검증 생략
- [ ] 10선 ID: `row:*`, `col:*`, `diag:main`, `diag:anti`
- [ ] assert 완화 · skip · xfail **없음**
- [ ] Solver · UI · 중복·범위 **범위 밖**
- [ ] Phase당 한 종류 수정만 (plan/smell = 변경 없음)

---

## pytest 최종

```bash
pytest tests/test_validate_lines.py -v
```

- [ ] 명령 실행
- [ ] 결과: ___ passed, ___ failed
- [ ] golden master (`-k golden_master`) passed

---

## Export

- [ ] `Report/NN....md` 생성
- [ ] `Prompting/NN....md` 생성
- [ ] NN 번호 중복 없음

---

*본 문서는 `Report/NN.MagicSquare_<주제>_Checklist.md` — MagicSquare_xx <주제> 실행 체크리스트입니다.*

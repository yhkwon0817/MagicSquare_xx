# Export — Report · Transcript

현재 Cursor 세션을 **Report** 보고서와 **Prompting** Transcript로 Export한다.  
**다른 파일은 만들지 않는다** — 아래 2개 산출물만 생성.

## 파일명 규칙 (`01.XXX` 형식)

`Report/` · `Prompting/`에 이미 있는 `NN.` 접두 번호를 확인하고, **다음 순번**을 쓴다.

| 위치 | 패턴 | 예시 |
|------|------|------|
| Report | `NN.MagicSquare_<주제>_Report.md` | `04.MagicSquare_TDD-RED-Command_Report.md` |
| Prompting | `NN.MagicSquare_<주제>-Transcript.md` | `04.MagicSquare_TDD-RED-Command-Transcript.md` |

- `NN` = 두 자리 순번 (`01`, `02`, …). 기존 최대값 + 1.
- `<주제>` = kebab-case 또는 PascalCase 요약 (영문 권장).
- Report와 Transcript는 **같은 NN**을 공유한다.

## Report 보고서 구조

`Report/NN.MagicSquare_<주제>_Report.md`:

1. **제목·작성 목적·범위**
2. **문서 메타데이터** — 문서 ID, 작성일, 선행 문서, 대응 Transcript 링크
3. **요약** — 세션 결과 한눈에
4. **본문** — 세션 주제에 맞는 정리 (TDD RED 세션이면 아래 필수 섹션 포함)
5. **결론 및 다음 단계**
6. **관련 문서** — 상호 링크

### TDD RED 세션 시 필수 포함

| 섹션 | 내용 |
|------|------|
| Phase 선언 | `[RED]` 첫 줄, GREEN/REFACTOR 금지 |
| AAA 절차 | Arrange → Act → Assert, 함수명 규칙 |
| pytest 예시 | pass / incomplete(R5) / fail(줄 ID·sum·expected) |
| 보고 형식 | 추가 테스트 · pytest 결과 · GREEN 다음 단계 |
| 금지 | `src/` 수정, assert 완화·skip·xfail |

## Prompting Transcript 구조

`Prompting/NN.MagicSquare_<주제>-Transcript.md`:

```markdown
# MagicSquare_xx — <주제> Transcript

_Exported on YYYY-MM-DD from Cursor (MagicSquare_xx 세션)_

**정리 보고서**: [`Report/NN....md`](../Report/NN....md)

---

**User**
(사용자 요청 원문 또는 요약)

---

**Cursor**
(응답·산출·결정 요약)

---

## 문서 관계
(선행 → 본 세션 → 후속 흐름)
```

- 대화는 **User / Cursor** 교대로 정리. 도구 호출·내부 추론은 생략.
- 핵심 코드·결정만 발췌. 전체 덤프 금지.

## 실행 절차

1. `Report/` · `Prompting/`에서 기존 `NN.` 목록 확인 → 다음 번호 결정
2. 세션 주제·산출물·선행 문서 파악
3. **Report** 작성 — 위 구조 + TDD RED 해당 시 필수 5섹션
4. **Transcript** 작성 — User/Cursor 교대, Report 링크
5. 응답에서 생성한 **파일 경로 2개**만 보고 (다른 파일 생성 금지)

## 응답 보고 형식

```markdown
## Export 완료

| 파일 | 역할 |
|------|------|
| `Report/NN....md` | 정형 보고서 |
| `Prompting/NN....md` | 대화 Transcript |
```

## 금지

- Report·Transcript·본 커맨드(`export.md`) **외** 파일 생성·수정
- `src/` 수정, assert 완화 (TDD RED 내용 기술 시에도 **규칙으로만** 기술)
- 번호 중복 (`01`이 이미 있으면 새 `01` 생성 금지)

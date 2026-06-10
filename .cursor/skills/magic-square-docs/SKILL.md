---
name: magic-square-docs
description: >-
  MagicSquare_xx Report·Transcript·Checklist 작성. /export 호출, 세션 Export,
  ARRR·TDD 커맨드 산출물 문서화 시 적용. Report/Prompting NN. 형식 준수.
---

# MagicSquare_xx — Docs Skill

세션·커맨드·ARRR 실습 결과를 **Report** · **Transcript** · **Checklist**로 정리할 때 이 Skill을 따른다.

## SSOT

| 문서 | 역할 |
|------|------|
| `.cursorrules` | 도메인 · API · TDD 규칙 |
| `docs/PRD.md` | 제품 요구 (없으면 `Report/03` §3) |
| `.cursor/commands/export.md` | Export 실행 절차 (**export-session** 동일) |

템플릿: 이 디렉터리의 `report-template.md`, `transcript-template.md`, `checklist-template.md`

## 산출물 3종

| 종류 | 저장 위치 | 용도 |
|------|-----------|------|
| **Report** | `Report/NN.MagicSquare_<주제>_Report.md` | 정형 보고서 |
| **Transcript** | `Prompting/NN.MagicSquare_<주제>-Transcript.md` | User/Cursor 대화 Export |
| **Checklist** | `Report/NN.MagicSquare_<주제>_Checklist.md` | Phase·커맨드 실행 체크 |

`NN` = `Report/` · `Prompting/` 기존 최대값 + 1 (Report·Transcript·Checklist **같은 NN** 권장).

## `/export` 실행 (질문 없이)

1. `Report/` · `Prompting/`에서 `NN.` 목록 확인
2. 세션 주제·선행 문서·산출 파일 파악
3. **Report** — [report-template.md](./report-template.md) 구조
4. **Transcript** — [transcript-template.md](./transcript-template.md) 구조
5. ARRR·TDD 세션이면 **Checklist** — [checklist-template.md](./checklist-template.md) (선택)
6. 응답에 생성 **파일 경로만** 보고 — SSOT·템플릿 **외** 파일 생성 금지

## ARRR 세션 Report 필수 섹션

| 섹션 | 내용 |
|------|------|
| ARRR 매핑 | Arrange/Red/Green/Refactor/Replay + 사용 커맨드 |
| Phase 선언 | `[RED]`/`[GREEN]`/`[REFACTOR]` 규칙 |
| API 계약 | `status` · `failed_lines` · R5 · 10선 ID |
| pytest | 명령·결과 (RED=failed, GREEN=passed) |
| 금지 | src/·tests/ Phase 위반 · assert 완화 |

## Transcript 규칙

- **User / Cursor** 교대 — 도구 호출·내부 추론 생략
- Report 상호 링크
- 핵심 코드·결정만 발췌

## Checklist 규칙

- 커맨드별 체크박스 — 실행 여부·pytest 결과·Phase 위반 없음
- `/red-test-plan` ~ `/refactor-safe` + `/tdd-red` + `/export` 항목

## 금지

- Report·Transcript·Checklist·export 커맨드 **외** 파일 생성 (세션 Export 시)
- 번호 중복 (`01` 재사용 금지)
- `src/` 수정 (문서 Skill만 사용할 때)

## 관련 Skill

- TDD 실행: [magic-square-tdd](../magic-square-tdd/SKILL.md)

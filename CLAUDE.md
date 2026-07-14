# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

볼링 게임 카타(The Bowling Game Kata) — 유효한 투구(roll) 순서가 주어졌을 때 텐핀 볼링 게임의 최종 점수를 계산하는 `Game` 클래스를 구현한다. 투구/프레임 수의 유효성 검증과 중간 프레임 점수 조회는 범위에서 제외한다 (핵심 점수 계산 로직에 집중).

`Game`이 제공해야 하는 인터페이스:
- `roll(pins: int) -> None` — 한 번의 투구를 기록
- `score() -> int` — 게임 종료 후 총점 반환

점수 규칙(스페어/스트라이크 보너스, 10번째 프레임의 추가 투구 처리 등)은 이 카타의 핵심이며, 구현 시 표준 볼링 점수 규칙을 그대로 따른다.

**현재 상태:** 초기 셋업 단계. PyCharm이 생성한 `main.py`(보일러플레이트, 실제 로직과 무관)와 pytest/pytest-cov가 설치된 `.venv`만 존재하며, `Game` 클래스와 테스트는 아직 작성되지 않았다.

## 개발 방식 — TDD 필수

이 저장소에서 기능 구현이나 버그 수정을 할 때는 반드시 `test-driven-development` 스킬(`.claude/skills/test-driven-development/SKILL.md`)의 Red-Green-Refactor 절차를 따른다: 실패하는 테스트를 먼저 작성하고 실패를 직접 확인한 뒤, 최소한의 코드로 통과시키고, 그 다음에만 리팩터링한다. 테스트보다 프로덕션 코드를 먼저 작성하지 않는다.

권장 테스트 진행 순서 (점진적으로 규칙을 확장):
1. 모든 투구가 거터(0핀) → 총점 0
2. 모든 투구가 1핀 → 총점 20
3. 스페어가 있는 경우
4. 스트라이크가 있는 경우
5. 퍼펙트 게임(전부 스트라이크) → 총점 300
6. 10번째 프레임에서 스페어/스트라이크로 인한 추가 투구

## 명령어

가상환경은 `.venv`에 이미 구성되어 있고 pytest, pytest-cov가 설치되어 있다.

```bash
# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 전체 테스트 실행
pytest

# 특정 파일만 실행
pytest tests/test_game.py

# 특정 테스트 하나만 실행
pytest tests/test_game.py::test_all_gutters_scores_zero

# 첫 실패에서 즉시 중단 (RED 확인용)
pytest -x

# 커버리지 확인
pytest --cov=src
```

## 예정 프로젝트 구조

```
Bowling_TDD/
├── src/
│   └── game.py        # Game 클래스 구현
├── tests/
│   └── test_game.py   # pytest 테스트
└── .claude/skills/test-driven-development/SKILL.md
```

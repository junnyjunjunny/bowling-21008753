# Plan: 모든 투구가 거터(0핀)인 경우 총점 0

## 목표 (RED)

`Game` 클래스에 20번 연속으로 0핀(거터)을 투구했을 때, `score()`가 0을 반환하는지 검증하는 테스트를 작성한다.

## 작성할 테스트

파일: `tests/test_game.py`

```python
from src.game import Game


def test_all_gutters_scores_zero():
    game = Game()

    for _ in range(20):
        game.roll(0)

    assert game.score() == 0
```

- 10프레임 × 2투구 = 20번의 `roll(0)` 호출.
- 스트라이크/스페어가 전혀 없는 가장 단순한 케이스이므로, 다른 로직(보너스 계산)이 개입할 여지가 없다.

## 예상되는 최소 구현 범위 (GREEN에서 진행 예정)

파일: `src/game.py`

- `Game` 클래스와 `__init__`, `roll(pins)`, `score()` 메서드의 최소 골격만 생성.
- `roll`: 매 투구를 리스트 등에 기록만 한다.
- `score`: 기록된 투구 값들의 단순 합계를 반환한다 (이 테스트를 통과시키는 데 필요한 최소 범위이며, 스페어/스트라이크 보너스 로직은 이번 사이클에서 구현하지 않는다).

## 이번 사이클에서 다루지 않는 것

- 스페어/스트라이크 보너스 계산
- 10번째 프레임 추가 투구 처리
- 입력 유효성 검증
